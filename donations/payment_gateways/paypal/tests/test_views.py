import stripe
import json
from decimal import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from paypalcheckoutsdk.core import PayPalHttpClient
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalhttp import HttpError

from newstream.functions import getSiteSettings, getSiteName, uuid4_str, getFullReverseUrl, printvars, object_to_json, _debug, _error, _exception
from site_settings.models import PaymentGateway, GATEWAY_PAYPAL
from donations.models import Donation, DonationPaymentMeta,  STATUS_COMPLETE, STATUS_PROCESSING, STATUS_FAILED, STATUS_PENDING
from donations.functions import gen_order_id
from donations.email_functions import sendDonationNotifToAdmins, sendDonationReceiptToDonor
from donations.payment_gateways.setting_classes import getPayPalSettings
from donations.payment_gateways import Factory_Paypal
from donations.payment_gateways.paypal.functions import capture_paypal_order, checkAccessTokenExpiry, listProducts, createProduct, createPlan, createSubscription, cancelSubscription

User = get_user_model()

@csrf_exempt
def create_prod_during_transaction(request):
    errorObj = {
        "issue": "Exception",
        "description": ""
    }
    try:
        # assume product list is none
        product_dict = {
            "name": "Newstream Donations(Fake-1)",
            "description": "Newstream Donations(PayPal) (Fake-1)",
            "type": "SERVICE",
            "category": "BOOKS_PERIODICALS_AND_NEWSPAPERS"
        }
        json_data = createProduct(request, product_dict=product_dict)
        _debug(json_data)
    except Exception as error:
        errorObj['description'] = str(error)
        _exception(errorObj["description"])
        return JsonResponse(object_to_json(errorObj), status=500)
    return JsonResponse(object_to_json(json_data))


@csrf_exempt
def get_prod_during_transaction(request):
    errorObj = {
        "issue": "Exception",
        "description": ""
    }
    paypalSettings = getPayPalSettings(request)
    try:
        product_list = listProducts(request)
        product = None
        if len(product_list['products']) == 0:
            raise ValueError(_('No Product found.'))
        else:
            # get the product, should aim at the product with the specific product id
            for prod in product_list['products']:
                if prod['id'] == paypalSettings.product_id:
                    product = prod
        if product == None:
            raise ValueError(_('Cannot initialize/get the paypal product object'))
    except Exception as error:
        errorObj['description'] = str(error)
        _exception(errorObj["description"])
        return JsonResponse(object_to_json(errorObj), status=500)
    return JsonResponse(object_to_json(product))


@csrf_exempt
def create_subscription_during_transaction(request):
    errorObj = {
        "issue": "Exception",
        "description": ""
    }
    result = {}
    paypalSettings = getPayPalSettings(request)
    try:
        product_list = listProducts(request)
        product = None
        if len(product_list['products']) == 0:
            raise ValueError(_('No Product found.'))
        else:
            # get the product, should aim at the product with the specific product id
            for prod in product_list['products']:
                if prod['id'] == paypalSettings.product_id:
                    product = prod
        if product == None:
            raise ValueError(_('Cannot initialize/get the paypal product object'))
        # create plan from dummy donation, need a username called 'paypal-tester'
        donation = Donation(
            order_number=uuid4_str(),
            user=User.objects.get(username='paypal-tester'),
            form=None,
            gateway=PaymentGateway.objects.get(title=GATEWAY_PAYPAL),
            is_recurring=True,
            donation_amount=Decimal('9.81'),
            currency='HKD',
            payment_status=STATUS_PENDING,
        )
        plan = createPlan(request, product['id'], donation)
        if plan['status'] == 'ACTIVE':
            subscription = createSubscription(request, plan['id'], donation, is_test=True)
            print(subscription)
            result['subscription_id'] = subscription['id']
            for link in subscription['links']:
                if link['rel'] == 'approve':
                    result['approval_link'] = link['href']
        else:
            raise ValueError(_("Newly created PayPal plan is not active, status: %(status)s") % {'status': plan['status']})
    except Exception as error:
        errorObj['description'] = str(error)
        _exception(errorObj["description"])
        return JsonResponse(object_to_json(errorObj), status=500)
    return JsonResponse(object_to_json(result))


@csrf_exempt
def cancel_subscription(request, subscription_id):
    errorObj = {
        "issue": "Exception",
        "description": ""
    }
    result = {}
    paypalSettings = getPayPalSettings(request)
    try:
        result = cancelSubscription(request, subscription_id)
    except Exception as error:
        errorObj['description'] = str(error)
        _exception(errorObj["description"])
        return JsonResponse(object_to_json(errorObj), status=500)
    return JsonResponse(object_to_json(result))
