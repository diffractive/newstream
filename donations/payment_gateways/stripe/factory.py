import stripe
from django.utils.translation import gettext_lazy as _

from newstream.classes import WebhookNotProcessedError
from newstream.functions import getSiteSettings, _debug
from donations.models import Donation, DonationPaymentMeta
from donations.payment_gateways.gateway_factory import PaymentGatewayFactory
from donations.payment_gateways.stripe.gateway import Gateway_Stripe
from donations.payment_gateways.stripe.functions import initStripeApiKey
from donations.payment_gateways.stripe.constants import *


class Factory_Stripe(PaymentGatewayFactory):
    @staticmethod
    def initGateway(request, donation, subscription, **kwargs):
        return Gateway_Stripe(request, donation, subscription, **kwargs)

    @staticmethod
    def initGatewayByVerification(request):
        initStripeApiKey(request)
        siteSettings = getSiteSettings(request)

        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        donation_id = None
        can_skip_donation_id = False
        event = None
        session = None
        payment_intent = None
        donation = None
        subscription = None
        subscription_obj = None
        kwargs = {}
        expected_events = [EVENT_CHECKOUT_SESSION_COMPLETED, EVENT_PAYMENT_INTENT_SUCCEEDED, EVENT_INVOICE_CREATED, EVENT_INVOICE_PAID, EVENT_CUSTOMER_SUBSCRIPTION_UPDATED, EVENT_CUSTOMER_SUBSCRIPTION_DELETED]

        # the following call will raise ValueError/stripe.error.SignatureVerificationError
        event = stripe.Webhook.construct_event(
            payload, sig_header, siteSettings.stripe_webhook_secret
        )

        # for events not being processed
        if event['type'] not in expected_events:
            raise WebhookNotProcessedError(_("Stripe Event not expected for processing at the moment"))
        _debug("[stripe recurring] Incoming Event type:"+event['type'])

        # Intercept the checkout.session.completed event
        if event['type'] == EVENT_CHECKOUT_SESSION_COMPLETED:
            session = event['data']['object']
            # Fulfill the purchase...
            if session:
                if session.mode == 'payment' and session.payment_intent:
                    payment_intent = stripe.PaymentIntent.retrieve(
                        session.payment_intent)
                    if 'donation_id' in payment_intent.metadata:
                        donation_id = payment_intent.metadata['donation_id']
                    else:
                        raise ValueError(_('Missing donation_id in payment_intent.metadata'))
                elif session.mode == 'subscription' and session.subscription:
                    subscription_obj = stripe.Subscription.retrieve(
                        session.subscription)
                    if 'donation_id' in subscription_obj.metadata:
                        donation_id = subscription_obj.metadata['donation_id']
                    else:
                        raise ValueError(_('Missing donation_id in subscription_obj.metadata'))

        # Intercept the payment_intent.succeeded event
        if event['type'] == EVENT_PAYMENT_INTENT_SUCCEEDED:
            payment_intent = event['data']['object']
            # Fulfill the purchase...
            if payment_intent:
                try:
                    dpm = DonationPaymentMeta.objects.get(field_key='stripe_payment_intent_id', field_value=payment_intent.id)
                    donation = dpm.donation
                    can_skip_donation_id = True
                except DonationPaymentMeta.DoesNotExist:
                    # should be renewal payments since only one-time payments have saved stripe_payment_intent_id
                    raise WebhookNotProcessedError(_('Payment Intent Id not found in DonationPaymentMeta:') + payment_intent.id)

        # Intercept the invoice created event for subscriptions(a must for instant invoice finalization)
        # https://stripe.com/docs/billing/subscriptions/webhooks#understand
        if event['type'] == EVENT_INVOICE_CREATED:
            invoice = event['data']['object']
            subscription_id = invoice.subscription

            if subscription_id:
                subscription_obj = stripe.Subscription.retrieve(subscription_id)
                if 'donation_id' in subscription_obj.metadata:
                    donation_id = subscription_obj.metadata['donation_id']
                    kwargs['invoice'] = invoice
                else:
                    raise ValueError(_('Missing donation_id in subscription_obj.metadata'))
            else:
                raise ValueError(_('Missing subscription_id'))

        # Intercept the invoice paid event for subscriptions
        if event['type'] == EVENT_INVOICE_PAID:
            invoice = event['data']['object']
            subscription_id = invoice.subscription

            if subscription_id:
                subscription_obj = stripe.Subscription.retrieve(subscription_id)
                if 'donation_id' in subscription_obj.metadata:
                    donation_id = subscription_obj.metadata['donation_id']
                    kwargs['invoice'] = invoice
                else:
                    raise ValueError(_('Missing donation_id in subscription.metadata'))
            else:
                raise ValueError(_('Missing subscription_id'))

        # The subscription created event is not to be used for subscription model init, so as to prevent race condition with the subscription model init in updated event
        # That is because there is no guarantee which event hits first, it's better to let one event handles the model init as well.

        # Intercept the subscription updated event
        if event['type'] == EVENT_CUSTOMER_SUBSCRIPTION_UPDATED:
            subscription_obj = event['data']['object']

            if subscription_obj:
                if 'donation_id' in subscription_obj.metadata:
                    donation_id = subscription_obj.metadata['donation_id']
                else:
                    raise ValueError(_('Missing donation_id in subscription_obj.metadata'))

        # Intercept the subscription deleted event
        if event['type'] == EVENT_CUSTOMER_SUBSCRIPTION_DELETED:
            subscription_obj = event['data']['object']

            if subscription_obj:
                if 'donation_id' in subscription_obj.metadata:
                    donation_id = subscription_obj.metadata['donation_id']
                else:
                    raise ValueError(_('Missing donation_id in subscription_obj.metadata'))

        # Finally init and return the Stripe Gateway Manager
        if not donation_id and not can_skip_donation_id:
            raise ValueError(_('Missing donation_id'))

        try:
            # no need to query donation object if can skip
            if not can_skip_donation_id and not donation:
                donation = Donation.objects.get(pk=donation_id)
            kwargs['session'] = session
            kwargs['event'] = event
            kwargs['payment_intent'] = payment_intent
            kwargs['subscription_obj'] = subscription_obj
            return Factory_Stripe.initGateway(request, donation, subscription, **kwargs)
        except Donation.DoesNotExist:
            raise ValueError(_('No matching Donation found, donation_id: ')+str(donation_id))

    @staticmethod
    def initGatewayByReturn(request):
        initStripeApiKey(request)

        donation_id = None
        session_id = request.GET.get("stripe_session_id", None)
        if not session_id:
            raise ValueError(_("Missing session_id in request.GET"))

        session = stripe.checkout.Session.retrieve(session_id)
        # no matter 'payment' or 'subscription', metadata also saved at checkout session level
        if 'donation_id' in session.metadata:
            donation_id = session.metadata['donation_id']
        else:
            raise ValueError(_("Missing donation_id in session.metadata"))

        try:
            donation = Donation.objects.get(pk=donation_id)
            kwargs = {}
            kwargs['session'] = session
            return Factory_Stripe.initGateway(request, donation, None, **kwargs)
        except Donation.DoesNotExist:
            raise ValueError(_('No matching Donation found, donation_id: ')+str(donation_id))
