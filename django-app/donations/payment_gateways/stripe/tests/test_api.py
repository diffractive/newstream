import json
from decimal import *
from http import HTTPStatus
from unittest import TestCase
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import Client

from newstream.functions import printvars
from donations.models import Subscription
User = get_user_model()

# tweak these settings for your tests
TEST_DOMAIN_NAME = "newstream.hongkongfp.com"
USERNAME = 'stripe-tester'
USERPASS = 'odysseus'
TEST_USER_CREDS = {'username':USERNAME, 'password':USERPASS}
TEST_CURRENCY = 'HKD'
TEST_SUBSCRIPTION_ID = 0
FORM_GATEWAY_ID = 3

class StripeApiTests(TestCase):
    '''
    *default domain of tested server is "testserver"*
    *unittest.TestCase does not roll back any changed test data*
    *each test method in this class should be tested individually*
    *can't find negative testing in stripe's api like those in paypal*

    *currently cannot initiate donation flow in this testcase, the redirect action is performed by stripe's javascript sdk, which i have no control in here*
    To test the full donation flow:
    Route 1(Manual Onetime-Donation): manually submit form -> submit stripe payment form -> back to thankyou page
    Route 2(Manual Recurring-Donation): manually submit form -> submit stripe payment form -> back to thankyou page
        then(can-automate): test_toggle_subscription x2 -> test_update_subscription -> test_cancel_subscription
    todo: Route n (irregularites in form data)
    '''
    # client_class = PersistentSessionClient

    def setUp(self):
        self.client = Client(SERVER_NAME=TEST_DOMAIN_NAME)
        # logins user
        self.client.login(**TEST_USER_CREDS)
        # if TEST_SUBSCRIPTION is set larger than 0, this number would be used
        # else if it is 0, test would fetch the latest subscription object for testing
        global TEST_SUBSCRIPTION_ID
        if TEST_SUBSCRIPTION_ID == 0:
            user = User.objects.filter(username=USERNAME).first()
            subs = Subscription.objects.filter(user=user).order_by('-id').first()
            self.subscription = subs
            TEST_SUBSCRIPTION_ID = subs.id

    def update_recurring(self, form_data, assertStatus=302):
        # check user logged in
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        # post update donation form
        response = self.client.post('/en/donations/edit-recurring/{}/'.format(TEST_SUBSCRIPTION_ID), data=form_data)
        self.assertEqual(response.status_code, assertStatus)

    def common_recurring_action(self, url, dict_data, assertStatus='success'):
        # check user logged in
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        # post to action url
        response = self.client.post(url, dict_data, content_type="application/json")
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(result['status'], assertStatus)
        if assertStatus != 'success':
            print('Fail Reason: {}'.format(result['reason']), flush=True)

    def test_cancel_subscription(self):
        self.common_recurring_action('/en/donations/cancel-recurring/', {'subscription_id': TEST_SUBSCRIPTION_ID})

    def test_toggle_subscription(self):
        self.common_recurring_action('/en/donations/toggle-recurring/', {'subscription_id': TEST_SUBSCRIPTION_ID})

    def test_update_subscription(self):
        self.update_recurring({'recurring_amount': Decimal('25.00'), 'subscription_id': TEST_SUBSCRIPTION_ID, 'currency': TEST_CURRENCY, 'billing_cycle_now': True})

    def test_update_subscription_billnowonly(self):
        self.update_recurring({'recurring_amount': self.subscription.recurring_amount, 'subscription_id': TEST_SUBSCRIPTION_ID, 'currency': TEST_CURRENCY, 'billing_cycle_now': True})

    def test_update_subscription_amountonly(self):
        self.update_recurring({'recurring_amount': Decimal('23.00'), 'subscription_id': TEST_SUBSCRIPTION_ID, 'currency': TEST_CURRENCY, 'billing_cycle_now': False})
