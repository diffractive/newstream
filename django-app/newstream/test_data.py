import random, string
from django.conf import settings
from allauth.account.models import EmailAddress
from datetime import datetime
from django.contrib.auth import get_user_model
from django.conf import settings

from donations.models import DonationForm, Donation, Subscription, STATUS_COMPLETE, STATUS_ACTIVE
from site_settings.models import AdminEmails, SiteSettings, PaymentGateway
from django.utils.timezone import make_aware
from donations.payment_gateways.stripe.constants import (EVENT_CHECKOUT_SESSION_COMPLETED,
    EVENT_PAYMENT_INTENT_SUCCEEDED, EVENT_INVOICE_CREATED, EVENT_INVOICE_PAID,
    EVENT_CUSTOMER_SUBSCRIPTION_UPDATED, EVENT_CUSTOMER_SUBSCRIPTION_DELETED)
import requests

User = get_user_model()

def rand_alphanumeric(length):
    """ for generating donation/subscription identifiers
    """
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

test_users = [
    {
        "email": "david.donor@diffractive.io",
        "password": "david.donor",
        "first_name": "David",
        "last_name": "Donor"
    }
]

test_donations = [
    {
        "user_email": "david.donor@diffractive.io", # for matching up the right user
        "transaction_id": "ch_3Mxo8cTTD2mrB42B1TnMfzL5",
        "is_recurring": False,
        "donation_amount": 1000,
        "currency": "HKD",
        "gateway": "stripe",
        "guest_email": '',
        "guest_name": '',
        "payment_status": STATUS_COMPLETE,
        "donation_date": datetime.strptime("2023-04-01", '%Y-%m-%d'),
    }
]

test_subscriptions = [
    {
        "user_email": "david.donor@diffractive.io", # for matching up the right user
        "profile_id": "sub_1Mxo8cTTD2mrB42B414bD7LS",
        "recurring_amount": 250,
        "currency": "HKD",
        "gateway": "stripe",
        "recurring_status": STATUS_ACTIVE,
        "subscribe_date": datetime.strptime("2023-02-05", '%Y-%m-%d'),
        "donation_transaction_ids": [
            "ch_4Mxo8cTTD2mrB42B1TnMfzL5",
            "ch_5Mxo8cTTD2mrB42B1TnMfzL6",
            "ch_6Mxo8cTTD2mrB42B1TnMfzL7"
        ] # including 1st donation and subsequent renewals to be created
    }
]

stripe_settings = {
    "test_product_id": "prod_TEST_PRODUCT_ID",
    "test_webhook_key": "whsec_TEST_WEBHOOK_KEY",
    "test_secret_key": "sk_TEST_SECRET_KEY",
    "live_product_id": "prod_LIVE_PRODUCT_ID",
    "live_webhook_key": "whsec_LIVE_WEBHOOK_KEY",
    "live_secret_key": "sk_LIVE_SECRET_KEY",
}

# for referencing when setting up donations/subscriptions
loaded_users = {}

def load_test_data():
    load_settings()
    if settings.RUN_LOCALSTRIPE:
        load_localstripe_webhooks()
        load_localstripe_create_product()
    load_test_users()
    load_test_donations()

def load_settings():
    """ Load necessary settings in order to let the app run smoothly e.g. sending emails ok
    """
    site_settings = SiteSettings.objects.get(pk=1)

    # set default from email address
    site_settings.default_from_email = settings.DEFAULT_FROM_EMAIL
    site_settings.default_from_name = 'Admin'

    # set default admin_emails list
    site_settings.admin_emails.add(AdminEmails(
        title="Admin",
        email=settings.DEFAULT_ADMIN_EMAIL,
    ))

    # set stripe product ids
    site_settings.stripe_testing_product_id = stripe_settings["test_product_id"]
    site_settings.stripe_testing_webhook_secret = stripe_settings["test_webhook_key"]
    site_settings.stripe_testing_api_secret_key = stripe_settings["test_secret_key"]
    site_settings.stripe_product_id = stripe_settings["live_product_id"]
    site_settings.stripe_webhook_secret = stripe_settings["live_webhook_key"]
    site_settings.stripe_api_secret_key = stripe_settings["live_secret_key"]
    # set footer link
    site_settings.privacy_policy_link = "https://github.com/diffractive/newstream"

    site_settings.save()

    print("Loaded settings √")

