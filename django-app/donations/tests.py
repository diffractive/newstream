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
from donations.models import Subscription, STATUS_ACTIVE
from site_settings.models import PaymentGateway


User = get_user_model()

test_user = {
    "email": "david.donor@diffractive.io",
    "password": "david.donor",
    "first_name": "David",
    "last_name": "Donor"
}

test_subscription = {
    "user_email": "david.donor@diffractive.io", # for matching up the right user
    "profile_id": "sub_1Mxo8cTTD2mrB42B414bD7LS",
    "recurring_amount": 250,
    "currency": "HKD",
    "gateway": "stripe",
    "recurring_status": STATUS_ACTIVE,
    "subscribe_date": datetime.strptime("2023-02-05", '%Y-%m-%d'),
}

# https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
errors = {
    # Covers all types of stripe errors
    "stripe_error": stripe.error.InvalidRequestError("Test Error", "", 403),

    # This covers DNS errors
    "connection_error": requests.exceptions.ConnectionError('Test Error'),

    # SSL Issues
    "ssl_error": requests.exceptions.SSLError('Test Error'),

    # Timeouts
    "timeout_error": requests.exceptions.Timeout('Test Error'),

    # Http errors
    "http_error": requests.exceptions.HTTPError('Test Error')

}

TEST_DOMAIN_NAME = "newstream.hongkongfp.com"
TEST_USER_CREDS = {'username':test_user['email'], 'password':test_user['password']}

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
        self.user = User.objects.create_user(email="david.donor@diffractive.io", password="david.donor")
        self.user.first_name = "David"
        self.user.last_name = "Donor"
        self.user.save()

        gateways = PaymentGateway.objects.all().order_by("list_order")
        gateway_map = {
            "paypal": gateways[1],
            "stripe": gateways[2]
        }

        self.subscription = Subscription(
            profile_id=test_subscription["profile_id"],
            user=self.user,
            gateway=gateway_map[test_subscription["gateway"]],
            recurring_amount=test_subscription["recurring_amount"],
            currency=test_subscription["currency"],
            recurring_status=test_subscription["recurring_status"],
            subscribe_date=make_aware(test_subscription["subscribe_date"])
        )
        self.subscription.save()

        self.client = Client(SERVER_NAME=TEST_DOMAIN_NAME)
        # logins user
        self.client.login(**TEST_USER_CREDS)


    @patch('stripe.Subscription.modify')
    def test_pause_subscription_errors(self, modify_mock):
        data = {"subscription_id": self.subscription.id}

        for key, val in errors.items():
            modify_mock.side_effect = val
            res = self.client.post(reverse('donations:toggle-recurring'), data=data, content_type='application/json').json()
            if key == "stripe_error":
                self.assertEqual(res['reason'],
                    'Stripe API Error(InvalidRequestError): Status(None), Code(403), Param(), Message(Test Error)')
            else:
                self.assertEqual(res['reason'], 'Test Error')
            self.assertEqual(res['status'], 'failure')

    @patch('stripe.Subscription.delete')
    def test_cancel_subscription_errors(self, delete_mock):
        data = {"subscription_id": self.subscription.id}

        for key, val in errors.items():
            delete_mock.side_effect = val
            res = self.client.post(reverse('donations:cancel-recurring'), data=data, content_type='application/json').json()
            if key == "stripe_error":
                self.assertEqual(res['reason'],
                    'Stripe API Error(InvalidRequestError): Status(None), Code(403), Param(), Message(Test Error)')
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

        for key, val in errors.items():
            # Test SubscriptionItem.list errors
            list_mock.side_effect = val
            res = self.client.post(
                reverse('donations:edit-recurring', kwargs={'id': self.subscription.id}),
                data = data, follow=True)
            messages = list(get_messages(res.wsgi_request))
            self.assertEqual(len(messages), 1)
            if key == "stripe_error":
                self.assertEqual(messages[0].message,
                    'Stripe API Error(InvalidRequestError): Status(None), Code(403), Param(), Message(Test Error)')
            else:
                self.assertEqual(messages[0].message, 'Test Error')

            # Test SubscriptionItem.modify errors
            list_mock.side_effect = None
            # We want list to return a value that will get us through the checks and run
            # the modify function
            list_mock.return_value = mock_res
            modify_mock.side_effect = val
            res = self.client.post(
                reverse('donations:edit-recurring', kwargs={'id': self.subscription.id}),
                data = data, follow=True)
            messages = list(get_messages(res.wsgi_request))
            if key == "stripe_error":
                self.assertEqual(messages[0].message,
                    'Stripe API Error(InvalidRequestError): Status(None), Code(403), Param(), Message(Test Error)')
            else:
                self.assertEqual(messages[0].message, 'Test Error')

    @patch('stripe.Subscription.modify')
    def test_update_billing_cycle(self, modify_mock):
        data = {'recurring_amount': [self.subscription.recurring_amount], 'billing_cycle_now': ['on']}

        for key, val in errors.items():
            modify_mock.side_effect = val
            res = self.client.post(
                reverse('donations:edit-recurring', kwargs={'id': self.subscription.id}),
                data = data, follow=True)
            messages = list(get_messages(res.wsgi_request))
            self.assertEqual(len(messages), 1)
            if key == "stripe_error":
                print(messages[0])
                self.assertEqual(messages[0].message,
                    'Stripe API Error(InvalidRequestError): Status(None), Code(403), Param(), Message(Test Error)')
            else:
                self.assertEqual(messages[0].message, 'Test Error')
