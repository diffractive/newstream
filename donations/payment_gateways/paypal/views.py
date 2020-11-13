import stripe
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from paypalcheckoutsdk.core import PayPalHttpClient
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalhttp import HttpError

from newstream.functions import getSiteSettings, getSiteName, uuid4_str, getFullReverseUrl, printvars, object_to_json, _debug, _error, _exception
from donations.models import Donation, DonationPaymentMeta, STATUS_COMPLETE, STATUS_PROCESSING
from donations.functions import gen_order_id
from donations.email_functions import sendDonationNotifToAdmins, sendDonationReceiptToDonor
from donations.payment_gateways.setting_classes import getPayPalSettings
from donations.payment_gateways import Factory_Paypal
from .functions import capture_paypal_order


def build_onetime_request_body(request):
    """Method to create body with CAPTURE intent"""
    donation_id = request.session.get('donation_id', None)
    if not donation_id:
        raise ValueError(_("Missing donation_id in session"))
    try:
        donation = Donation.objects.get(pk=int(donation_id))
    except Donation.DoesNotExist:
        raise ValueError(_("Donation object not found by id: ")+str(donation_id))
    # returl_url or cancel_url params in application_context tested to be only useful if order not initiated by Javascript APK
    return \
    {
        "intent": "CAPTURE",
        "application_context": {
            "brand_name": getSiteName(request),
            "landing_page": "NO_PREFERENCE",
            "shipping_preference": "NO_SHIPPING",
            "user_action": "PAY_NOW",
            "return_url": getFullReverseUrl(request, 'donations:return-from-paypal'),
            "cancel_url": getFullReverseUrl(request, 'donations:cancel-from-paypal')
        },
        "purchase_units": [
            {
                "description": getSiteName(request) + str(_(" Onetime Donation")),
                "custom_id": donation_id,
                "amount": {
                    "currency_code": donation.currency,
                    "value": str(donation.donation_amount)
                }
            }
        ]
    }


@csrf_exempt
def create_paypal_transaction(request):
    errorObj = {
        "issue": "Exception",
        "description": ""
    }
    try:
        paypalSettings = getPayPalSettings(request)
        client = PayPalHttpClient(paypalSettings.environment)

        req = OrdersCreateRequest()
        # The following line is for mocking negative responses
        # req.headers['PayPal-Mock-Response'] = '{"mock_application_codes":"INTERNAL_SERVER_ERROR"}'
        req.prefer('return=representation')
        req.request_body(build_onetime_request_body(request))
        response = client.execute(req)
        _debug('PayPal: Order Created Status: '+response.result.status)
        # set approval_link attribute
        for link in response.result.links:
            _debug('PayPal: --- {}: {} ---'.format(link.rel, link.href))
            if link.rel == 'approve':
                response.result.approval_link = link.href
    except ValueError as e:
        _exception(str(e))
        errorObj['issue'] = "Donation.DoesNotExist"
        errorObj['description'] = str(e)
        return JsonResponse(object_to_json(errorObj), status=500)
    except HttpError as ioe:
        # Catching exceptions from the paypalclient execution, HttpError is a subclass of IOError
        httpError = json.loads(ioe.message)
        if 'details' in httpError and len(httpError['details']) > 0:
            errorObj["issue"] = httpError['details'][0]['issue']
            errorObj["description"] = httpError['details'][0]['description']
            _exception(errorObj["description"])
        return JsonResponse(object_to_json(errorObj), status=ioe.status_code)
    except Exception as error:
        errorObj['description'] = str(error)
        _exception(errorObj["description"])
        return JsonResponse(object_to_json(errorObj), status=500)
    return JsonResponse(object_to_json(response.result))


@csrf_exempt
def verify_paypal_response(request):
    try:
        # Set up gateway manager object with its linking donation, session, etc...
        gatewayManager = Factory_Paypal.initGatewayByVerification(request)

        if gatewayManager:
            _debug('PayPal Webhook Passed.')
            # print('Paypal webhook passed thru', flush=True)
            return gatewayManager.process_webhook_response()
    except ValueError as error:
        _exception(str(error))
        return HttpResponse(status=500)
    except Exception as error:
        _exception(str(error))
        return HttpResponse(status=500)
        
    # return fine for now, only testing purposes
    return HttpResponse(status=200)


@csrf_exempt
def return_from_paypal(request):
    try:
        gatewayManager = Factory_Paypal.initGatewayByReturn(request)
        request.session['return-donation-id'] = gatewayManager.donation.id
        # further capture payment if detected order approved, if not just set payment as processing and leave it to webhook processing
        if gatewayManager.order_status == 'APPROVED':
            # might raise IOError/HttpError
            capture_status = capture_paypal_order(request, gatewayManager.order_id)
            if capture_status == 'COMPLETED':
                _debug('PayPal: Order Captured. Payment Completed.')
                gatewayManager.donation.payment_status = STATUS_COMPLETE
                gatewayManager.donation.save()
                # send email notifs
                sendDonationReceiptToDonor(request, gatewayManager.donation)
                sendDonationNotifToAdmins(request, gatewayManager.donation)
        else:
            _debug('PayPal: Order status after Paypal returns: '+gatewayManager.order_status)
            gatewayManager.donation.payment_status = STATUS_PROCESSING
            gatewayManager.donation.save()
    except IOError as error:
        request.session['error-title'] = str(_("IOError"))
        request.session['error-message'] = str(error)
        _exception(str(error))
    except ValueError as error:
        request.session['error-title'] = str(_("ValueError"))
        request.session['error-message'] = str(error)
        _exception(str(error))
    except Exception as error:
        request.session['error-title'] = str(_("Exception"))
        request.session['error-message'] = str(error)
        _exception(str(error))
    return redirect('donations:thank-you')


@csrf_exempt
def cancel_from_paypal(request):
    try:
        gatewayManager = Factory_Paypal.initGatewayByReturn(request)
        request.session['return-donation-id'] = gatewayManager.donation.id
        # might carry out further actions for donation cancellation
    except IOError as error:
        request.session['error-title'] = str(_("IOError"))
        request.session['error-message'] = str(error)
        _exception(str(error))
    except ValueError as error:
        request.session['error-title'] = str(_("ValueError"))
        request.session['error-message'] = str(error)
        _exception(str(error))
    except Exception as error:
        request.session['error-title'] = str(_("Exception"))
        request.session['error-message'] = str(error)
        _exception(str(error))
    return redirect('donations:cancelled')
