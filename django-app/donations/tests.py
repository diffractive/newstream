from types import SimpleNamespace
import stripe
import requests
from unittest.mock import patch
from datetime import datetime
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.utils.timezone import make_aware
from donations.models import Subscription, SubscriptionInstance, STATUS_ACTIVE
from site_settings.models import PaymentGateway


User = get_user_model()

TEST_USER = {
    "email": "david.donor@diffractive.io",
    "password": "david.donor",
    "first_name": "David",
    "last_name": "Donor"
}

TEST_SUBSCRIPTION = {
    "profile_id": "sub_1Mxo8cTTD2mrB42B414bD7LS",
    "recurring_amount": 250,
    "currency": "HKD",
    "gateway": "stripe",
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
            profile_id=TEST_SUBSCRIPTION["profile_id"],
            parent=parent,
            user=self.user,
            gateway=gateway_map[TEST_SUBSCRIPTION["gateway"]],
            recurring_amount=TEST_SUBSCRIPTION["recurring_amount"],
            currency=TEST_SUBSCRIPTION["currency"],
            recurring_status=TEST_SUBSCRIPTION["recurring_status"],
            subscribe_date=make_aware(TEST_SUBSCRIPTION["subscribe_date"])
        )
        self.subscription.save()

        self.client = Client(SERVER_NAME=TEST_DOMAIN_NAME)
        # logins user
        self.client.login(**TEST_USER_CREDS)


    @patch('stripe.Subscription.modify')
    def test_pause_subscription_errors(self, modify_mock):
        data = {"subscription_id": self.subscription.id}

        for error in ERRORS:
            modify_mock.side_effect = error['error']
            res = self.client.post(reverse('donations:toggle-recurring'), data=data, content_type='application/json').json()
            if error['type'] == "stripe":
                self.assertEqual(res['reason'],
                    'There has been an error connecting with Stripe: Test Error')
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
                    'There has been an error connecting with Stripe: Test Error')
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
                    'There has been an error connecting with Stripe: Test Error')
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
                    'There has been an error connecting with Stripe: Test Error')
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
                    'There has been an error connecting with Stripe: Test Error')
            else:
                self.assertEqual(messages[0].message, 'Test Error')
