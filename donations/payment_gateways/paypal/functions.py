import json
import time
import pycurl
import certifi
from io import BytesIO
from django.utils.translation import gettext_lazy as _
from paypalcheckoutsdk.core import PayPalHttpClient
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalhttp import HttpError

from donations.models import STATUS_FAILED
from donations.payment_gateways.setting_classes import getPayPalSettings
from donations.email_functions import sendDonationErrorNotifToAdmins
from newstream.functions import getSiteName, getFullReverseUrl, printvars, uuid4_str, _debug, _error

def common_headers(request):
    return ['Content-Type: application/json', 'Authorization: Bearer %s' % (request.session['paypal_token']), 'PayPal-Request-Id: %s' % (uuid4_str())]

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
        c.setopt(c.POST, 1)
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
        raise RuntimeError("curlPaypal request unsuccessful. Status Code: {}, Full body: {}".format(status_code, body.decode('utf-8')))
    # print("Curl to PayPal status code: {}({})".format(status_code, type(status_code)))
    # Here we deserialize the json into a python object
    return json.loads(body.decode('utf-8'))


def saveNewAccessToken(request, token_url, client_id, secret_key):
    json_data = curlPaypal(token_url, ['Accept: application/json', 'Accept-Language: en_US'], userpwd='%s:%s' % (client_id, secret_key), post_data='grant_type=client_credentials')
    if 'access_token' in json_data:
        request.session['paypal_token'] = json_data['access_token']
    else:
        raise RuntimeError(str(_("Cannot get 'access_token' attribute from paypal response.")))
    if 'expires_in' in json_data:
        # deduct 10 seconds from the expiry as buffer
        current_time = round(time.time()) - 10
        request.session['paypal_token_expiry'] = current_time + int(json_data['expires_in'])
    else:
        raise RuntimeError(str(_("Cannot get access_token's 'expires_in' attribute from paypal response.")))


def checkAccessTokenExpiry(request):
    paypalSettings = getPayPalSettings(request)
    token_uri = '/v1/oauth2/token'
    # check if the paypal_token_expiry stored in session has passed or not
    current_time = round(time.time())
    if 'paypal_token_expiry' not in request.session or current_time > request.session['paypal_token_expiry']:
        saveNewAccessToken(request, paypalSettings.api_url+token_uri, paypalSettings.client_id, paypalSettings.secret_key)


def listProducts(request):
    checkAccessTokenExpiry(request)
    paypalSettings = getPayPalSettings(request)
    api_url = paypalSettings.api_url+'/v1/catalogs/products?page_size=20'
    return curlPaypal(api_url, common_headers(request))


def createProduct(request, product_dict={}):
    checkAccessTokenExpiry(request)
    paypalSettings = getPayPalSettings(request)
    api_url = paypalSettings.api_url+'/v1/catalogs/products'
    if not product_dict:
        product_dict = {
            "name": "Newstream Donations",
            "description": "Newstream Donations(PayPal)",
            "type": "SERVICE",
            "category": "BOOKS_PERIODICALS_AND_NEWSPAPERS"
        }
    return curlPaypal(api_url, common_headers(request), post_data=json.dumps(product_dict))


