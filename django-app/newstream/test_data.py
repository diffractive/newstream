import random, string, uuid, math
from django.conf import settings
from allauth.account.models import EmailAddress
from datetime import datetime
from django.contrib.auth import get_user_model
from django.conf import settings

from donations.models import DonationForm, Donation, Subscription, SubscriptionInstance, STATUS_COMPLETE, STATUS_ACTIVE, STATUS_CANCELLED
from site_settings.models import AdminEmails, SiteSettings, PaymentGateway
from django.utils.timezone import make_aware
from donations.payment_gateways.stripe.constants import (EVENT_CHECKOUT_SESSION_COMPLETED,
    EVENT_PAYMENT_INTENT_SUCCEEDED, EVENT_INVOICE_CREATED, EVENT_INVOICE_PAID,
    EVENT_CUSTOMER_SUBSCRIPTION_UPDATED, EVENT_CUSTOMER_SUBSCRIPTION_DELETED,
    EVENT_INVOICE_PAYMENT_FAILED)
from donations.payment_gateways.paypal.constants import (EVENT_PAYMENT_SALE_COMPLETED,
    EVENT_PAYMENT_CAPTURE_COMPLETED, EVENT_BILLING_SUBSCRIPTION_ACTIVATED,
    EVENT_BILLING_SUBSCRIPTION_CANCELLED, EVENT_BILLING_SUBSCRIPTION_UPDATED,
    EVENT_BILLING_SUBSCRIPTION_SUSPENDED, EVENT_BILLING_SUBSCRIPTION_PAYMENT_FAILED,
    EVENT_BILLING_PLAN_PRICING_CHANGE_ACTIVATED)
import requests

User = get_user_model()

def rand_alphanumeric(length):
    """ for generating donation/subscription identifiers
    """
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

# note that these test data should not appear on production environments
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
        "parent_uuid": uuid.UUID('ade64816-cd44-4c91-a26a-273af8a3f06b'),
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
    },
    {
        "parent_uuid": uuid.UUID('d21c4cc0-39b9-4990-8360-0859bbedc697'),
        "user_email": "david.donor@diffractive.io", # for matching up the right user
        "profile_id": "I-J23PB6KN3BC7",
        "recurring_amount": 500,
        "currency": "HKD",
        "gateway": "paypal",
        "recurring_status": STATUS_CANCELLED,
        "cancel_reason": SubscriptionInstance.CancelReason.BY_DONOR,
        "subscribe_date": datetime.strptime("2022-12-08", '%Y-%m-%d'),
        "donation_transaction_ids": [
            "9V798077EC622080D",
            "5VP98746NC241063R",
            "6AF881233D529931Y"
        ] # including 1st donation and subsequent renewals to be created
    },
    {
        "parent_uuid": uuid.UUID('d21c4cc0-39b9-4990-8360-0859bbedc697'),
        "user_email": "david.donor@diffractive.io", # for matching up the right user
        "profile_id": "I-N23EB6KN9BC2",
        "recurring_amount": 500,
        "currency": "HKD",
        "gateway": "paypal",
        "recurring_status": STATUS_ACTIVE,
        "subscribe_date": datetime.strptime("2023-03-08", '%Y-%m-%d'),
        "donation_transaction_ids": [
            "7OF881233D529932Q",
            "3XF881233D529432M"
        ] # including 1st donation and subsequent renewals to be created
    }
]

localstripe_settings = {
    "test_product_id": "prod_TEST_PRODUCT_ID",
    "test_webhook_key": "whsec_TEST_WEBHOOK_KEY",
    "test_secret_key": "sk_TEST_SECRET_KEY",
}

# for referencing when setting up donations/subscriptions
loaded_users = {}

def load_test_data(init=True):
    if init:
        load_settings()
    load_test_users()
    load_test_donations()
    if settings.INIT_LOCALSTRIPE:
        load_localstripe_webhooks()
        load_localstripe_create_product()
    if settings.PAYPAL_API_BASE:
        load_localpaypal_settings()
        load_localpaypal_webhooks()

def reset_test_data():
    remove_test_data()
    load_test_data(init=False)

def load_settings():
    """ Load necessary settings in order to let the app run smoothly e.g. sending emails ok
    """
    site_settings = SiteSettings.objects.get(pk=1)

    # set default from email address
    site_settings.default_from_email = settings.DEFAULT_FROM_EMAIL
    site_settings.default_from_name = 'Admin'

    # set default admin_emails list
    if settings.NEWSTREAM_ADMIN_EMAILS is not None:
        admin_emails = settings.NEWSTREAM_ADMIN_EMAILS.split(',')
        for admin_email in admin_emails:
            if AdminEmails.objects.filter(email=admin_email).exists():
                continue
            site_settings.admin_emails.add(AdminEmails(
                title="Admin",
                email=admin_email,
            ))

    # set footer link
    site_settings.privacy_policy_link = "https://github.com/diffractive/newstream"

    # enable daily subscriptions
    site_settings.allow_daily_subscription = True

    site_settings.save()

    print("Loaded settings √")

