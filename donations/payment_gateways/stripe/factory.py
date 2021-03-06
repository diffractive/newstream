import stripe

from newstream.classes import WebhookNotProcessedError
from newstream.functions import raiseObjectNone, getSiteSettings
from donations.models import Donation
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
        event = None
        session = None
        subscription = None
        kwargs = {}
        expected_events = [EVENT_CHECKOUT_SESSION_COMPLETED, EVENT_INVOICE_CREATED, EVENT_INVOICE_PAID, EVENT_CUSTOMER_SUBSCRIPTION_UPDATED, EVENT_CUSTOMER_SUBSCRIPTION_DELETED]

        event = stripe.Webhook.construct_event(
            payload, sig_header, siteSettings.stripe_webhook_secret
        )

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
                    subscription = stripe.Subscription.retrieve(
                        session.subscription)
                    if 'donation_id' in subscription.metadata:
                        donation_id = subscription.metadata['donation_id']
                    else:
                        raise ValueError(_('Missing donation_id in subscription.metadata'))

        # Intercept the invoice created event for subscriptions(a must for instant invoice finalization)
        # https://stripe.com/docs/billing/subscriptions/webhooks#understand
        if event['type'] == EVENT_INVOICE_CREATED:
            invoice = event['data']['object']
            subscription_id = invoice.subscription

            if subscription_id:
                subscription = stripe.Subscription.retrieve(subscription_id)
                if 'donation_id' in subscription.metadata:
                    donation_id = subscription.metadata['donation_id']
                    kwargs['invoice'] = invoice
                else:
                    raise ValueError(_('Missing donation_id in subscription.metadata'))
            else:
                raise ValueError(_('Missing subscription_id'))

        # Intercept the invoice paid event for subscriptions
        if event['type'] == EVENT_INVOICE_PAID:
            invoice = event['data']['object']
            subscription_id = invoice.subscription

            if subscription_id:
                subscription = stripe.Subscription.retrieve(subscription_id)
                if 'donation_id' in subscription.metadata:
                    donation_id = subscription.metadata['donation_id']
                    kwargs['invoice'] = invoice
                else:
                    raise ValueError(_('Missing donation_id in subscription.metadata'))
            else:
                raise ValueError(_('Missing subscription_id'))

        # The subscription created event is not to be used for subscription model init, so as to prevent race condition with the subscription model init in updated event
        # That is because there is no guarantee which event hits first, it's better to let one event handles the model init as well.

        # Intercept the subscription updated event
        if event['type'] == EVENT_CUSTOMER_SUBSCRIPTION_UPDATED:
            subscription = event['data']['object']

            if subscription:
                if 'donation_id' in subscription.metadata:
                    donation_id = subscription.metadata['donation_id']
                else:
                    raise ValueError(_('Missing donation_id in subscription.metadata'))

        # Intercept the subscription deleted event
        if event['type'] == EVENT_CUSTOMER_SUBSCRIPTION_DELETED:
            subscription = event['data']['object']

            if subscription:
                if 'donation_id' in subscription.metadata:
                    donation_id = subscription.metadata['donation_id']
                else:
                    raise ValueError(_('Missing donation_id in subscription.metadata'))

        # Finally init and return the Stripe Gateway Manager
        if not donation_id:
            raise ValueError(_('Missing donation_id'))
        # for events not being processed
        if event['type'] not in expected_events:
            raise WebhookNotProcessedError(_("Stripe Event not expected for processing at the moment"))

        try:
            donation = Donation.objects.get(pk=donation_id)
            kwargs['session'] = session
            kwargs['event'] = event
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
