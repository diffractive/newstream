import json
import logging
logger = logging.getLogger('newstream')
from datetime import datetime, timezone
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from paypalhttp import HttpError

from newstream.classes import WebhookNotProcessedError, WebhookMissingDonationIdError
from newstream.functions import object_to_json, _debug, _exception
from donations.models import Donation, STATUS_COMPLETE, STATUS_FAILED, STATUS_PAYMENT_FAILED, SubscriptionInstance, SubscriptionPaymentMeta
from donations.functions import removeSubscriptionWarnings
from donations.email_functions import sendDonationNotifToAdmins, sendDonationReceiptToDonor
from donations.payment_gateways.setting_classes import getPayPalSettings
from donations.payment_gateways import Factory_Paypal
from donations.payment_gateways.paypal.functions import create_paypal_order, capture_paypal_order, listProducts, createProduct, createPlan, createSubscription


def create_paypal_transaction(request):
    """ When the user reaches last step after confirming the donation,
        user is redirected via gatewayManager.redirect_to_gateway_url(), which renders redirection_paypal.html

        This function calls to PayPal Api to create a PayPal subscription object or PayPal order(one-time donation),
        then this function returns the approval_link to frontend js and to redirect to PayPal's checkout page

        Sample (JSON) request: {
            'csrfmiddlewaretoken': 'LZSpOsb364pn9R3gEPXdw2nN3dBEi7RWtMCBeaCse2QawCFIndu93fD3yv9wy0ij'
        }

        @todo: revise error handling, avoid catching all exceptions at the end
    """

    errorObj = {
        "issue": "Exception",
        "description": ""
    }
    result = {}
    try:
        paypalSettings = getPayPalSettings()

        donation_id = request.session.pop('donation_id', None)
        if not donation_id:
            raise ValueError(_("Missing donation_id in session"))
        donation = Donation.objects.get(pk=int(donation_id))

        if donation.is_recurring:
            # Product should have been created by admin manually at the dashboard/setup wizard
            # if no product exists, create one here(double safety net)
            # todo: make sure the product_id in site_settings has been set by some kind of configuration enforcement before site is launched
            product_list = listProducts(request.session)
            product = None
            if len(product_list['products']) == 0:
                product = createProduct(request.session)
            else:
                # get the product, should aim at the product with the specific product id
                for prod in product_list['products']:
                    if prod['id'] == paypalSettings.product_id:
                        product = prod
            if product == None:
                raise ValueError(_('Cannot initialize/get the paypal product object'))
            # Create plan and subscription
            plan = createPlan(request.session, product['id'], donation)
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
    """ This endpoint should be set as the listening endpoint for the webhook set in PayPal's developer dashboard(within a REST API App)
        The verification of the incoming PayPal requests is done via Factory_Paypal.initGatewayByVerification(request)
        The webhook should be set with the following events only:
            Billing subscription activated
            Billing subscription cancelled
            Billing subscription updated
            Payment capture completed
            Payment sale completed

        For more info on how to build this webhook endpoint, refer to PayPal documentation:
        https://developer.paypal.com/docs/subscriptions/integrate/

        @todo: revise error handling, avoid catching all exceptions at the end
    """

    try:
        # Set up gateway manager object with its linking donation, session, etc...
        gatewayManager = Factory_Paypal.initGatewayByVerification(request)

        if gatewayManager:
            return gatewayManager.process_webhook_response()
        else:
            raise Exception(_('gatewayManager for paypal not initialized.'))
    except WebhookNotProcessedError as error:
        # beware: this exception should be reserved for the incoming but not processed webhook events
        logger.info(str(error))
        # return 200 to prevent resending of paypal server of those requests
        return HttpResponse(status=200, reason=str(error))
    except WebhookMissingDonationIdError as error:
        if error.subscription_id in settings.PAYPAL_WEBHOOK_IGNORABLE_RESOURCES.split(','):
            log = "{}, but subscription id: {} is in list of PAYPAL_WEBHOOK_IGNORABLE_RESOURCES".format(error.message, error.subscription_id)
            logger.info(log)
            return HttpResponse(status=200, reason=log)
        else:
            log = "{}, subscription id: {}".format(error.message, error.subscription_id)
            logger.exception(log, exc_info=True)
            return HttpResponse(status=500, reason=log)
    except ValueError as error:
        _exception(str(error))
        return HttpResponse(status=500)
    except Exception as error:
        _exception(str(error))
        return HttpResponse(status=500)


