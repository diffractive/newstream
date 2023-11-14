from types import SimpleNamespace
import stripe
import requests
import json
import pytest
from unittest.mock import patch
from datetime import datetime
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.utils.timezone import make_aware, now
from django.conf import settings
from donations.models import Donation, Subscription, SubscriptionInstance, STATUS_ACTIVE, STATUS_COMPLETE, STATUS_PAYMENT_FAILED
from site_settings.models import PaymentGateway
from donations.payment_gateways.paypal.constants import *
from donations.payment_gateways.stripe.constants import *
from pprint import pformat, pprint

PAYPAL_WEBHOOK_URL = 'http://app.newstream.local:8000/en/donations/verify-paypal-response/'
STRIPE_WEBHOOK_URL = 'http://app.newstream.local:8000/en/donations/verify-stripe-response/'

User = get_user_model()

TEST_USER = {
    "email": "david.donor@diffractive.io",
    "password": "david.donor",
    "first_name": "David",
    "last_name": "Donor"
}

TEST_STRIPE_SUBSCRIPTION = {
    "profile_id": "sub_1Mxo8cTTD2mrB42B414bD7LS",
    "recurring_amount": 250,
    "currency": "HKD",
    "gateway": "stripe",
    "recurring_status": STATUS_ACTIVE,
    "subscribe_date": datetime.strptime("2023-02-05", '%Y-%m-%d'),
}

TEST_PAYPAL_SUBSCRIPTION = {
    "profile_id": "I-CHKSDMCHNA",
    "recurring_amount": 250,
    "currency": "HKD",
    "gateway": "paypal",
    "recurring_status": STATUS_ACTIVE,
    "subscribe_date": datetime.strptime("2023-02-05", '%Y-%m-%d'),
}

# https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
ERRORS = [
    # Covers all types of stripe errors
    {"type": "stripe", "error": stripe.error.InvalidRequestError("Test Error", "", 403)},

    # This covers DNS errors
    {"type": "connection", "error": requests.exceptions.ConnectionError('Test Error')},

    # SSL Issues
    {"type": "ssl", "error": requests.exceptions.SSLError('Test Error')},

    # Timeouts
    {"type": "timeout", "error": requests.exceptions.Timeout('Test Error')},

    # Http errors
    {"type": "http", "error": requests.exceptions.HTTPError('Test Error')}
]

TEST_DOMAIN_NAME = "newstream.hongkongfp.com"
TEST_USER_CREDS = {'username':TEST_USER['email'], 'password':TEST_USER['password']}

