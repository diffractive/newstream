import json
import time
import pycurl
import certifi
from io import BytesIO
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from paypalcheckoutsdk.core import PayPalHttpClient
from paypalcheckoutsdk.orders import OrdersCaptureRequest, OrdersCreateRequest
from paypalhttp import HttpError

from donations.models import STATUS_FAILED, FREQ_DAILY, SubscriptionPaymentMeta
from donations.payment_gateways.setting_classes import getPayPalSettings
from donations.email_functions import sendDonationErrorNotifToAdmins
from newstream.functions import get_site_name, uuid4_str, _debug, printvars, _exception

def common_headers(paypal_token):
    return ['Content-Type: application/json', 'Authorization: Bearer %s' % (paypal_token), 'PayPal-Request-Id: %s' % (uuid4_str())]

def curlPaypal(url, headers, userpwd='', post_data='', verb='GET'):
    _debug('curlPaypal url: {}'.format(url))
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.HTTPHEADER, headers)
    if userpwd:
        c.setopt(c.USERPWD, userpwd)
    if post_data:
        c.setopt(c.POSTFIELDS, post_data)
    if verb == 'POST':
        c.setopt(c.CUSTOMREQUEST, 'POST')
    elif verb == 'PATCH':
        c.setopt(c.CUSTOMREQUEST, 'PATCH')
    c.setopt(c.VERBOSE, True)
    c.perform()
    status_code = c.getinfo(pycurl.HTTP_CODE)
    c.close()

    body = buffer.getvalue()
    # Body is a byte string.
    # We have to know the encoding in order to print it to a text file
    # such as standard output.
    if status_code == 204:
        _debug('curlPaypal returns 204')
        return {}
    if status_code >= 300:
        _exception("curlPaypal request unsuccessful. Status Code: {}, Full body: {}".format(status_code, body.decode('utf-8')))
        raise RuntimeError(_("There has been an error connecting with Paypal"))
    # print("Curl to PayPal status code: {}({})".format(status_code, type(status_code)))
    # Here we deserialize the json into a python object
    return json.loads(body.decode('utf-8'))


def saveNewAccessToken(session, token_url, client_id, secret_key):
    json_data = curlPaypal(token_url, ['Accept: application/json', 'Accept-Language: en_US'], userpwd='%s:%s' % (client_id, secret_key), post_data='grant_type=client_credentials')
    if 'access_token' in json_data:
        session['paypal_token'] = json_data['access_token']
    else:
        raise RuntimeError(str(_("Cannot get 'access_token' attribute from paypal response.")))
    if 'expires_in' in json_data:
        # deduct 10 seconds from the expiry as buffer
        current_time = round(time.time()) - 10
        session['paypal_token_expiry'] = current_time + int(json_data['expires_in'])
    else:
        raise RuntimeError(str(_("Cannot get access_token's 'expires_in' attribute from paypal response.")))


def checkAccessTokenExpiry(session):
    paypalSettings = getPayPalSettings()
    token_uri = '/v1/oauth2/token'
    # check if the paypal_token_expiry stored in session has passed or not
    current_time = round(time.time())
    if 'paypal_token_expiry' not in session or current_time > session['paypal_token_expiry']:
        saveNewAccessToken(session, paypalSettings.api_url+token_uri, paypalSettings.client_id, paypalSettings.secret_key)
    _debug("Paypal Auth Token: "+session['paypal_token'])


def listProducts(session):
    checkAccessTokenExpiry(session)
    paypalSettings = getPayPalSettings()
    api_url = paypalSettings.api_url+'/v1/catalogs/products?page_size=20'
    if paypalSettings.sandbox_mode and session.get('negtest_listProducts', None):
        api_url += '&total_required=' + session.get('negtest_listProducts')
    return curlPaypal(api_url, common_headers(session['paypal_token']))


def createProduct(session, product_dict={}):
    checkAccessTokenExpiry(session)
    paypalSettings = getPayPalSettings()
    api_url = paypalSettings.api_url+'/v1/catalogs/products'
    if not product_dict:
        product_dict = {
            "name": "Newstream Donations",
            "description": "Newstream Donations(PayPal)",
            "type": "SERVICE",
            "category": "BOOKS_PERIODICALS_AND_NEWSPAPERS"
        }
    if paypalSettings.sandbox_mode and session.get('negtest_createProduct', None):
        product_dict['name'] = session.get('negtest_createProduct')
    return curlPaypal(api_url, common_headers(session['paypal_token']), post_data=json.dumps(product_dict))


