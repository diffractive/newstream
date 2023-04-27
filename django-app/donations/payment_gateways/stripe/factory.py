import stripe
from django.utils.translation import gettext_lazy as _

from newstream.classes import WebhookNotProcessedError
from newstream.functions import _debug
from donations.models import Donation, DonationPaymentMeta, Subscription
from donations.payment_gateways.setting_classes import getStripeSettings
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
        initStripeApiKey()
        stripeSettings = getStripeSettings()

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
        invoice = None
        kwargs = {}
        expected_events = [EVENT_CHECKOUT_SESSION_COMPLETED, EVENT_PAYMENT_INTENT_SUCCEEDED, EVENT_INVOICE_CREATED, EVENT_INVOICE_PAID, EVENT_CUSTOMER_SUBSCRIPTION_UPDATED, EVENT_CUSTOMER_SUBSCRIPTION_DELETED]

        # the following call will raise ValueError/stripe.error.SignatureVerificationError
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripeSettings.webhook_secret
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
        # if it's givewp subscription -> no donation_id in metadata is set -> query subscription from profile_id -> then get first donation as parent donation
        # if it's newstream-created subscription -> has donation_id in metadata -> query donation is enough(since profile_id might not have yet been set in subscription)
        # https://stripe.com/docs/billing/subscriptions/webhooks#understand
        if event['type'] == EVENT_INVOICE_CREATED:
            invoice = event['data']['object']
            subscription_id = invoice.subscription

            if subscription_id:
                subscription_obj = stripe.Subscription.retrieve(subscription_id)
                if 'donation_id' in subscription_obj.metadata:
                    # newstream-created subscription
                    donation_id = subscription_obj.metadata['donation_id']
                else:
                    # givewp subscription
                    try:
                        subscription = Subscription.objects.get(profile_id=subscription_id)
                        donation = Donation.objects.filter(subscription=subscription).order_by('id').first()
                        can_skip_donation_id = True
                        if not donation:
                            raise ValueError(_('Missing parent donation queried via Subscription, subscription_id: ')+subscription_id)
                    except Subscription.DoesNotExist:
                        raise ValueError(_('No matching Subscription found, profile_id: ')+subscription_id)
            else:
                raise ValueError(_('Missing subscription_id'))

        # Intercept the invoice paid event for subscriptions
        # At Givewp, invoice.payment_succeeded is processed instead
        # but I checked that the payloads of both invoice.paid and invoice.payment_succeeded are the same
        # so I will process only the invoice.paid event for both Newstream or Givewp Subscriptions
        # if it's givewp subscription -> no donation_id in metadata is set -> query subscription from profile_id -> then get first donation as parent donation
        # if it's newstream-created subscription -> has donation_id in metadata -> query donation is enough(since profile_id might not have yet been set in subscription)
        if event['type'] == EVENT_INVOICE_PAID:
            invoice = event['data']['object']
            subscription_id = invoice.subscription

            if subscription_id:
                subscription_obj = stripe.Subscription.retrieve(subscription_id)
                if 'donation_id' in subscription_obj.metadata:
                    # newstream-created subscription
                    donation_id = subscription_obj.metadata['donation_id']
                else:
                    # givewp subscription
                    try:
                        subscription = Subscription.objects.get(profile_id=subscription_id)
                        donation = Donation.objects.filter(subscription=subscription).order_by('id').first()
                        can_skip_donation_id = True
                        if not donation:
                            raise ValueError(_('Missing parent donation queried via Subscription, subscription_id: ')+subscription_id)
                    except Subscription.DoesNotExist:
                        raise ValueError(_('No matching Subscription found, profile_id: ')+subscription_id)
            else:
                raise ValueError(_('Missing subscription_id'))

        # The subscription created event is not to be used for subscription model init, so as to prevent race condition with the subscription model init in updated event
        # That is because there is no guarantee which event hits first, it's better to let one event handles the model init as well.

        # Intercept the subscription updated event
        # if it's givewp subscription -> no donation_id in metadata is set -> query subscription from profile_id -> then get first donation as parent donation
        # if it's newstream-created subscription -> has donation_id in metadata -> query donation is enough(since profile_id might not have yet been set in subscription)
        if event['type'] == EVENT_CUSTOMER_SUBSCRIPTION_UPDATED:
            subscription_obj = event['data']['object']

            if subscription_obj:
                if 'donation_id' in subscription_obj.metadata:
                    # newstream-created subscription
                    donation_id = subscription_obj.metadata['donation_id']
                else:
                    # givewp subscription
                    subscription_id = subscription_obj.id
                    try:
                        subscription = Subscription.objects.get(profile_id=subscription_id)
                        donation = Donation.objects.filter(subscription=subscription).order_by('id').first()
                        can_skip_donation_id = True
                        if not donation:
                            raise ValueError(_('Missing parent donation queried via Subscription, subscription_id: ')+subscription_id)
                    except Subscription.DoesNotExist:
                        raise ValueError(_('No matching Subscription found, profile_id: ')+subscription_id)

        # Intercept the subscription deleted event
        # This event links to either Newstream or Givewp created subscriptions
        # if it's givewp subscription -> no donation_id in metadata is set -> query subscription from profile_id -> then get first donation as parent donation
        # if it's newstream-created subscription -> has donation_id in metadata -> query donation is enough(since profile_id might not have yet been set in subscription)
        if event['type'] == EVENT_CUSTOMER_SUBSCRIPTION_DELETED:
            subscription_obj = event['data']['object']

            if subscription_obj:
                if 'donation_id' in subscription_obj.metadata:
                    # newstream-created subscription
                    donation_id = subscription_obj.metadata['donation_id']
                else:
                    # givewp subscription
                    subscription_id = subscription_obj.id
                    try:
                        subscription = Subscription.objects.get(profile_id=subscription_id)
                        donation = Donation.objects.filter(subscription=subscription).order_by('id').first()
                        can_skip_donation_id = True
                        if not donation:
                            raise ValueError(_('Missing parent donation queried via Subscription, subscription_id: ')+subscription_id)
                    except Subscription.DoesNotExist:
                        raise ValueError(_('No matching Subscription found, profile_id: ')+subscription_id)

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
            kwargs['invoice'] = invoice
            return Factory_Stripe.initGateway(request, donation, subscription, **kwargs)
        except Donation.DoesNotExist:
            raise ValueError(_('No matching Donation found, donation_id: ')+str(donation_id))

    @staticmethod
    def initGatewayByReturn(request):
        initStripeApiKey()

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
            # raise error if stripe_session_id already found in DonationPaymentMeta
            dpm = DonationPaymentMeta.objects.filter(donation=donation, field_key='stripe_session_id', field_value=session_id)
            if len(dpm) >= 1:
                raise ValueError(_("Stripe session id found. Return request from Stripe is already invalid."))
            else:
                dpm = DonationPaymentMeta(donation=donation, field_key='stripe_session_id', field_value=session_id)
                dpm.save()
            return Factory_Stripe.initGateway(request, donation, None, **kwargs)
        except Donation.DoesNotExist:
            raise ValueError(_('No matching Donation found, donation_id: ')+str(donation_id))