# Create your tests here.
@pytest.mark.django_db
class MockStripeResponses(TestCase):
    """
    These tests will mock a stripe response to see how the code handles mocked responses
    """
    def setUp(self):
        """
        Create a user and a subscription to be manipulated. Also login to perform authed api functions
        """

        # Create test user
        self.user = User.objects.create_user(email=TEST_USER['email'], password=TEST_USER['password'])
        self.user.first_name = TEST_USER['first_name']
        self.user.last_name = TEST_USER['last_name']
        self.user.save()

        gateways = PaymentGateway.objects.all().order_by("list_order")
        gateway_map = {
            "paypal": gateways[1],
            "stripe": gateways[2]
        }

        parent = Subscription(
            user=self.user,
            created_by=self.user,
        )
        parent.save()

        self.subscription = SubscriptionInstance(
            profile_id=TEST_STRIPE_SUBSCRIPTION["profile_id"],
            user=self.user,
            parent=parent,
            gateway=gateway_map[TEST_STRIPE_SUBSCRIPTION["gateway"]],
            recurring_amount=TEST_STRIPE_SUBSCRIPTION["recurring_amount"],
            currency=TEST_STRIPE_SUBSCRIPTION["currency"],
            recurring_status=TEST_STRIPE_SUBSCRIPTION["recurring_status"],
            subscribe_date=make_aware(TEST_STRIPE_SUBSCRIPTION["subscribe_date"])
        )
        self.subscription.save()

        self.client = Client(SERVER_NAME=TEST_DOMAIN_NAME)
        # logins user
        self.client.login(**TEST_USER_CREDS)

        settings.STRIPE_WEBHOOK_IGNORABLE_RESOURCES = 'I-IRRELEVANT'


    @patch('stripe.Subscription.modify')
    def test_pause_subscription_errors(self, modify_mock):
        data = {"subscription_id": self.subscription.id}

        for error in ERRORS:
            modify_mock.side_effect = error['error']
            res = self.client.post(reverse('donations:toggle-recurring'), data=data, content_type='application/json').json()
            if error['type'] == "stripe":
                self.assertEqual(res['reason'],
                    'There has been an error connecting with Stripe: Test Error, subscription id: {}'.format(self.subscription.profile_id))
            else:
                self.assertEqual(res['reason'], 'Test Error')
            self.assertEqual(res['status'], 'failure')

    @patch('stripe.Subscription.delete')
    def test_cancel_subscription_errors(self, delete_mock):
        data = {"subscription_id": self.subscription.id}

        for error in ERRORS:
            delete_mock.side_effect = error['error']
            res = self.client.post(reverse('donations:cancel-recurring'), data=data, content_type='application/json').json()
            if error['type'] == "stripe":
                self.assertEqual(res['reason'],
                    'There has been an error connecting with Stripe: Test Error, subscription id: {}'.format(self.subscription.profile_id))
            else:
                self.assertEqual(res['reason'], 'Test Error')
            self.assertEqual(res['status'], 'failure')

    @patch('stripe.SubscriptionItem.list')
    @patch('stripe.SubscriptionItem.modify')
    def test_update_subscription_amount(self, modify_mock, list_mock):
        data = {'recurring_amount': ['200.00']}

        # We want to return dot notation values https://stackoverflow.com/a/16279578
        mock_dict = {"id": "test_id"}
        mock_obj = SimpleNamespace(**mock_dict)
        mock_res = {"data": [mock_obj]}

        for error in ERRORS:
            # Test SubscriptionItem.list errors
            list_mock.side_effect = error['error']
            res = self.client.post(
                reverse('donations:edit-recurring', kwargs={'id': self.subscription.id}),
                data = data, follow=True)
            messages = list(get_messages(res.wsgi_request))
            self.assertEqual(len(messages), 1)
            if error['type'] == "stripe":
                self.assertEqual(messages[0].message,
                    'There has been an error connecting with Stripe: Test Error, subscription id: {}'.format(self.subscription.profile_id))
            else:
                self.assertEqual(messages[0].message, 'Test Error')

            # Test SubscriptionItem.modify errors
            list_mock.side_effect = None
            # We want list to return a value that will get us through the checks and run
            # the modify function
            list_mock.return_value = mock_res
            modify_mock.side_effect = error['error']
            res = self.client.post(
                reverse('donations:edit-recurring', kwargs={'id': self.subscription.id}),
                data = data, follow=True)
            messages = list(get_messages(res.wsgi_request))
            if error['type'] == "stripe":
                self.assertEqual(messages[0].message,
                    'There has been an error connecting with Stripe: Test Error, subscription id: {}'.format(self.subscription.profile_id))
            else:
                self.assertEqual(messages[0].message, 'Test Error')

    @patch('stripe.Subscription.modify')
    def test_update_billing_cycle(self, modify_mock):
        data = {'recurring_amount': [self.subscription.recurring_amount], 'billing_cycle_now': ['on']}

        for error in ERRORS:
            modify_mock.side_effect = error['error']
            res = self.client.post(
                reverse('donations:edit-recurring', kwargs={'id': self.subscription.id}),
                data = data, follow=True)
            messages = list(get_messages(res.wsgi_request))
            self.assertEqual(len(messages), 1)
            if error['type'] == "stripe":
                self.assertEqual(messages[0].message,
                    'There has been an error connecting with Stripe: Test Error, subscription id: {}'.format(self.subscription.profile_id))
            else:
                self.assertEqual(messages[0].message, 'Test Error')

    @patch('stripe.Subscription.retrieve')
    @patch('stripe.Webhook.construct_event')
    def test_webhook_missing_donation_id(self, constructed_event, mock_subscription):
        constructed_event.return_value = {
            "type": EVENT_CHECKOUT_SESSION_COMPLETED,
            "data": {
                "object": type('',(object,),{
                    "mode": "subscription",
                    "subscription": self.subscription.profile_id
                })()
            }
        }
        mock_subscription.return_value = type('',(object,),{
            "id": self.subscription.profile_id,
            "metadata": {
                "test_key": "test_value"
            }
        })()
        headers = {
            "HTTP_STRIPE_SIGNATURE": "test",
        }
        # testing EVENT_CHECKOUT_SESSION_COMPLETED event without 'donation_id' in resource body
        res = self.client.post(STRIPE_WEBHOOK_URL, {}, content_type="application/json", follow=True, **headers)
        self.assertEqual(res.reason_phrase, "Missing donation_id in subscription_obj.metadata, subscription id: {}".format(self.subscription.profile_id))

        # testing other subscription related events without 'donation_id' in resource metadata
        # plus subscription id not found in Newstream
        # First, make up a sub id not found on Newstream
        mock_sub_id = "I-NOTFOUND"
        constructed_event.return_value["data"]["object"] = type('',(object,),{
            "subscription": mock_sub_id,
        })()
        mock_subscription.return_value = type('',(object,),{
            "id": mock_sub_id,
            "metadata": {
                "test_key": "test_value"
            }
        })()
        # Then loop over the five events for this error scenario
        for evt in [EVENT_INVOICE_CREATED, EVENT_INVOICE_PAID, EVENT_INVOICE_PAYMENT_FAILED, EVENT_CUSTOMER_SUBSCRIPTION_UPDATED, EVENT_CUSTOMER_SUBSCRIPTION_DELETED]:
            constructed_event.return_value["type"] = evt
            if evt in [EVENT_CUSTOMER_SUBSCRIPTION_UPDATED, EVENT_CUSTOMER_SUBSCRIPTION_DELETED]:
                constructed_event.return_value["data"]["object"] = type('',(object,),{
                    "id": mock_sub_id,
                    "metadata": {
                        "test_key": "test_value"
                    }
                })()
            res = self.client.post(STRIPE_WEBHOOK_URL, {}, content_type="application/json", follow=True, **headers)
            self.assertEqual(res.reason_phrase, "No matching SubscriptionInstance found, subscription id: {}".format(mock_sub_id))

    @patch('stripe.Subscription.retrieve')
    @patch('stripe.Webhook.construct_event')
    def test_webhook_with_ignored_resources(self, constructed_event, mock_subscription):
        mock_sub_id = "I-IRRELEVANT"
        constructed_event.return_value = {
            "type": EVENT_CHECKOUT_SESSION_COMPLETED,
            "data": {
                "object": type('',(object,),{
                    "mode": "subscription",
                    "subscription": mock_sub_id
                })()
            }
        }
        mock_subscription.return_value = type('',(object,),{
            "id": mock_sub_id,
            "metadata": {
                "test_key": "test_value"
            }
        })()
        headers = {
            "HTTP_STRIPE_SIGNATURE": "test",
        }
        # testing EVENT_CHECKOUT_SESSION_COMPLETED event without 'donation_id' in resource body
        res = self.client.post(STRIPE_WEBHOOK_URL, {}, content_type="application/json", follow=True, **headers)
        self.assertEqual(res.reason_phrase, "Missing donation_id in subscription_obj.metadata, but subscription id: {} is in list of STRIPE_WEBHOOK_IGNORABLE_RESOURCES".format(mock_sub_id))

        # testing other subscription related events without 'donation_id' in resource metadata
        # plus subscription id not found in Newstream
        # First, make up a sub id not found on Newstream
        constructed_event.return_value["data"]["object"] = type('',(object,),{
            "subscription": mock_sub_id,
        })()
        mock_subscription.return_value = type('',(object,),{
            "id": mock_sub_id,
            "metadata": {
                "test_key": "test_value"
            }
        })()
        # Then loop over the five events for this error scenario
        for evt in [EVENT_INVOICE_CREATED, EVENT_INVOICE_PAID, EVENT_INVOICE_PAYMENT_FAILED, EVENT_CUSTOMER_SUBSCRIPTION_UPDATED, EVENT_CUSTOMER_SUBSCRIPTION_DELETED]:
            constructed_event.return_value["type"] = evt
            if evt in [EVENT_CUSTOMER_SUBSCRIPTION_UPDATED, EVENT_CUSTOMER_SUBSCRIPTION_DELETED]:
                constructed_event.return_value["data"]["object"] = type('',(object,),{
                    "id": mock_sub_id,
                    "metadata": {
                        "test_key": "test_value"
                    }
                })()
            res = self.client.post(STRIPE_WEBHOOK_URL, {}, content_type="application/json", follow=True, **headers)
            self.assertEqual(res.reason_phrase, "No matching SubscriptionInstance found, but subscription id: {} is in list of STRIPE_WEBHOOK_IGNORABLE_RESOURCES".format(mock_sub_id))


