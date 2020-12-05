import json
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from paypalcheckoutsdk.core import PayPalHttpClient
from paypalcheckoutsdk.orders import OrdersGetRequest
from paypalrestsdk.notifications import WebhookEvent

from newstream.classes import WebhookNotProcessedError
from newstream.functions import printvars, _debug, _error
from donations.models import Donation
from donations.payment_gateways.gateway_factory import PaymentGatewayFactory
from donations.payment_gateways.paypal.gateway import Gateway_Paypal
from donations.payment_gateways.paypal.constants import *
from donations.payment_gateways.setting_classes import getPayPalSettings
from donations.payment_gateways.paypal.functions import getSubscriptionDetails


class Factory_Paypal(PaymentGatewayFactory):
    @staticmethod
    def initGateway(request, donation, subscription, **kwargs):
        return Gateway_Paypal(request, donation, subscription, **kwargs)

    @staticmethod
    def initGatewayByVerification(request):
        paypalSettings = getPayPalSettings(request)

        # The payload body sent in the webhook event
        event_body = request.body.decode()
        json_data = json.loads(request.body)
        _debug('Event Type: '+json_data['event_type'])
        # printvars(request.headers)
        # Paypal-Transmission-Id in webhook payload header
        transmission_id = request.headers['Paypal-Transmission-Id']
        # Paypal-Transmission-Time in webhook payload header
        timestamp = request.headers['Paypal-Transmission-Time']
        # Webhook id created
        webhook_id = paypalSettings.webhook_id
        # Paypal-Transmission-Sig in webhook payload header
        actual_signature = request.headers['Paypal-Transmission-Sig']
        # Paypal-Cert-Url in webhook payload header
        cert_url = request.headers['Paypal-Cert-Url']
        # PayPal-Auth-Algo in webhook payload header
        auth_algo = request.headers['PayPal-Auth-Algo']

        response = WebhookEvent.verify(
            transmission_id, timestamp, webhook_id, event_body, cert_url, actual_signature, auth_algo)
        if not response:
            _debug('Webhook verification result: '+str(response))

        if response:
            donation_id = None
            subscription = None
            kwargs = {}
            expected_events = [EVENT_PAYMENT_CAPTURE_COMPLETED, EVENT_BILLING_SUBSCRIPTION_ACTIVATED, EVENT_BILLING_SUBSCRIPTION_UPDATED, EVENT_PAYMENT_SALE_COMPLETED]

            # one-time donation payment captured
            if json_data['event_type'] == EVENT_PAYMENT_CAPTURE_COMPLETED:
                if 'custom_id' in json_data['resource']:
                    donation_id = json_data['resource']['custom_id']
                else:
                    raise ValueError(_('Missing custom_id(donation_id) in json_data.resource'))

            # subscription activated
            if json_data['event_type'] == EVENT_BILLING_SUBSCRIPTION_ACTIVATED:
                subscription = json_data['resource']
                if 'custom_id' in json_data['resource']:
                    donation_id = json_data['resource']['custom_id']
                else:
                    raise ValueError(_('Missing custom_id(donation_id) in json_data.resource'))

            # subscription updated
            if json_data['event_type'] == EVENT_BILLING_SUBSCRIPTION_UPDATED:
                subscription = json_data['resource']
                if 'custom_id' in json_data['resource']:
                    donation_id = json_data['resource']['custom_id']
                else:
                    raise ValueError(_('Missing custom_id(donation_id) in json_data.resource'))

            # subscription payment sale completed
            if json_data['event_type'] == EVENT_PAYMENT_SALE_COMPLETED:
                subscription_id = json_data['resource']['billing_agreement_id']
                subscription = getSubscriptionDetails(request, subscription_id)
                if 'custom_id' in subscription:
                    donation_id = subscription['custom_id']
                else:
                    raise ValueError(_('Missing custom_id(donation_id) in curlPaypal-returned subscription'))

            if json_data['event_type'] in expected_events and not donation_id:
                raise ValueError(_("Missing donation_id after processing events from paypal"))
            if json_data['event_type'] not in expected_events:
                raise WebhookNotProcessedError(_("PayPal Event not expected for processing at the moment"))
            try:
                donation = Donation.objects.get(pk=donation_id)
                kwargs['payload'] = json_data['resource']
                kwargs['event_type'] = json_data['event_type']
                return Factory_Paypal.initGateway(request, donation, subscription, **kwargs)
            except Donation.DoesNotExist:
                raise ValueError(_("Donation object not found by id: ")+str(donation_id))
        else:
            raise ValueError(_("PayPal Webhook verification failed."))

    @staticmethod
    def initGatewayByReturn(request):
        # a get param named 'token' contains the order_id
        paypalSettings = getPayPalSettings(request)
        client = PayPalHttpClient(paypalSettings.environment)
        donation_id = None
        subscription = {}
        kwargs = {}

        if request.GET.get('subscription_id', None):
            # recurring payment
            subscription = getSubscriptionDetails(request, request.GET.get('subscription_id'))
            if 'custom_id' in subscription:
                donation_id = subscription['custom_id']
            else:
                raise ValueError(_('Missing custom_id(donation_id) in curlPaypal-returned subscription'))
        elif request.GET.get('token', None):
            # onetime payment
            req = OrdersGetRequest(request.GET.get('token'))
            # might throw IOError
            response = client.execute(req)
            _debug('PayPal: Returns from Gateway')
            _debug('PayPal: Order status: ' + response.result.status)
            donation_id = response.result.purchase_units[0].custom_id
            kwargs['order_id'] = request.GET.get('token')
            kwargs['order_status'] = response.result.status
            if not donation_id:
                raise ValueError(_("Missing donation_id in purchase_units custom_id attribute"))
        else:
            raise ValueError(_("Missing token from PayPal request"))
        
        try:
            donation = Donation.objects.get(pk=donation_id)
            return Factory_Paypal.initGateway(request, donation, subscription, **kwargs)
        except Donation.DoesNotExist:
            raise ValueError(_("Donation object not found by id: ")+str(donation_id))