@csrf_exempt
def return_from_paypal(request):
    """ This endpoint is submitted as the return_url when creating the PayPal SubscriptionInstance/Order at create_paypal_transaction(request)
        This url should receive GET params: 'token' and 'subscription_id'(only recurring payments); 'ba_token' is not used
        In Factory_PayPal.initGatewayByReturn(request), we save the subscription_id/token into the donationPaymentMeta data upon a successful request;
        exception will be raised if the endpoint is reached but a previous meta value is found,
        this is done to prevent this endpoint being called unlimitedly

        @todo: revise error handling, avoid catching all exceptions at the end
    """

    try:
        gatewayManager = Factory_Paypal.initGatewayByReturn(request)
        request.session['return-donation-id'] = gatewayManager.donation.id
        # subscription donation updates are handled by webhooks
        # returning from paypal only needs to deal with onetime donations
        if not gatewayManager.donation.is_recurring:
            # further capture payment if detected order approved, if not just set payment as processing and leave it to webhook processing
            if gatewayManager.order_status == 'APPROVED':
                # might raise IOError/HttpError
                capture_response = capture_paypal_order(gatewayManager.donation, gatewayManager.order_id)
                if capture_response.status == 'COMPLETED':
                    _debug('PayPal: Order Captured. Payment Completed.')
                    gatewayManager.donation.payment_status = STATUS_COMPLETE
                    gatewayManager.donation.donation_date = datetime.now(timezone.utc)
                    gatewayManager.donation.transaction_id = capture_response.purchase_units[0].payments.captures[0].id
                    gatewayManager.donation.save()
            else:
                _debug('PayPal: Order status after Paypal returns: '+gatewayManager.order_status)
        else:
            # save the subscription_id as profile_id
            gatewayManager.donation.subscription.profile_id = request.GET.get('subscription_id')
            gatewayManager.donation.subscription.save()

            # Resolve any existing subscriptions
            removeSubscriptionWarnings(request.user)
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
    """ This endpoint is submitted as the cancel_url when creating the PayPal SubscriptionInstance/Order at create_paypal_transaction(request)
        This url should receive GET params: 'token' and 'subscription_id'(only recurring payments); 'ba_token' is not used
        In Factory_PayPal.initGatewayByReturn(request), we save the subscription_id/token into the donationPaymentMeta data upon a successful request;
        exception will be raised if the endpoint is reached but a previous meta value is found,
        this is done to prevent this endpoint being called unlimitedly, which would set the payment status as Cancelled each time

        @todo: revise error handling, avoid catching all exceptions at the end
    """

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


def return_from_paypal_card_update(request):
    """ This endpoint is submitted as the return_url in the updating the payment flow.
        This url should receive GET params: 'token' and 'subscription_id'(only recurring payments); 'ba_token' is not used
        In Factory_PayPal.initGatewayByReturn(request), we save the subscription_id/token into the donationPaymentMeta data upon a successful request;
        exception will be raised if the endpoint is reached but a previous meta value is found,
        this is done to prevent this endpoint being called unlimitedly

        @todo: revise error handling, avoid catching all exceptions at the end
    """
    try:
        gatewayManager = Factory_Paypal.initGatewayByReturn(request)
        if gatewayManager.donation.is_recurring:
            gatewayManager.donation.subscription.profile_id = request.GET.get('subscription_id')
            gatewayManager.donation.subscription.save()
            try:
                # We want to cancel the payment failed subscriptioninstance under this subscription
                # now that we have an active one
                parent = gatewayManager.donation.subscription.parent
                instance = SubscriptionInstance.objects.get(parent=parent, recurring_status=STATUS_PAYMENT_FAILED)

                # Save this flag for old subscription instance so that we don't send emails when we cancel the subscription
                spmeta = SubscriptionPaymentMeta(
                    subscription=instance, field_key='awaiting_cancelation', field_value=True)
                spmeta.save()

                old_gateway = Factory_Paypal.initGateway(request, None, instance)
                old_gateway.cancel_recurring_payment()
            except SubscriptionPaymentMeta.DoesNotExist:
                pass

            # Resolve any existing subscriptions
            removeSubscriptionWarnings(request.user)
        request.session['updated-card'] = 'True'
        request.session['return-donation-id'] = gatewayManager.donation.id
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
    return redirect('donations:my-recurring-donations')


@csrf_exempt
def cancel_from_paypal_card_update(request):
    """ This endpoint is submitted as the cancel_url in the updating the payment details flow for the PayPal
        SubscriptionInstance/Order at create_paypal_transaction(request)
        This url should receive GET params: 'token' and 'subscription_id'(only recurring payments); 'ba_token' is not used
        In Factory_PayPal.initGatewayByReturn(request), we save the subscription_id/token into the donationPaymentMeta data upon a successful request;
        exception will be raised if the endpoint is reached but a previous meta value is found,
        this is done to prevent this endpoint being called unlimitedly, which would set the payment status as Cancelled each time

        @todo: revise error handling, avoid catching all exceptions at the end
    """

    try:
        gatewayManager = Factory_Paypal.initGatewayByReturn(request)
        request.session['return-donation-id'] = gatewayManager.donation.id

        # Remove newly created donation and subscription
        donation = Donation.objects.get(
            pk=request.session['return-donation-id'])
        sub_instance = donation.subscription
        donation.delete()
        sub_instance.delete()
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
    return redirect('donations:my-recurring-donations')

