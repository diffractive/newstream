import stripe

from newstream.functions import raiseObjectNone, getSiteSettings
from donations.models import Donation
from donations.payment_gateways.gateway_factory import PaymentGatewayFactory
from donations.payment_gateways.stripe.gateway import Gateway_Stripe
from donations.payment_gateways.stripe.functions import initStripeApiKey


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

        # Intercept the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Fulfill the purchase...
            if session:
                if session.mode == 'payment' and session.payment_intent:
                    payment_intent = stripe.PaymentIntent.retrieve(
                        session.payment_intent)
                    if 'donation_id' in payment_intent.metadata:
                        donation_id = payment_intent.metadata['donation_id']
                    else:
                        return None
                elif session.mode == 'subscription' and session.subscription:
                    subscription = stripe.Subscription.retrieve(
                        session.subscription)
                    if 'donation_id' in subscription.metadata:
                        donation_id = subscription.metadata['donation_id']
                    else:
                        return None

        # Intercept the invoice paid event for subscriptions
        if event['type'] == 'invoice.paid':
            invoice = event['data']['object']
            subscription_id = invoice.subscription

            if subscription_id:
                subscription = stripe.Subscription.retrieve(subscription_id)
                if 'donation_id' in subscription.metadata:
                    donation_id = subscription.metadata['donation_id']
                    kwargs['invoice'] = invoice
                else:
                    return None
            else:
                return None

        # The subscription created event is not to be used for subscription model init, so as to prevent race condition with the subscription model init in updated event
        # That is because there is no guarantee which event hits first, it's better to let one event handles the model init as well.

        # Intercept the subscription updated event
        if event['type'] == 'customer.subscription.updated':
            subscription = event['data']['object']

            if subscription:
                if 'donation_id' in subscription.metadata:
                    donation_id = subscription.metadata['donation_id']
                else:
                    return None

        # Intercept the subscription deleted event
        if event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']

            if subscription:
                if 'donation_id' in subscription.metadata:
                    donation_id = subscription.metadata['donation_id']
                else:
                    return None

        # Finally init and return the Stripe Gateway Manager
        if donation_id:
            try:
                donation = Donation.objects.get(pk=donation_id)
                kwargs['session'] = session
                kwargs['event'] = event
                return Factory_Stripe.initGateway(request, donation, subscription, **kwargs)
            except Donation.DoesNotExist:
                print('No matching Donation found, donation_id: ' +
                      str(donation_id), flush=True)
                return None
        return None

    @staticmethod
    def initGatewayByReturn(request):
        initStripeApiKey(request)

        donation_id = None
        session_id = request.GET.get("stripe_session_id", None)
        if session_id:
            session = stripe.checkout.Session.retrieve(session_id)
            # no matter 'payment' or 'subscription', metadata also saved at checkout session level
            if 'donation_id' in session.metadata:
                donation_id = session.metadata['donation_id']
            else:
                return None

            try:
                donation = Donation.objects.get(pk=donation_id)
                kwargs = {}
                kwargs['session'] = session
                return Factory_Stripe.initGateway(request, donation, None, **kwargs)
            except Donation.DoesNotExist:
                print('No matching Donation found, donation_id: ' +
                      str(donation_id), flush=True)
                return None
        else:
            print('No returned Stripe session found', flush=True)
            return None
