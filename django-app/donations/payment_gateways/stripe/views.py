import stripe
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction

from newstream.classes import WebhookNotProcessedError
from newstream.functions import uuid4_str, reverse_with_site_url, _exception, _debug, object_to_json
from donations.models import Donation, DonationPaymentMeta, SubscriptionPaymentMeta, SubscriptionInstance, STATUS_PAYMENT_FAILED, FREQ_DAILY
from donations.functions import removeSubscriptionWarnings
from donations.payment_gateways.setting_classes import getStripeSettings
from donations.payment_gateways.stripe.functions import initStripeApiKey, formatDonationAmount
from donations.payment_gateways.stripe.factory import Factory_Stripe


def create_checkout_session(request):
    """ When the user reaches last step after confirming the donation,
        user is redirected via gatewayManager.redirect_to_gateway_url(), which renders redirection_stripe.html

        This function calls to Stripe Api to create a Stripe Session object,
        then this function returns the stripe session id to the stripe js api 'stripe.redirectToCheckout({ sessionId: session.id })' for the redirection to Stripe's checkout page

        Sample (JSON) request: {
            'csrfmiddlewaretoken': 'LZSpOsb364pn9R3gEPXdw2nN3dBEi7RWtMCBeaCse2QawCFIndu93fD3yv9wy0ij'
        }

        @todo: revise error handling, avoid catching all exceptions at the end
    """

    errorObj = {
        "issue": "Exception",
        "description": ""
    }
    try:
        initStripeApiKey()
        stripeSettings = getStripeSettings()

        donation_id = request.session.pop('donation_id', None)
        if not donation_id:
            raise ValueError(_("No donation_id in session"))

        # might throw DoesNotExist error
        donation = Donation.objects.get(pk=donation_id)
        success_url = request.build_absolute_uri(reverse('donations:return-from-stripe'))+'?stripe_session_id={CHECKOUT_SESSION_ID}'
        cancel_url = request.build_absolute_uri(reverse('donations:cancel-from-stripe'))+'?stripe_session_id={CHECKOUT_SESSION_ID}'
        # init session_kwargs with common parameters
        session_kwargs = {
            'payment_method_types': ['card'],
            'metadata': {
                'donation_id': donation.id
            },
            'success_url': success_url,
            'cancel_url': cancel_url,
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
            # see https://stripe.com/docs/api/subscriptions/create#create_subscription-items-price_data-recurring-interval for frequency interval units
            if donation.subscription.recurring_frequency == FREQ_DAILY:
                interval_unit = "day"
            else:
                interval_unit = "month"
            adhoc_price['recurring'] = {
                'interval': interval_unit,
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

        # Update card flow
        if donation.is_recurring:
            try:
                # If we have the old_instance_id metadata we want to change the redirect url
                SubscriptionPaymentMeta.objects.get(subscription=donation.subscription, field_key='old_instance_id')

                success_url = request.build_absolute_uri(reverse('donations:return-from-stripe-card-update'))+'?stripe_session_id={CHECKOUT_SESSION_ID}'
                cancel_url = request.build_absolute_uri(reverse('donations:cancel-from-stripe-card-update'))+'?stripe_session_id={CHECKOUT_SESSION_ID}'
                session_kwargs['success_url'] = success_url
                session_kwargs['cancel_url'] = cancel_url
            except SubscriptionPaymentMeta.DoesNotExist:
                pass

        session = stripe.checkout.Session.create(**session_kwargs)

        # save payment_intent id for recognition purposes when receiving the payment_intent.succeeded webhook for onetime donations
        if session.get('payment_intent'):
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
@transaction.atomic
def verify_stripe_response(request):
    """ This endpoint should be set as the listening endpoint for the webhook set in Stripe's dashboard
        The verification of the incoming Stripe requests is done via Factory_Stripe.initGatewayByVerification(request)
        The webhook should be set with the following events only:
            payment_intent.succeeded
            customer.subscription.deleted
            customer.subscription.updated
            invoice.paid
            invoice.created
            checkout.session.completed

        For more info on how to build this webhook endpoint, refer to Stripe documentation:
        https://stripe.com/docs/webhooks

        @todo: revise error handling, avoid catching all exceptions at the end
    """

    try:
        # Set up gateway manager object with its linking donation, session, etc...
        gatewayManager = Factory_Stripe.initGatewayByVerification(request)

        return gatewayManager.process_webhook_response()
    except WebhookNotProcessedError as error:
        # beware: this exception should be reserved for the incoming but not processed webhook events, or events processed but data not needed further action
        _debug(str(error))
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
    """ This endpoint is submitted as the success_url when creating the Stripe session at create_checkout_session(request)
        This url should receive a single GET param: 'stripe_session_id'
        In Factory_Stripe.initGatewayByReturn(request), we save the stripe_session_id into the donationPaymentMeta data upon a successful request;
        exception will be raised if the endpoint is reached but a previous meta value is found,
        this is done to prevent this endpoint being called unlimitedly

        For more info on how to build this endpoint, refer to Stripe documentation:
        https://stripe.com/docs/payments/checkout/custom-success-page

        @todo: revise error handling, avoid catching all exceptions at the end
    """

    try:
        gatewayManager = Factory_Stripe.initGatewayByReturn(request)
        request.session['return-donation-id'] = gatewayManager.donation.id

        if gatewayManager.donation.is_recurring:
            # Resolve any existing subscriptions
            removeSubscriptionWarnings(request.user)
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
    """ This endpoint is submitted as the cancel_url when creating the Stripe session at create_checkout_session(request)
        This url should receive a single GET param: 'stripe_session_id'
        In Factory_Stripe.initGatewayByReturn(request), we save the stripe_session_id into the donationPaymentMeta data upon a successful request;
        exception will be raised if the endpoint is reached but a previous meta value is found,
        this is done to prevent this endpoint being called unlimitedly, which would set the payment status as Cancelled each time

        @todo: revise error handling, avoid catching all exceptions at the end
    """

    try:
        gatewayManager = Factory_Stripe.initGatewayByReturn(request)
        request.session['return-donation-id'] = gatewayManager.donation.id

        if gatewayManager.session:
            # expire the checkout session for either one-off or recurring donations
            # payment intent for one-off donations will also be cancelled by Stripe after we manually expire the checkout session
            stripe.checkout.Session.expire(gatewayManager.session.id)
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

@login_required
def cancel_from_stripe_card_update(request):
    """ This endpoint is submitted as the cancel_url when creating the Stripe session at create_checkout_session(request)
        for situations in which we update the user's subscription in order to update the fix failed payments.
        We would like to delete donations and subscriptions created from this
        This url should receive a single GET param: 'stripe_session_id'
        In Factory_Stripe.initGatewayByReturn(request), we save the stripe_session_id into the donationPaymentMeta data upon a successful request;
        exception will be raised if the endpoint is reached but a previous meta value is found,
        this is done to prevent this endpoint being called unlimitedly, which would set the payment status as Cancelled each time

        @todo: revise error handling, avoid catching all exceptions at the end
    """

    try:
        gatewayManager = Factory_Stripe.initGatewayByReturn(request)
        request.session['return-donation-id'] = gatewayManager.donation.id

        donation = Donation.objects.get(
            pk=request.session['return-donation-id'])
        sub_instance = donation.subscription
        donation.delete()
        sub_instance.delete()
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
    return redirect('donations:my-recurring-donations')

@login_required
def return_from_stripe_card_update(request):
    """ This endpoint is submitted as the success_url when creating the Stripe session at create_checkout_session(request)
        for situations in which we update the user's subscription in order to update the fix failed payments.
        We would also want to cancel the failed payment
        This url should receive a single GET param: 'stripe_session_id'
        In Factory_Stripe.initGatewayByReturn(request), we save the stripe_session_id into the donationPaymentMeta data upon a successful request;
        exception will be raised if the endpoint is reached but a previous meta value is found,
        this is done to prevent this endpoint being called unlimitedly

        For more info on how to build this endpoint, refer to Stripe documentation:
        https://stripe.com/docs/payments/checkout/custom-success-page

        @todo: revise error handling, avoid catching all exceptions at the end
    """

    try:
        gatewayManager = Factory_Stripe.initGatewayByReturn(request)
        if gatewayManager.donation.is_recurring:
            try:
                # We wamt to cancel the payment failed subscriptioninstance under this subscription
                # now that we have an active one
                parent = gatewayManager.donation.subscription.parent
                instance = SubscriptionInstance.objects.get(parent=parent, recurring_status=STATUS_PAYMENT_FAILED)

                # Save this flag for old subscription instance so that we don't send emails when we cancel the subscription
                spmeta = SubscriptionPaymentMeta(
                    subscription=instance, field_key='awaiting_cancelation', field_value=True)
                spmeta.save()

                old_gateway = Factory_Stripe.initGateway(request, None, instance)
                old_gateway.cancel_recurring_payment()
            except SubscriptionPaymentMeta.DoesNotExist:
                pass

            # Resolve any existing subscriptions
            removeSubscriptionWarnings(request.user)
        request.session['updated-card'] = 'True'
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
    return redirect('donations:my-recurring-donations')