def createPlan(session, product_id, donation):
    checkAccessTokenExpiry(session)
    paypalSettings = getPayPalSettings()
    api_url = paypalSettings.api_url+'/v1/billing/plans'

    # see https://developer.paypal.com/docs/api/subscriptions/v1/#plans_create for frequency interval units
    if donation.subscription.recurring_frequency == FREQ_DAILY:
        interval_unit = "DAY"
    else:
        interval_unit = "MONTH"

    plan_dict = {
        "product_id": product_id,
        "name": "Newstream Donation Plan for %s" % (donation.user.display_fullname()),
        "description": "Newstream Donation Plan for %s" % (donation.user.display_fullname()),
        "status": "ACTIVE",
        "billing_cycles": [
            {
                "frequency": {
                    "interval_unit": interval_unit,
                    "interval_count": 1
                },
                "tenure_type": "REGULAR",
                "sequence": 1,
                "total_cycles": 0,
                "pricing_scheme": {
                    "fixed_price": {
                        "value": str(donation.donation_amount),
                        "currency_code": donation.currency
                    }
                }
            }
        ],
        "payment_preferences": {
            "auto_bill_outstanding": 'true',
            "payment_failure_threshold": 3
        }
    }
    if paypalSettings.sandbox_mode and session.get('negtest_createPlan', None):
        plan_dict['name'] = session.get('negtest_createPlan')
    return curlPaypal(api_url, common_headers(session['paypal_token']), post_data=json.dumps(plan_dict))


def getUserGivenName(user):
    if user.first_name:
        return user.first_name
    else:
        return user.email.split('@')[0]


def createSubscription(request, plan_id, donation):
    """ This function creates the PayPal Subscription via REST API
        param request   : django request obj, for getting session and building return urls
        param plan_id   : the id of the PayPal Plan object
        param donation  : newstream donation instance
    """
    checkAccessTokenExpiry(request.session)
    paypalSettings = getPayPalSettings()
    api_url = paypalSettings.api_url+'/v1/billing/subscriptions'
    return_url = request.build_absolute_uri(reverse('donations:return-from-paypal'))
    cancel_url = request.build_absolute_uri(reverse('donations:cancel-from-paypal'))
    try:
        # If we have the old_instance_id metadata we want to change the redirect url
        SubscriptionPaymentMeta.objects.get(subscription=donation.subscription, field_key='old_instance_id')
        return_url = request.build_absolute_uri(reverse('donations:return-from-paypal-card-update'))
        cancel_url = request.build_absolute_uri(reverse('donations:cancel-from-paypal-card-update'))
    except SubscriptionPaymentMeta.DoesNotExist:
        pass
    subscription_dict = {
        "plan_id": plan_id,
        "quantity": "1",
        "subscriber": {
            "name": {
                "given_name": getUserGivenName(donation.user),
                "surname": donation.user.last_name or ''
            },
            "email_address": donation.user.email
        },
        "application_context": {
            "brand_name": get_site_name(),
            "locale": "en-US",
            "shipping_preference": "NO_SHIPPING",
            "user_action": "SUBSCRIBE_NOW",
            "payment_method": {
                "payer_selected": "PAYPAL",
                "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
            },
            "return_url": return_url,
            "cancel_url": cancel_url
        },
        "custom_id": str(donation.id)
    }
    if paypalSettings.sandbox_mode and request.session.get('negtest_createSubscription', None):
        subscription_dict['plan_id'] = request.session.get('negtest_createSubscription')
    return curlPaypal(api_url, common_headers(request.session['paypal_token']), post_data=json.dumps(subscription_dict))


def getSubscriptionDetails(session, subscription_id):
    checkAccessTokenExpiry(session)
    paypalSettings = getPayPalSettings()
    api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}'.format(subscription_id)
    if paypalSettings.sandbox_mode and session.get('negtest_getSubscriptionDetails', None):
       api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}'.format(session.get('negtest_getSubscriptionDetails'))
    return curlPaypal(api_url, common_headers(session['paypal_token']))


def cancelSubscription(session, subscription_id):
    '''paypal returns 404 if the subscription has not passed the approval stage'''
    checkAccessTokenExpiry(session)
    paypalSettings = getPayPalSettings()
    api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}/cancel'.format(subscription_id)
    if paypalSettings.sandbox_mode and session.get('negtest_cancelSubscription', None):
       api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}/cancel'.format(session.get('negtest_cancelSubscription'))
    return curlPaypal(api_url, common_headers(session['paypal_token']), verb='POST')


def activateSubscription(session, subscription_id):
    checkAccessTokenExpiry(session)
    paypalSettings = getPayPalSettings()
    api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}/activate'.format(subscription_id)
    if paypalSettings.sandbox_mode and session.get('negtest_activateSubscription', None):
       api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}/activate'.format(session.get('negtest_activateSubscription'))
    return curlPaypal(api_url, common_headers(session['paypal_token']), verb='POST')


