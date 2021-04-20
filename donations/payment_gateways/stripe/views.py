import stripe
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from newstream.classes import WebhookNotProcessedError
from newstream.functions import getSiteSettings, uuid4_str, getFullReverseUrl, _exception, object_to_json
from donations.models import Donation, DonationPaymentMeta
from donations.payment_gateways.setting_classes import getStripeSettings
from donations.payment_gateways.stripe.functions import initStripeApiKey, formatDonationAmount
from donations.payment_gateways.stripe.factory import Factory_Stripe


@csrf_exempt
def create_checkout_session(request):
    errorObj = {
        "issue": "Exception",
        "description": ""
    }
    try:
        initStripeApiKey(request)
        stripeSettings = getStripeSettings(request)
        siteSettings = getSiteSettings(request)

        donation_id = request.session.pop('donation_id', None)
        if not donation_id:
            raise ValueError(_("No donation_id in session"))

        # might throw DoesNotExist error
        donation = Donation.objects.get(pk=donation_id)

        # init session_kwargs with common parameters
        session_kwargs = {
            'payment_method_types': ['card'],
            'metadata': {
                'donation_id': donation.id
            },
            'success_url': getFullReverseUrl(
                    request, 'donations:return-from-stripe')+'?stripe_session_id={CHECKOUT_SESSION_ID}',
            'cancel_url': getFullReverseUrl(
                    request, 'donations:cancel-from-stripe')+'?stripe_session_id={CHECKOUT_SESSION_ID}',
            'idempotency_key': uuid4_str()
        }

        # try to get existing stripe customer
        donor_email = donation.user.email if donation.user else donation.guest_email
        customers = stripe.Customer.list(email=donor_email, limit=1)
        if len(customers['data']) > 0:
            session_kwargs['customer'] = customers['data'][0]['id']
        else:
            session_kwargs['customer_email'] = donor_email

        # Product should have been created by admin manually at the dashboard
        # todo: make sure the product_id in site_settings has been set by some kind of configuration enforcement before site is launched
        # stripe.error.InvalidRequestError would be raised if the product_id is either not found or empty/None
        product = stripe.Product.retrieve(stripeSettings.product_id)

        # ad-hoc price is used
        amount_str = formatDonationAmount(
            donation.donation_amount, donation.currency)
        adhoc_price = {
            'unit_amount_decimal': amount_str,
            'currency': donation.currency.lower(),
            'product': product.id
        }
        if donation.is_recurring:
            adhoc_price['recurring'] = {
                'interval': 'month',
                'interval_count': 1
            }
        session_kwargs['line_items'] = [{
            'price_data': adhoc_price,
            'quantity': 1,
        }]

        # set session mode
        session_mode = 'payment'
        if donation.is_recurring:
            session_mode = 'subscription'
        session_kwargs['mode'] = session_mode

        # set metadata
        if donation.is_recurring:
            session_kwargs['subscription_data'] = {
                'metadata': {
                    'donation_id': donation.id
                }
            }
        else:
            session_kwargs['payment_intent_data'] = {
                'metadata': {
                    'donation_id': donation.id
                }
            }

        session = stripe.checkout.Session.create(**session_kwargs)

        # save payment_intent id for recognition purposes when receiving the payment_intent.succeeded webhook for onetime donations
        if session.payment_intent:
            dpm = DonationPaymentMeta(donation=donation, field_key='stripe_payment_intent_id', field_value=session.payment_intent)
            dpm.save()

        return JsonResponse({'id': session.id})
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
    except (stripe.error.RateLimitError, stripe.error.InvalidRequestError, stripe.error.AuthenticationError, stripe.error.APIConnectionError, stripe.error.StripeError) as e:
        _exception("Stripe API Error({}): Status({}), Code({}), Param({}), Message({})".format(type(e).__name__, e.http_status, e.code, e.param, e.user_message))
        errorObj['issue'] = type(e).__name__
        errorObj['description'] = 'Message is: %s' % e.user_message
        return JsonResponse(object_to_json(errorObj), status=int(e.http_status))
    except Exception as e:
        errorObj['description'] = str(e)
        _exception(errorObj["description"])
        return JsonResponse(object_to_json(errorObj), status=500)


