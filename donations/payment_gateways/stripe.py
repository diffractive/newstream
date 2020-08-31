import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from donations.models import Donation, STATUS_COMPLETE
from donations.payment_gateways.core import PaymentGatewayManager
from donations.payment_gateways.setting_classes import getStripeSettings
from donations.functions import formatAmountCentsDecimal, sendDonationNotifToAdmins, sendDonationReceipt
from newstream.functions import uuid4_str, getSiteName, getSiteSettings, getFullReverseUrl, printvars


def initStripeApiKey(request):
    stripeSettings = getStripeSettings(request)
    stripe.api_key = stripeSettings.secret_key


class Gateway_Stripe(PaymentGatewayManager):

    def __init__(self, request, donation, session=None):
        super().__init__(request, donation)
        # set stripe settings object
        self.settings = getStripeSettings(request)
        # stripe uses a checkout session object, init the property here
        # the paymentIntent object's id is referenced in session.payment_intent
        self.session = session

    def base_live_redirect_url(self):
        pass

    def base_testmode_redirect_url(self):
        pass

    def build_redirect_url_params(self):
        return ''

    def redirect_to_gateway_url(self):
        """ Overriding parent implementation as Stripe redirects with js on client browser """

        # save donation id in session for use in later checkout session creation
        self.request.session['donation_id'] = self.donation.id

        return render(self.request, 'donations/redirection_stripe.html', {'publishable_key': self.settings.publishable_key})

    def verify_gateway_response(self):
        pass


class StripeGatewayFactory(object):
    @staticmethod
    def initGatewayByVerification(request):
        """ Instantiate the specific type of payment gateway manager with current request (expected to be a form of verification response from gateway server) """
        initStripeApiKey(request)
        siteSettings = getSiteSettings(request)

        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, siteSettings.stripe_webhook_secret
            )
        except ValueError as e:
            # Invalid payload
            print(e, flush=True)
            return None
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print(e, flush=True)
            return None

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']

            # Fulfill the purchase...
            session_id = session.id
            if session_id:
                session = stripe.checkout.Session.retrieve(session_id)
                payment_intent = stripe.PaymentIntent.retrieve(
                    session.payment_intent)

                if 'donation_id' in payment_intent.metadata:
                    donation_id = payment_intent.metadata['donation_id']
                    try:
                        donation = Donation.objects.get(pk=donation_id)
                        # update payment status
                        donation.payment_status = STATUS_COMPLETE
                        donation.save()
                        return Gateway_Stripe(request, donation, session)
                    except Donation.DoesNotExist:
                        print('No matching Donation found, donation_id: ' +
                              str(donation_id), flush=True)
                        return None

        return None

    @staticmethod
    def initGatewayByReturn(request):
        initStripeApiKey(request)

        session_id = request.GET.get("stripe_session_id", None)
        if session_id:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent = stripe.PaymentIntent.retrieve(
                session.payment_intent)

            if 'donation_id' in payment_intent.metadata:
                donation_id = payment_intent.metadata['donation_id']
                try:
                    donation = Donation.objects.get(pk=donation_id)
                    return Gateway_Stripe(request, donation, session)
                except Donation.DoesNotExist:
                    print('No matching Donation found, donation_id: ' +
                          str(donation_id), flush=True)
                    return None
            return None
        else:
            print('No returned Stripe session found', flush=True)
            return None


@csrf_exempt
def create_checkout_session(request):
    initStripeApiKey(request)
    stripeSettings = getStripeSettings(request)
    siteSettings = getSiteSettings(request)

    donation_id = request.session.get('donation_id', None)

    if donation_id:
        # get donation
        donation = get_object_or_404(Donation, id=donation_id)

        # Product should have been created by admin manually at the dashboard
        # if no product exists, create one here(double safety net)
        # todo: make sure the product_id in site_settings has been set by some kind of configuration enforcement before site is launched
        product_list = stripe.Product.list(active=True)
        print("Number of active Stripe products: " +
              str(len(product_list['data'])), flush=True)
        product = None
        if len(product_list['data']) == 0:
            # create new product here
            product = stripe.Product.create(name=str(_(
                "Newstream Default Product for Donation")), idempotency_key=uuid4_str())
            # Update product id in site_settings & stripe settings
            siteSettings.stripe_product_id = product.id
            siteSettings.save()
            stripeSettings.product_id = product.id
        else:
            # get the product, should aim at the product with the specific product id
            for prod in product_list['data']:
                if prod.id == stripeSettings.product_id:
                    product = prod
        if product == None:
            print('Cannot initialize/get the stripe product instance', flush=True)
            return HttpResponse(status=500)

        # ad-hoc price is used
        amount_str = formatAmountCentsDecimal(
            donation.donation_amount*100, donation.currency)
        adhoc_price = {
            'unit_amount_decimal': amount_str,
            'currency': donation.currency.lower(),
            'product': product.id
        }

        session = stripe.checkout.Session.create(
            customer_email=donation.user.email,
            payment_method_types=['card'],
            line_items=[{
                'price_data': adhoc_price,
                'quantity': 1,
            }],
            mode='payment',
            payment_intent_data={
                'metadata': {
                    'donation_id': donation.id
                }
            },
            success_url=getFullReverseUrl(
                request, 'donations:return-from-stripe')+'?stripe_session_id={CHECKOUT_SESSION_ID}',
            cancel_url=getFullReverseUrl(
                request, 'donations:cancel-from-stripe')+'?stripe_session_id={CHECKOUT_SESSION_ID}',
            idempotency_key=uuid4_str()
        )

        return JsonResponse({'id': session.id})
    return HttpResponse(status=500)


@csrf_exempt
def verify_stripe_response(request):
    gatewayManager = StripeGatewayFactory.initGatewayByVerification(request)
    if gatewayManager:
        # set default language for admins' emails
        translation.activate(settings.LANGUAGE_CODE)

        # email new donation notification to admin list
        # only when the donation is brand new, not counting in recurring renewals
        if not gatewayManager.donation.parent_donation:
            sendDonationNotifToAdmins(request, gatewayManager.donation)

        # set language for donation_receipt.html
        user = gatewayManager.donation.user
        if user.language_preference:
            translation.activate(user.language_preference)

        # email thank you receipt to user
        sendDonationReceipt(request, gatewayManager.donation)

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


@csrf_exempt
def return_from_stripe(request):
    gatewayManager = StripeGatewayFactory.initGatewayByReturn(request)
    if gatewayManager:
        request.session['return-donation-id'] = gatewayManager.donation.id
    else:
        request.session['return-error'] = str(_(
            "Results returned from gateway is invalid."))
    return redirect('donations:thank-you')


@csrf_exempt
def cancel_from_stripe(request):
    gatewayManager = StripeGatewayFactory.initGatewayByReturn(request)
    if gatewayManager:
        request.session['return-donation-id'] = gatewayManager.donation.id

        if gatewayManager.session:
            # todo: nicer reception for the returned paymentIntent object
            stripe.PaymentIntent.cancel(gatewayManager.session.payment_intent)
    else:
        request.session['return-error'] = str(_(
            "Results returned from gateway is invalid."))
    return redirect('donations:cancelled')