def suspendSubscription(session, subscription_id):
    checkAccessTokenExpiry(session)
    paypalSettings = getPayPalSettings()
    api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}/suspend'.format(subscription_id)
    if paypalSettings.sandbox_mode and session.get('negtest_suspendSubscription', None):
       api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}/suspend'.format(session.get('negtest_suspendSubscription'))
    return curlPaypal(api_url, common_headers(session['paypal_token']), verb='POST')


def updateSubscription(session, subscription_id, new_amount, currency):
    checkAccessTokenExpiry(session)
    paypalSettings = getPayPalSettings()
    api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}'.format(subscription_id)
    patch_body = [
        {
            "op": "replace",
            "path": "/plan/billing_cycles/@sequence==1/pricing_scheme/fixed_price",
            "value": {
                "currency_code": currency,
                "value": new_amount
            }
        }
    ]
    if paypalSettings.sandbox_mode and session.get('negtest_updateSubscription', None):
        api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}'.format(session.get('negtest_updateSubscription'))
    return curlPaypal(api_url, common_headers(session['paypal_token']), post_data=json.dumps(patch_body), verb='PATCH')


def process_capture_failure(donation, issue, description):
    """grouping according to each error description written on https://developer.paypal.com/docs/api/orders/v2/#errors"""
    group_customer_support = [
        'COMPLIANCE_VIOLATION',
        'MAX_NUMBER_OF_PAYMENT_ATTEMPTS_EXCEEDED',
        'PAYEE_ACCOUNT_LOCKED_OR_CLOSED',
        'PAYEE_ACCOUNT_RESTRICTED',
        'PAYER_ACCOUNT_LOCKED_OR_CLOSED',
        'PAYER_ACCOUNT_RESTRICTED',
        'TRANSACTION_AMOUNT_EXCEEDS_MONTHLY_MAX_LIMIT',
        'TRANSACTION_LIMIT_EXCEEDED',
        'TRANSACTION_RECEIVING_LIMIT_EXCEEDED'
    ]
    # send notification to admin
    sendDonationErrorNotifToAdmins(donation, issue, description)
    # filter error message for display
    if issue in group_customer_support:
        description += str(_(' Please call PayPal Customer Support for more details.'))
    return "{}: {}".format(issue, description)


def capture_paypal_order(donation, order_id):
    """Method to capture order using order_id"""
    paypalSettings = getPayPalSettings()
    client = PayPalHttpClient(paypalSettings.environment)

    req = OrdersCaptureRequest(order_id)
    _debug('PayPal: Capture Order')
    try:
        response = client.execute(req)
    except IOError as ioe:
        fail_reason = str(ioe)
        if isinstance(ioe, HttpError):
            # Something went wrong server-side
            httpError = json.loads(ioe.message)
            if 'details' in httpError and len(httpError['details']) > 0:
                fail_reason = process_capture_failure(donation, httpError['details'][0]['issue'], httpError['details'][0]['description'])
        # update donation status to failed
        donation.payment_status = STATUS_FAILED
        donation.save()
        raise IOError(fail_reason)
    return response.result


def build_onetime_request_body(request, donation):
    """ Method to create body with CAPTURE intent
        param   request: django request object, used for creating return urls
        param  donation: newstream donation instance
    """
    # returl_url or cancel_url params in application_context tested to be only useful if order not initiated by Javascript APK
    return \
    {
        "intent": "CAPTURE",
        "application_context": {
            "brand_name": get_site_name(),
            "landing_page": "NO_PREFERENCE",
            "shipping_preference": "NO_SHIPPING",
            "user_action": "PAY_NOW",
            "return_url": request.build_absolute_uri(reverse('donations:return-from-paypal')),
            "cancel_url": request.build_absolute_uri(reverse('donations:cancel-from-paypal'))
        },
        "purchase_units": [
            {
                "description": get_site_name() + str(_(" Onetime Donation")),
                "custom_id": donation.id,
                "amount": {
                    "currency_code": donation.currency,
                    "value": str(donation.donation_amount)
                }
            }
        ]
    }


def create_paypal_order(request, donation):
    paypalSettings = getPayPalSettings()
    client = PayPalHttpClient(paypalSettings.environment)

    req = OrdersCreateRequest()
    # set dictionary object in session['extra_test_headers'] in TestCases
    if request.session.get('extra_test_headers', None) and donation.is_test:
        for key, value in request.session.get('extra_test_headers').items():
            req.headers[key] = value
    req.prefer('return=representation')
    req.request_body(build_onetime_request_body(request, donation))
    return client.execute(req)