@pytest.mark.django_db
class MockPaypalResponses(TestCase):
    """
    These tests will mock a paypal response to see how the code handles mocked responses
    """
    def setUp(self):
        """
        Create a user and a subscription to be manipulated. Also login to perform authed api functions
        """

        # Create test user
        self.user = User.objects.create_user(email=TEST_USER['email'], password=TEST_USER['password'])
        self.user.first_name = TEST_USER['first_name']
        self.user.last_name = TEST_USER['last_name']
        self.user.save()

        gateways = PaymentGateway.objects.all().order_by("list_order")
        gateway_map = {
            "paypal": gateways[1],
            "stripe": gateways[2]
        }

        parent = Subscription(
            user=self.user,
            created_by=self.user,
        )
        parent.save()

        self.subscription = SubscriptionInstance(
            profile_id=TEST_PAYPAL_SUBSCRIPTION["profile_id"],
            parent=parent,
            user=self.user,
            gateway=gateway_map[TEST_PAYPAL_SUBSCRIPTION["gateway"]],
            recurring_amount=TEST_PAYPAL_SUBSCRIPTION["recurring_amount"],
            currency=TEST_PAYPAL_SUBSCRIPTION["currency"],
            recurring_status=TEST_PAYPAL_SUBSCRIPTION["recurring_status"],
            subscribe_date=make_aware(TEST_PAYPAL_SUBSCRIPTION["subscribe_date"])
        )
        self.subscription.save()

        self.donation = Donation(
            transaction_id='test_id',
            user=self.user,
            gateway=gateway_map[TEST_PAYPAL_SUBSCRIPTION["gateway"]],
            is_recurring=True,
            donation_amount=10,
            currency='HKD',
            payment_status=STATUS_COMPLETE,
            subscription=self.subscription,
            donation_date=now()
        )
        self.donation.save()

        # We have 2 donations to simulate the webhook coming from the new donation
        self.donation2 = Donation(
            transaction_id='test_id_2',
            user=self.user,
            gateway=gateway_map[TEST_PAYPAL_SUBSCRIPTION["gateway"]],
            is_recurring=True,
            donation_amount=10,
            currency='HKD',
            payment_status=STATUS_COMPLETE,
            subscription=self.subscription,
            donation_date=now()
        )
        self.donation2.save()

        self.client = Client(SERVER_NAME=TEST_DOMAIN_NAME)
        # logins user
        self.client.login(**TEST_USER_CREDS)

        settings.NEWSTREAM_ADMIN_EMAILS = 'admin@diffractive.io'
        settings.PAYPAL_WEBHOOK_IGNORABLE_RESOURCES = 'I-IRRELEVANT'

    @patch('donations.payment_gateways.paypal.factory.verifyWebhook')
    def test_fail_payment(self, verify_mock):
        verify_mock.return_value = { "verification_status": "SUCCESS" }

        headers = {
            "HTTP_Paypal-Transmission-Id": "test",
            "HTTP_Paypal-Transmission-Time": "test",
            "HTTP_Paypal-Transmission-Sig": "test",
            "HTTP_Paypal-Cert-Url": "test",
            "HTTP_PayPal-Auth-Algo": "test",
        }
        # We only use these fields from the webhook response
        json_data = {
            "event_type": "BILLING.SUBSCRIPTION.PAYMENT.FAILED",
            "resource": {
                "custom_id": self.donation.id,
                "id": self.subscription.profile_id,
                "status": "ACTIVE"
            }
        }
        self.client.post(PAYPAL_WEBHOOK_URL, json.dumps(json_data), content_type="application/json", follow=True, **headers)

        sub = SubscriptionInstance.objects.get(profile_id=self.subscription.profile_id)

        self.assertEqual(sub.recurring_status, STATUS_PAYMENT_FAILED)

    @patch('donations.payment_gateways.paypal.factory.getSubscriptionDetails')
    @patch('donations.payment_gateways.paypal.factory.verifyWebhook')
    def test_reinstate_subscription(self, verify_mock, details_mock):
        verify_mock.return_value = { "verification_status": "SUCCESS" }
        details_mock.return_value = {
            "custom_id": self.donation2.id,
            "id": self.subscription.profile_id,
            "status": "ACTIVE"
        }

        sub = SubscriptionInstance.objects.get(profile_id=self.subscription.profile_id)
        sub.recurring_status = STATUS_PAYMENT_FAILED
        sub.save()

        headers = {
            "HTTP_Paypal-Transmission-Id": "test",
            "HTTP_Paypal-Transmission-Time": "test",
            "HTTP_Paypal-Transmission-Sig": "test",
            "HTTP_Paypal-Cert-Url": "test",
            "HTTP_PayPal-Auth-Algo": "test",
        }
        # We only use these fields from the webhook response
        json_data = {
            "event_type": 'PAYMENT.SALE.COMPLETED',
            "resource": {
                'state': 'completed',
                "billing_agreement_id": self.subscription.profile_id,
                "id": self.subscription.profile_id,
                "custom_id": self.donation2.id,
                'amount': {
                    "total": 10,
                    "currency": "HKD",
                }
            }
        }
        self.client.post(PAYPAL_WEBHOOK_URL, json.dumps(json_data), content_type="application/json", follow=True, **headers)

        sub = SubscriptionInstance.objects.get(profile_id=self.subscription.profile_id)
        self.assertEqual(sub.recurring_status, STATUS_ACTIVE)

    @patch('donations.payment_gateways.paypal.factory.getSubscriptionDetails')
    @patch('donations.payment_gateways.paypal.factory.verifyWebhook')
    def test_webhook_missing_custom_id(self, verify_mock, details_mock):
        verify_mock.return_value = { "verification_status": "SUCCESS" }
        details_mock.return_value = {
            "id": self.subscription.profile_id,
            "status": "ACTIVE"
        }

        headers = {
            "HTTP_Paypal-Transmission-Id": "test",
            "HTTP_Paypal-Transmission-Time": "test",
            "HTTP_Paypal-Transmission-Sig": "test",
            "HTTP_Paypal-Cert-Url": "test",
            "HTTP_PayPal-Auth-Algo": "test",
        }
        # providing the minimum required attributes for mocking the scenarios
        json_data_1 = {
            "event_type": EVENT_PAYMENT_SALE_COMPLETED,
            "resource": {
                "billing_agreement_id": self.subscription.profile_id,
            }
        }
        json_data_2 = {
            "event_type": EVENT_BILLING_SUBSCRIPTION_ACTIVATED,
            "resource": {
                "id": self.subscription.profile_id,
            }
        }

        # testing EVENT_PAYMENT_SALE_COMPLETED event without 'custom_id' in resource body
        res = self.client.post(PAYPAL_WEBHOOK_URL, json.dumps(json_data_1), content_type="application/json", follow=True, **headers)
        self.assertEqual(res.reason_phrase, "Missing custom_id(donation_id) in json_data.resource, subscription id: {}".format(self.subscription.profile_id))

        # testing all other subscription related webhook events without 'custom_id'
        for evt in [EVENT_BILLING_SUBSCRIPTION_ACTIVATED, EVENT_BILLING_SUBSCRIPTION_UPDATED, EVENT_BILLING_SUBSCRIPTION_PAYMENT_FAILED, EVENT_BILLING_SUBSCRIPTION_CANCELLED, EVENT_BILLING_SUBSCRIPTION_SUSPENDED]:
            json_data_2["event_type"] = evt
            res = self.client.post(PAYPAL_WEBHOOK_URL, json.dumps(json_data_2), content_type="application/json", follow=True, **headers)
            self.assertEqual(res.reason_phrase, "Missing custom_id(donation_id) in json_data.resource, subscription id: {}".format(self.subscription.profile_id))

    @patch('donations.payment_gateways.paypal.factory.getSubscriptionDetails')
    @patch('donations.payment_gateways.paypal.factory.verifyWebhook')
    def test_webhook_with_ignored_resources(self, verify_mock, details_mock):
        mock_sub_id = "I-IRRELEVANT"
        verify_mock.return_value = { "verification_status": "SUCCESS" }
        details_mock.return_value = {
            "id": mock_sub_id,
            "status": "ACTIVE"
        }

        headers = {
            "HTTP_Paypal-Transmission-Id": "test",
            "HTTP_Paypal-Transmission-Time": "test",
            "HTTP_Paypal-Transmission-Sig": "test",
            "HTTP_Paypal-Cert-Url": "test",
            "HTTP_PayPal-Auth-Algo": "test",
        }
        # providing the minimum required attributes for mocking the scenarios
        json_data_1 = {
            "event_type": EVENT_PAYMENT_SALE_COMPLETED,
            "resource": {
                "billing_agreement_id": mock_sub_id,
            }
        }
        json_data_2 = {
            "event_type": EVENT_BILLING_SUBSCRIPTION_ACTIVATED,
            "resource": {
                "id": mock_sub_id,
            }
        }

        # testing EVENT_PAYMENT_SALE_COMPLETED event without 'custom_id' in resource body
        res = self.client.post(PAYPAL_WEBHOOK_URL, json.dumps(json_data_1), content_type="application/json", follow=True, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.reason_phrase, "Missing custom_id(donation_id) in json_data.resource, but subscription id: {} is in list of PAYPAL_WEBHOOK_IGNORABLE_RESOURCES".format(mock_sub_id))

        # testing all other subscription related webhook events without 'custom_id'
        for evt in [EVENT_BILLING_SUBSCRIPTION_ACTIVATED, EVENT_BILLING_SUBSCRIPTION_UPDATED, EVENT_BILLING_SUBSCRIPTION_PAYMENT_FAILED, EVENT_BILLING_SUBSCRIPTION_CANCELLED, EVENT_BILLING_SUBSCRIPTION_SUSPENDED]:
            json_data_2["event_type"] = evt
            res = self.client.post(PAYPAL_WEBHOOK_URL, json.dumps(json_data_2), content_type="application/json", follow=True, **headers)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.reason_phrase, "Missing custom_id(donation_id) in json_data.resource, but subscription id: {} is in list of PAYPAL_WEBHOOK_IGNORABLE_RESOURCES".format(mock_sub_id))