def createPlan(request, product_id, donation):
    checkAccessTokenExpiry(request)
    paypalSettings = getPayPalSettings(request)
    api_url = paypalSettings.api_url+'/v1/billing/plans'
    plan_dict = {
        "product_id": product_id,
        "name": "Newstream Donation Plan for %s" % (donation.user.fullname),
        "description": "Newstream Donation Plan for %s" % (donation.user.fullname),
        "status": "ACTIVE",
        "billing_cycles": [
            {
                "frequency": {
                    "interval_unit": "MONTH",
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
    # uncomment below to test 'doom to fail' scenario - https://developer.paypal.com/docs/subscriptions/testing/#create-plan
    # plan_dict['name'] = 'ERRSUB001'
    return curlPaypal(api_url, common_headers(request), post_data=json.dumps(plan_dict))


def getUserGivenName(user):
    if user.first_name:
        return user.first_name
    else:
        return user.email.split('@')[0]


def createSubscription(request, plan_id, donation, is_test=False):
    checkAccessTokenExpiry(request)
    paypalSettings = getPayPalSettings(request)
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
            "brand_name": getSiteName(request),
            "locale": "en-US",
            "shipping_preference": "NO_SHIPPING",
            "user_action": "SUBSCRIBE_NOW",
            "payment_method": {
                "payer_selected": "PAYPAL",
                "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
            },
            "return_url": getFullReverseUrl(request, 'donations:return-from-paypal') if not is_test else 'http://example.com/return/',
            "cancel_url": getFullReverseUrl(request, 'donations:cancel-from-paypal') if not is_test else 'http://example.com/cancel/'
        },
        "custom_id": str(donation.id)
    }
    # uncomment below to test 'doom to fail' scenario - https://developer.paypal.com/docs/subscriptions/testing/#create-plan
    # subscription_dict['plan_id'] = 'ERRSUB033'
    api_url = paypalSettings.api_url+'/v1/billing/subscriptions'
    return curlPaypal(api_url, common_headers(request), post_data=json.dumps(subscription_dict))


def getSubscriptionDetails(request, subscription_id):
    checkAccessTokenExpiry(request)
    paypalSettings = getPayPalSettings(request)
    api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}'.format(subscription_id)
    return curlPaypal(api_url, common_headers(request))


def cancelSubscription(request, subscription_id):
    '''paypal returns 404 if the subscription has not passed the approval stage'''
    checkAccessTokenExpiry(request)
    paypalSettings = getPayPalSettings(request)
    api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}/cancel'.format(subscription_id)
    return curlPaypal(api_url, common_headers(request), verb='POST')


def activateSubscription(request, subscription_id):
    checkAccessTokenExpiry(request)
    paypalSettings = getPayPalSettings(request)
    api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}/activate'.format(subscription_id)
    return curlPaypal(api_url, common_headers(request), verb='POST')


def suspendSubscription(request, subscription_id):
    checkAccessTokenExpiry(request)
    paypalSettings = getPayPalSettings(request)
    api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}/suspend'.format(subscription_id)
    return curlPaypal(api_url, common_headers(request), verb='POST')


def updateSubscription(request, subscription_id, new_amount, currency):
    checkAccessTokenExpiry(request)
    paypalSettings = getPayPalSettings(request)
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
    return curlPaypal(api_url, common_headers(request), post_data=json.dumps(patch_body), verb='PATCH')


def cancelSubscription(request, subscription_id):
    checkAccessTokenExpiry(request)
    paypalSettings = getPayPalSettings(request)
    api_url = paypalSettings.api_url+'/v1/billing/subscriptions/{}/cancel'.format(subscription_id)
    return curlPaypal(api_url, common_headers(request), verb='POST')


def process_capture_failure(request, donation, issue, description):
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
    sendDonationErrorNotifToAdmins(request, donation, issue, description)
    # filter error message for display
    if issue in group_customer_support:
        description += str(_(' Please call PayPal Customer Support for more details.'))
    return "{}: {}".format(issue, description)


def capture_paypal_order(request, donation, order_id):
    """Method to capture order using order_id"""
    paypalSettings = getPayPalSettings(request)
    client = PayPalHttpClient(paypalSettings.environment)

    req = OrdersCaptureRequest(order_id)
    # The following line is for mocking negative responses
    # req.headers['PayPal-Mock-Response'] = '{"mock_application_codes":"MAX_NUMBER_OF_PAYMENT_ATTEMPTS_EXCEEDED"}'
    _debug('PayPal: Capture Order')
    try:
        response = client.execute(req)
    except IOError as ioe:
        fail_reason = str(ioe)
        if isinstance(ioe, HttpError):
            # Something went wrong server-side
            httpError = json.loads(ioe.message)
            if 'details' in httpError and len(httpError['details']) > 0:
                fail_reason = process_capture_failure(request, donation, httpError['details'][0]['issue'], httpError['details'][0]['description'])
        # update donation status to failed
        donation.payment_status = STATUS_FAILED
        donation.save()
        raise IOError(fail_reason)
    return response.result.status