def load_test_users():
    """ Load test users for setting up some test donations/subscriptions
    """
    for item in test_users:
        if User.objects.filter(email=item["email"]).exists():
            continue
        user = User.objects.create_user(email=item["email"], password=item["password"])
        user.first_name = item["first_name"]
        user.last_name = item["last_name"]
        user.save()
        loaded_users[item["email"]] = user
        # save donor email as verified and primary
        email_obj = EmailAddress(email=item["email"], verified=True, primary=True, user=user)
        email_obj.save()

    print("Loaded test users √")

def load_test_donations():
    """ Load test donations/subscriptions
    """
    # load payment gateway, donation form
    form = DonationForm.objects.get(title="Main Form")
    # 2nd object is PayPal, 3rd is Stripe
    gateways = PaymentGateway.objects.all().order_by("list_order")
    gateway_map = {
        "paypal": gateways[1],
        "stripe": gateways[2]
    }

    for item in test_donations:
        if Donation.objects.filter(transaction_id=item["transaction_id"]).exists():
            continue
        donation = Donation(
            transaction_id=item["transaction_id"],
            user=loaded_users[item["user_email"]],
            form=form,
            gateway=gateway_map[item["gateway"]],
            is_recurring=item["is_recurring"],
            donation_amount=item["donation_amount"],
            currency=item["currency"],
            guest_email=item["guest_email"],
            guest_name=item["guest_name"],
            payment_status=item["payment_status"],
            donation_date=make_aware(item["donation_date"]),
        )
        donation.save()

    print("Loaded test donations √")

    for item in test_subscriptions:
        if Subscription.objects.filter(profile_id=item["profile_id"]).exists():
            continue
        subscription = Subscription(
            profile_id=item["profile_id"],
            user=loaded_users[item["user_email"]],
            gateway=gateway_map[item["gateway"]],
            recurring_amount=item["recurring_amount"],
            currency=item["currency"],
            recurring_status=item["recurring_status"],
            subscribe_date=make_aware(item["subscribe_date"])
        )
        subscription.save()

        counter = 0
        for transaction_id in item["donation_transaction_ids"]:
            if Donation.objects.filter(transaction_id=transaction_id).exists():
                continue
            sub_date = item["subscribe_date"]
            donation_date = datetime(sub_date.year + int((sub_date.month + counter) / 12), (sub_date.month + counter) % 12, sub_date.day)
            donation = Donation(
                transaction_id=transaction_id,
                subscription=subscription,
                user=loaded_users[item["user_email"]],
                form=form,
                gateway=gateway_map[item["gateway"]],
                is_recurring=True,
                donation_amount=item["recurring_amount"],
                currency=item["currency"],
                guest_email="",
                guest_name="",
                payment_status=STATUS_COMPLETE,
                donation_date=make_aware(donation_date),
            )
            donation.save()

            counter += 1

    print("Loaded test subscriptions √")


def load_localstripe_create_product():
    auth = requests.auth.HTTPBasicAuth(stripe_settings["test_secret_key"], '')
    post_data = {
        "name": "Newstream Product",
        "id": stripe_settings["test_product_id"]
    }
    requests.post(settings.STRIPE_API_BASE + '/v1/products', auth=auth, json=post_data)

    print("Localstripe product created √")


def load_localstripe_webhooks():
    post_data = {
        "url": 'http://app.newstream.local:8000/en/donations/verify-stripe-response/',
        "secret": stripe_settings["test_webhook_key"],
        "events": [
            EVENT_CHECKOUT_SESSION_COMPLETED,
            EVENT_PAYMENT_INTENT_SUCCEEDED,
            EVENT_INVOICE_CREATED,
            EVENT_INVOICE_PAID,
            EVENT_CUSTOMER_SUBSCRIPTION_UPDATED,
            EVENT_CUSTOMER_SUBSCRIPTION_DELETED
        ]
    }

    requests.post(settings.STRIPE_API_BASE + '/_config/webhooks/newstream', json=post_data)

    print("Localstripe webhooks registered √")
