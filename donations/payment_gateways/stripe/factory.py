import stripe
from django.utils.translation import gettext_lazy as _

from newstream.classes import WebhookNotProcessedError
from newstream.functions import raiseObjectNone, getSiteSettings, _debug
from donations.models import Donation, Subscription
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
        '''
        This method verifies webhooks of either Newstream-created transactions or Givewp-created subscriptions
        In givewp, $event_json->data->object->charge is ensured to be not empty before processing the webhooks,
        but I cannot find the 'charge' attribute in my Newstream 'customer.subscription.deleted' event,
        thus I will not apply the same checking here but run the same stripe_signature header check instead.
        '''
        initStripeApiKey(request)
        siteSettings = getSiteSettings(request)

        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        donation_id = None
        can_skip_donation_id = False
        event = None
        session = None
        donation = None
        subscription = None
        subscription_obj = None
        kwargs = {}
        expected_events = [EVENT_CHECKOUT_SESSION_COMPLETED, EVENT_INVOICE_CREATED, EVENT_INVOICE_PAID, EVENT_CUSTOMER_SUBSCRIPTION_UPDATED, EVENT_CUSTOMER_SUBSCRIPTION_DELETED]

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
        # At Givewp, invoice.payment_succeeded is processed instead
        # but I checked that the payloads of both invoice.paid and invoice.payment_succeeded are the same
        # so I will process only the invoice.paid event for both Newstream or Givewp Subscriptions
        # notice that Givewp subscriptions do not have metadata['donation_id'], so ValueError is commented
        if event['type'] == EVENT_INVOICE_PAID:
            invoice = event['data']['object']
            subscription_id = invoice.subscription

            if subscription_id:
                subscription_obj = stripe.Subscription.retrieve(subscription_id)
                if 'donation_id' in subscription_obj.metadata:
                    donation_id = subscription_obj.metadata['donation_id']
                    kwargs['invoice'] = invoice
                else:
                    # should be a Givewp subscription
                    try:
                        subscription = Subscription.objects.get(profile_id=subscription_id)
                        donation = Donation.objects.filter(subscription=subscription).order_by('id').first()
                        if not donation:
                            raise ValueError(_('Missing parent donation queried via Subscription, subscription_id: ')+subscription_id)
                    except Subscription.DoesNotExist:
                        raise ValueError(_('No matching Subscription found, profile_id: ')+subscription_id)
                    # raise ValueError(_('Missing donation_id in subscription_obj.metadata'))
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
        # This event links to either Newstream or Givewp created subscriptions
        # For Givewp created subscriptions, no donation_id is saved in subscription.metadata
        if event['type'] == EVENT_CUSTOMER_SUBSCRIPTION_DELETED:
            subscription_obj = event['data']['object']

            if subscription_obj:
                # donation_id checking can be commented since givewp subscriptions do not have donation_id
                # if 'donation_id' in subscription_obj.metadata:
                #     donation_id = subscription_obj.metadata['donation_id']
                # else:
                #     raise ValueError(_('Missing donation_id in subscription_obj.metadata'))
                try:
                    subscription = Subscription.objects.get(profile_id=subscription_obj.id)
                except Subscription.DoesNotExist:
                    raise ValueError(_('No matching Subscription found, profile_id: ')+subscription_obj.id)

        # Finally init and return the Stripe Gateway Manager
        if not donation_id and not can_skip_donation_id:
            raise ValueError(_('Missing donation_id'))

        try:
            # no need to query donation object if can skip
            if not can_skip_donation_id and not donation:
                donation = Donation.objects.get(pk=donation_id)
            kwargs['session'] = session
            kwargs['event'] = event
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