@csrf_exempt
def verify_stripe_response(request):
    try:
        # Set up gateway manager object with its linking donation, session, etc...
        gatewayManager = Factory_Stripe.initGatewayByVerification(request)

        return gatewayManager.process_webhook_response()
    except WebhookNotProcessedError as error:
        # beware: this exception should be reserved for the incoming but not processed webhook events, or events processed but data not needed further action
        _exception(str(error))
        # return 200 for attaining a higher rate of successful response rate at Stripe backend
        return HttpResponse(status=200)
    except ValueError as e:
        # Might be invalid payload from initGatewayByVerification
        # or missing donation_id/subscription_id or donation object not found
        _exception(str(e))
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature from initGatewayByVerification
        _exception(str(e))
        return HttpResponse(status=400)
    except (stripe.error.RateLimitError, stripe.error.InvalidRequestError, stripe.error.AuthenticationError, stripe.error.APIConnectionError, stripe.error.StripeError) as e:
        _exception("Stripe API Error({}): Status({}), Code({}), Param({}), Message({})".format(type(e).__name__, e.http_status, e.code, e.param, e.user_message))
        return HttpResponse(status=int(e.http_status))
    except Exception as e:
        _exception(str(e))
        return HttpResponse(status=500)


@csrf_exempt
def return_from_stripe(request):
    try:
        gatewayManager = Factory_Stripe.initGatewayByReturn(request)
        request.session['return-donation-id'] = gatewayManager.donation.id
    except ValueError as e:
        _exception(str(e))
        request.session['error-title'] = str(_("ValueError"))
        request.session['error-message'] = str(e)
    except (stripe.error.RateLimitError, stripe.error.InvalidRequestError, stripe.error.AuthenticationError, stripe.error.APIConnectionError, stripe.error.StripeError) as e:
        _exception("Stripe API Error({}): Status({}), Code({}), Param({}), Message({})".format(type(e).__name__, e.http_status, e.code, e.param, e.user_message))
        request.session['error-title'] = type(e).__name__
        request.session['error-message'] = e.user_message
    except Exception as e:
        _exception(str(e))
        request.session['error-title'] = str(_("Unknown Exception"))
        request.session['error-message'] = str(_(
            "Results returned from gateway is invalid."))
    return redirect('donations:thank-you')


@csrf_exempt
def cancel_from_stripe(request):
    try:
        gatewayManager = Factory_Stripe.initGatewayByReturn(request)
        request.session['return-donation-id'] = gatewayManager.donation.id

        if gatewayManager.session:
            if gatewayManager.session.mode == 'payment':
                stripe.PaymentIntent.cancel(
                    gatewayManager.session.payment_intent)
            # for subscription mode, payment_intent is not yet created, so no need to cancel
    except ValueError as e:
        _exception(str(e))
        request.session['error-title'] = str(_("ValueError"))
        request.session['error-message'] = str(e)
    except (stripe.error.RateLimitError, stripe.error.InvalidRequestError, stripe.error.AuthenticationError, stripe.error.APIConnectionError, stripe.error.StripeError) as e:
        _exception("Stripe API Error({}): Status({}), Code({}), Param({}), Message({})".format(type(e).__name__, e.http_status, e.code, e.param, e.user_message))
        request.session['error-title'] = type(e).__name__
        request.session['error-message'] = e.user_message
    except Exception as e:
        _exception(str(e))
        request.session['error-title'] = str(_("Unknown Error"))
        request.session['error-message'] = str(_(
            "Results returned from gateway is invalid."))
    return redirect('donations:cancelled')