def load_test_users():
    """ Load test users for setting up some test donations/subscriptions
    """
    for item in test_users:
        user_qs = User.objects.filter(email=item["email"])
        if user_qs.count() == 1:
            loaded_users[item["email"]] = user_qs.first()
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
            created_at=make_aware(item["donation_date"]),
            updated_at=make_aware(item["donation_date"]),
        )
        donation.save()

    print("Loaded test donations √")

    for item in test_subscriptions:
        # create the parent first
        if not Subscription.objects.filter(uuid=item["parent_uuid"]).exists():
            subscription = Subscription(
                uuid=item["parent_uuid"],
                user=loaded_users[item["user_email"]],
                created_by=loaded_users[item["user_email"]],
                subscription_created_at=make_aware(item["subscribe_date"])
            )
            subscription.save()
        else:
            subscription = Subscription.objects.get(uuid=item["parent_uuid"])

        # then create the instance
        if SubscriptionInstance.objects.filter(profile_id=item["profile_id"]).exists():
            # update the Subscription parent to match with test_data
            # and delete the one created by data migration
            instance = SubscriptionInstance.objects.get(profile_id=item["profile_id"])
            if str(instance.parent_id) != str(item["parent_uuid"]):
                instance.parent.delete()
                instance.parent = subscription
                instance.save()
            continue
        instance = SubscriptionInstance(
            profile_id=item["profile_id"],
            user=loaded_users[item["user_email"]],
            gateway=gateway_map[item["gateway"]],
            parent=subscription,
            recurring_amount=item["recurring_amount"],
            currency=item["currency"],
            recurring_status=item["recurring_status"],
            cancel_reason=item["cancel_reason"] if "cancel_reason" in item else None,
            subscribe_date=make_aware(item["subscribe_date"]),
            created_at=make_aware(item["subscribe_date"]),
            updated_at=make_aware(item["subscribe_date"])
        )
        instance.save()

        for i, transaction_id in enumerate(item["donation_transaction_ids"]):
            if Donation.objects.filter(transaction_id=transaction_id).exists():
                continue
            sub_date = item["subscribe_date"]
            donation_date = datetime(sub_date.year + math.floor((sub_date.month + i - 1) / 12), ((sub_date.month + i - 1) % 12) + 1, sub_date.day)
            donation = Donation(
                transaction_id=transaction_id,
                subscription=instance,
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

    print("Loaded test subscriptions √")

def remove_test_data():
    remove_test_users()
    remove_test_donations()

def remove_test_users():
    for item in test_users:
        User.objects.filter(email=item["email"]).delete()
    print("Removed test users √")

def remove_test_donations():
    for item in test_donations:
        Donation.objects.filter(transaction_id=item["transaction_id"]).delete()
    print("Removed test donations √")

    for item in test_subscriptions:
        Donation.objects.filter(subscription__profile_id=item["profile_id"]).delete()
        SubscriptionInstance.objects.filter(profile_id=item["profile_id"]).delete()
        Subscription.objects.filter(uuid=item["parent_uuid"]).delete()
    print("Removed test subscriptions √")

def load_localstripe_create_product():
    auth = requests.auth.HTTPBasicAuth(localstripe_settings["test_secret_key"], '')
    res = requests.get(settings.STRIPE_API_BASE + '/v1/products/{}'.format(localstripe_settings["test_product_id"]), auth=auth)
    if res.status_code == 200:
        print("Localstripe product exists √")
    else:
        post_data = {
            "name": "Newstream Product",
            "id": localstripe_settings["test_product_id"]
        }
        requests.post(settings.STRIPE_API_BASE + '/v1/products', auth=auth, json=post_data)

        print("Localstripe product created √")


def load_localstripe_webhooks():
    post_data = {
        "url": 'http://app.newstream.local:8000/en/donations/verify-stripe-response/',
        "secret": localstripe_settings["test_webhook_key"],
        "events": [
            EVENT_CHECKOUT_SESSION_COMPLETED,
            EVENT_PAYMENT_INTENT_SUCCEEDED,
            EVENT_INVOICE_CREATED,
            EVENT_INVOICE_PAID,
            EVENT_INVOICE_PAYMENT_FAILED,
            EVENT_CUSTOMER_SUBSCRIPTION_UPDATED,
            EVENT_CUSTOMER_SUBSCRIPTION_DELETED
        ]
    }

    # There's no list webhooks api atm, but inspecting localstripe code, no duplicate webhooks will be created with the same id("newstream")
    requests.post(settings.STRIPE_API_BASE + '/_config/webhooks/newstream', json=post_data)

    print("Localstripe webhooks registered √")

def load_localpaypal_settings():
    site_settings = SiteSettings.objects.get(pk=1)
    # match paypal_sandbox_api_product_id with the created test product in localpaypal database
    site_settings.paypal_sandbox_api_product_id = "PROD-TESTINGID"
    site_settings.save()

    print("Localpaypal settings saved √")

def load_localpaypal_webhooks():
    post_data = {
        "url": 'http://app.newstream.local:8000/en/donations/verify-paypal-response/',
        "event_types": [
            EVENT_PAYMENT_SALE_COMPLETED,
            EVENT_PAYMENT_CAPTURE_COMPLETED,
            EVENT_BILLING_SUBSCRIPTION_ACTIVATED,
            EVENT_BILLING_SUBSCRIPTION_CANCELLED,
            EVENT_BILLING_SUBSCRIPTION_UPDATED,
            EVENT_BILLING_SUBSCRIPTION_SUSPENDED,
            EVENT_BILLING_SUBSCRIPTION_PAYMENT_FAILED,
            EVENT_BILLING_PLAN_PRICING_CHANGE_ACTIVATED,
        ]
    }

    # TODO: currently throws a duplicate key violation error from localpaypal if webhook already exist
    requests.post(settings.PAYPAL_API_BASE + '/config/webhooks', json=post_data)

    print("Localpaypal webhooks registered √")
