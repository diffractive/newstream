import json
from decimal import *
from http import HTTPStatus
from unittest import TestCase
# from django.test import TestCase
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import Client

from newstream.functions import printvars
from donations.models import Subscription
# from newstream.classes import PersistentSessionClient
User = get_user_model()

# tweak these settings for your tests
TEST_DOMAIN_NAME = "newstream.hongkongfp.com"
TEST_USER_CREDS = {'username':'paypal-tester', 'password':'odysseus'}
TEST_CURRENCY = 'HKD'
TEST_SUBSCRIPTION_ID = 0

class PayPalApiTests(TestCase):
    '''
    *default domain of tested server is "testserver"*
    *unittest.TestCase does not roll back any changed test data*
    *each test method in this class should be tested individually*

    To test the full donation flow:
    Route 1(Onetime-Donation): test_onetime_donation -> manually approve at approval_link -> back to thankyou page
    Route 2(Recurring-Donation): test_recurring_donation -> manually approve at approval_link -> back to thankyou page
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
            subs = Subscription.objects.order_by('-id').first()
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

    def common_donation_flow(self, form_data, assertStatus=HTTPStatus.OK):
        # check user logged in
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        # post donation form
        response = self.client.post('/en/donations/donation-details/', data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("Redirecting to Payment Gateway Page...", response.content.decode('utf-8'))
        # post paypal transaction
        response = self.client.post('/en/donations/create-paypal-transaction/')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, assertStatus)
        if assertStatus == HTTPStatus.OK:
            self.assertTrue(result['approval_link'])
            # for manual approval
            print(result['approval_link'], flush=True)
        else:
            print('Response Status Code: {}'.format(response.status_code), flush=True)
            print('Issue: {}'.format(result['issue']), flush=True)
            print('Description: {}'.format(result['description']), flush=True)

    def test_onetime_donation(self):
        self.common_donation_flow({'donation_amount': Decimal('10.00'), 'donation_frequency': 'onetime', 'payment_gateway': 2, 'currency': TEST_CURRENCY})

    def test_recurring_donation(self):
        self.common_donation_flow({'donation_amount': Decimal('20.00'), 'donation_frequency': 'monthly', 'payment_gateway': 2, 'currency': TEST_CURRENCY})

    def test_cancel_subscription(self):
        self.common_recurring_action('/en/donations/cancel-recurring/', {'subscription_id': TEST_SUBSCRIPTION_ID})

    def test_toggle_subscription(self):
        self.common_recurring_action('/en/donations/toggle-recurring/', {'subscription_id': TEST_SUBSCRIPTION_ID})

    def test_update_subscription(self):
        self.update_recurring({'recurring_amount': Decimal('22.00'), 'subscription_id': TEST_SUBSCRIPTION_ID, 'currency': TEST_CURRENCY})

    def test_onetime_donation_NT1(self):
        '''Negative Test: test failing paypalcheckoutsdk.orders.OrdersCreateRequest'''
        # most probably cannot test failing OrdersCaptureRequest using sessions since client and browser session should be different
        # example pairing1: INTERNAL_SERVER_ERROR with 500 as assertStatus
        # example pairing2: INVALID_CURRENCY_CODE with 422 as assertStatus
        # To modify the session and then save it, it must be stored in a variable first (because a new SessionStore is created every time this property is accessed)
        s = self.client.session
        s.update({
            "extra_test_headers": {'PayPal-Mock-Response': '{"mock_application_codes":"INVALID_CURRENCY_CODE"}'},
        })
        s.save()
        self.common_donation_flow({'donation_amount': Decimal('10.00'), 'donation_frequency': 'onetime', 'payment_gateway': 2, 'currency': TEST_CURRENCY}, assertStatus=422)

    def test_recurring_donation_NT1(self):
        '''Negative Test: test failing listProducts'''
        # get various test values here - https://developer.paypal.com/docs/subscriptions/testing/#test-values
        s = self.client.session
        s.update({
            "negtest_listProducts": "ERRCAT006",
        })
        s.save()
        self.common_donation_flow({'donation_amount': Decimal('10.00'), 'donation_frequency': 'monthly', 'payment_gateway': 2, 'currency': TEST_CURRENCY}, assertStatus=500)

    def test_recurring_donation_NT2(self):
        '''Negative Test: test failing createProduct'''
        # get various test values here - https://developer.paypal.com/docs/subscriptions/testing/#test-values
        s = self.client.session
        s.update({
            "negtest_createProduct": "ERRCAT001",
        })
        s.save()
        self.common_donation_flow({'donation_amount': Decimal('10.00'), 'donation_frequency': 'monthly', 'payment_gateway': 2, 'currency': TEST_CURRENCY}, assertStatus=500)

    def test_recurring_donation_NT3(self):
        '''Negative Test: test failing createPlan'''
        # get various test values here - https://developer.paypal.com/docs/subscriptions/testing/#test-values
        s = self.client.session
        s.update({
            "negtest_createPlan": "ERRSUB001",
        })
        s.save()
        self.common_donation_flow({'donation_amount': Decimal('10.00'), 'donation_frequency': 'monthly', 'payment_gateway': 2, 'currency': TEST_CURRENCY}, assertStatus=500)

    def test_recurring_donation_NT4(self):
        '''Negative Test: test failing createSubscription'''
        # get various test values here - https://developer.paypal.com/docs/subscriptions/testing/#test-values
        s = self.client.session
        s.update({
            "negtest_createSubscription": "ERRSUB032",
        })
        s.save()
        self.common_donation_flow({'donation_amount': Decimal('10.00'), 'donation_frequency': 'monthly', 'payment_gateway': 2, 'currency': TEST_CURRENCY}, assertStatus=500)

    def test_recurring_donation_NT5(self):
        '''Negative Test: test failing cancelSubscription'''
        # get various test values here - https://developer.paypal.com/docs/subscriptions/testing/#test-values
        s = self.client.session
        s.update({
            "negtest_cancelSubscription": "ERRSUB063",
        })
        s.save()
        self.common_recurring_action('/en/donations/cancel-recurring/', {'subscription_id': TEST_SUBSCRIPTION_ID}, assertStatus='failure')

    def test_recurring_donation_NT6(self):
        '''Negative Test: test failing activateSubscription'''
        # get various test values here - https://developer.paypal.com/docs/subscriptions/testing/#test-values
        s = self.client.session
        s.update({
            "negtest_activateSubscription": "ERRSUB066",
        })
        s.save()
        self.common_recurring_action('/en/donations/toggle-recurring/', {'subscription_id': TEST_SUBSCRIPTION_ID}, assertStatus='failure')

    def test_recurring_donation_NT7(self):
        '''Negative Test: test failing suspendSubscription'''
        # get various test values here - https://developer.paypal.com/docs/subscriptions/testing/#test-values
        s = self.client.session
        s.update({
            "negtest_suspendSubscription": "ERRSUB059",
        })
        s.save()
        self.common_recurring_action('/en/donations/toggle-recurring/', {'subscription_id': TEST_SUBSCRIPTION_ID}, assertStatus='failure')
    
    def test_recurring_donation_NT8(self):
        '''Negative Test: test failing updateSubscription'''
        # get various test values here - https://developer.paypal.com/docs/subscriptions/testing/#test-values
        s = self.client.session
        s.update({
            "negtest_updateSubscription": "ERRSUB047",
        })
        s.save()
        self.update_recurring({'recurring_amount': Decimal('22.00'), 'subscription_id': TEST_SUBSCRIPTION_ID, 'currency': TEST_CURRENCY}, assertStatus=HTTPStatus.OK)