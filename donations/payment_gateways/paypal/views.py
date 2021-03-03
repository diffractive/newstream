import json
from datetime import datetime, timezone
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from paypalhttp import HttpError

from newstream.classes import WebhookNotProcessedError
from newstream.functions import object_to_json, _debug, _exception
from donations.models import Donation, STATUS_COMPLETE, STATUS_FAILED
from donations.email_functions import sendDonationNotifToAdmins, sendDonationReceiptToDonor
from donations.payment_gateways.setting_classes import getPayPalSettings
from donations.payment_gateways import Factory_Paypal
from donations.payment_gateways.paypal.functions import create_paypal_order, capture_paypal_order, listProducts, createProduct, createPlan, createSubscription


@csrf_exempt
def create_paypal_transaction(request):
    errorObj = {
        "issue": "Exception",
        "description": ""
    }
    result = {}
    try:
        paypalSettings = getPayPalSettings(request)

        donation_id = request.session.get('donation_id', None)
        if not donation_id:
            raise ValueError(_("Missing donation_id in session"))
        donation = Donation.objects.get(pk=int(donation_id))

        if donation.is_recurring:
            # Product should have been created by admin manually at the dashboard/setup wizard
            # if no product exists, create one here(double safety net)
            # todo: make sure the product_id in site_settings has been set by some kind of configuration enforcement before site is launched
            product_list = listProducts(request)
            product = None
            if len(product_list['products']) == 0:
                product = createProduct(request)
            else:
                # get the product, should aim at the product with the specific product id
                for prod in product_list['products']:
                    if prod['id'] == paypalSettings.product_id:
                        product = prod
            if product == None:
                raise ValueError(_('Cannot initialize/get the paypal product object'))
            # Create plan and subscription
            plan = createPlan(request, product['id'], donation)
            if plan['status'] == 'ACTIVE':
                subscription = createSubscription(request, plan['id'], donation)
                result['subscription_id'] = subscription['id']
                for link in subscription['links']:
                    if link['rel'] == 'approve':
                        result['approval_link'] = link['href']
            else:
                raise ValueError(_("Newly created PayPal plan is not active, status: %(status)s") % {'status': plan['status']})
        # else: one-time donation
        else:
            response = create_paypal_order(request, donation)
            ppresult = response.result
            _debug('PayPal: Order Created Status: '+ppresult.status)
            # set approval_link attribute
            for link in ppresult.links:
                _debug('PayPal: --- {}: {} ---'.format(link.rel, link.href))
                if link.rel == 'approve':
                    result['approval_link'] = link.href
    except ValueError as e:
        _exception(str(e))
        errorObj['issue'] = "ValueError"
        errorObj['description'] = str(e)
        return JsonResponse(object_to_json(errorObj), status=500)
    except Donation.DoesNotExist:
        _exception("Donation.DoesNotExist")
        errorObj['issue'] = "Donation.DoesNotExist"
        errorObj['description'] = str(_("Donation object not found by id: %(id)s") % {'id': donation_id})
        return JsonResponse(object_to_json(errorObj), status=500)
    except HttpError as ioe:
        # Catching exceptions from the paypalclient execution, HttpError is a subclass of IOError
        httpError = json.loads(ioe.message)
        if 'details' in httpError and len(httpError['details']) > 0:
            errorObj["issue"] = httpError['details'][0]['issue']
            errorObj["description"] = httpError['details'][0]['description']
            _exception(errorObj["description"])
        # update donation status to failed
        donation.payment_status = STATUS_FAILED
        donation.save()
        return JsonResponse(object_to_json(errorObj), status=ioe.status_code)
    except Exception as error:
        errorObj['description'] = str(error)
        _exception(errorObj["description"])
        return JsonResponse(object_to_json(errorObj), status=500)
    return JsonResponse(object_to_json(result))


@csrf_exempt
def verify_paypal_response(request):
    try:
        # Set up gateway manager object with its linking donation, session, etc...
        gatewayManager = Factory_Paypal.initGatewayByVerification(request)

        if gatewayManager:
            return gatewayManager.process_webhook_response()
    except WebhookNotProcessedError as error:
        # beware: this exception should be reserved for the incoming but not processed webhook events
        _exception(str(error))
        # return 200 to prevent resending of paypal server of those requests
        return HttpResponse(status=200)
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
        # subscription donation updates are handled by webhooks
        # returning from paypal only needs to deal with onetime donations
        if not gatewayManager.donation.is_recurring:
            # further capture payment if detected order approved, if not just set payment as processing and leave it to webhook processing
            if gatewayManager.order_status == 'APPROVED':
                # might raise IOError/HttpError
                capture_status = capture_paypal_order(request, gatewayManager.donation, gatewayManager.order_id)
                if capture_status == 'COMPLETED':
                    _debug('PayPal: Order Captured. Payment Completed.')
                    gatewayManager.donation.payment_status = STATUS_COMPLETE
                    gatewayManager.donation.donation_date = datetime.now(timezone.utc)
                    gatewayManager.donation.save()
                    # send email notifs
                    sendDonationReceiptToDonor(request, gatewayManager.donation)
                    sendDonationNotifToAdmins(request, gatewayManager.donation)
            else:
                _debug('PayPal: Order status after Paypal returns: '+gatewayManager.order_status)
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
        # no need to carry out further actions for donation cancellation
        # 1. if it is a subscription, curlPaypal will fail to cancel it before any donor approval is given(resource not found error will be returned)
        # 2. there is no cancel-order endpoint for the Orders API
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
