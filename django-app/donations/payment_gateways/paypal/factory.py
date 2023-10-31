import json
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from paypalcheckoutsdk.core import PayPalHttpClient
from paypalcheckoutsdk.orders import OrdersGetRequest
from paypalrestsdk.notifications import WebhookEvent

from newstream.classes import WebhookNotProcessedError
from newstream.functions import _debug
from donations.models import Donation, DonationPaymentMeta
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
        paypalSettings = getPayPalSettings()

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

        # Ignore webhook verification if using localpaypal
        if settings.PAYPAL_API_BASE:
            response = True,
        else:
            response = WebhookEvent.verify(
                transmission_id, timestamp, webhook_id, event_body, cert_url, actual_signature, auth_algo)
        if not response:
            raise ValueError("PayPal Webhook verification failed. Webhook verification result: "+str(response))

        if response:
            donation_id = None
            subscription = None
            subscription_obj = None
            kwargs = {}
            expected_events = [EVENT_PAYMENT_CAPTURE_COMPLETED, EVENT_BILLING_SUBSCRIPTION_ACTIVATED, EVENT_BILLING_SUBSCRIPTION_UPDATED, EVENT_PAYMENT_SALE_COMPLETED, EVENT_BILLING_SUBSCRIPTION_CANCELLED, EVENT_BILLING_SUBSCRIPTION_PAYMENT_FAILED, EVENT_BILLING_SUBSCRIPTION_SUSPENDED]

            # one-time donation payment captured
            if json_data['event_type'] == EVENT_PAYMENT_CAPTURE_COMPLETED:
                if 'custom_id' in json_data['resource']:
                    donation_id = json_data['resource']['custom_id']
                else:
                    raise ValueError('Missing custom_id(donation_id) in json_data.resource, resource id: {}'.format(json_data['resource']['id']))

            # subscription activated
            if json_data['event_type'] == EVENT_BILLING_SUBSCRIPTION_ACTIVATED:
                subscription_obj = json_data['resource']
                if 'custom_id' in json_data['resource']:
                    donation_id = json_data['resource']['custom_id']
                else:
                    raise ValueError('Missing custom_id(donation_id) in json_data.resource, subscription id: {}'.format(json_data['resource']['id']))

            # subscription updated
            if json_data['event_type'] == EVENT_BILLING_SUBSCRIPTION_UPDATED:
                subscription_obj = json_data['resource']
                if 'custom_id' in json_data['resource']:
                    donation_id = json_data['resource']['custom_id']
                else:
                    raise ValueError('Missing custom_id(donation_id) in json_data.resource, subscription id: {}'.format(json_data['resource']['id']))

            # subscription payment sale completed
            if json_data['event_type'] == EVENT_PAYMENT_SALE_COMPLETED:
                subscription_id = json_data['resource']['billing_agreement_id']
                subscription_obj = getSubscriptionDetails(request.session, subscription_id)
                if 'custom_id' in subscription_obj:
                    donation_id = subscription_obj['custom_id']
                else:
                    raise ValueError('Missing custom_id(donation_id) in curlPaypal-returned subscription_obj, subscription id: {}'.format(subscription_obj['id']))

            # subscription payment failed
            if json_data['event_type'] == EVENT_BILLING_SUBSCRIPTION_PAYMENT_FAILED:
                subscription_obj = json_data['resource']
                if 'custom_id' in json_data['resource']:
                    donation_id = json_data['resource']['custom_id']
                else:
                    raise ValueError('Missing custom_id(donation_id) in json_data.resource, subscription id: {}'.format(json_data['resource']['id']))

            # subscription cancelled
            if json_data['event_type'] == EVENT_BILLING_SUBSCRIPTION_CANCELLED:
                subscription_obj = json_data['resource']
                if 'custom_id' in json_data['resource']:
                    donation_id = json_data['resource']['custom_id']
                else:
                    raise ValueError('Missing custom_id(donation_id) in json_data.resource, subscription id: {}'.format(json_data['resource']['id']))

            # subscription suspended
            if json_data['event_type'] == EVENT_BILLING_SUBSCRIPTION_SUSPENDED:
                subscription_obj = json_data['resource']
                if 'custom_id' in json_data['resource']:
                    donation_id = json_data['resource']['custom_id']
                else:
                    raise ValueError('Missing custom_id(donation_id) in json_data.resource, subscription id: {}'.format(json_data['resource']['id']))

            if json_data['event_type'] in expected_events and not donation_id:
                raise ValueError(_("Missing donation_id after processing events from paypal"))
            if json_data['event_type'] not in expected_events:
                raise WebhookNotProcessedError(_("PayPal Event not expected for processing at the moment"))
            try:
                donation = Donation.objects.get(pk=donation_id)
                kwargs['payload'] = json_data['resource']
                kwargs['event_type'] = json_data['event_type']
                kwargs['subscription_obj'] = subscription_obj
                return Factory_Paypal.initGateway(request, donation, subscription, **kwargs)
            except Donation.DoesNotExist:
                raise ValueError(_("Donation object not found by id: ")+str(donation_id))

    @staticmethod
    def initGatewayByReturn(request):
        # a get param named 'token' contains the order_id
        paypalSettings = getPayPalSettings()
        client = PayPalHttpClient(paypalSettings.environment)
        donation_id = None
        subscription_obj = {}
        kwargs = {}

        if request.GET.get('subscription_id', None):
            # recurring payment
            subscription_obj = getSubscriptionDetails(request.session, request.GET.get('subscription_id'))
            kwargs['subscription_obj'] = subscription_obj
            if 'custom_id' in subscription_obj:
                donation_id = subscription_obj['custom_id']
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

            if request.GET.get('subscription_id', None):
                # raise error if paypal_subscription_id already found in DonationPaymentMeta
                dpm = DonationPaymentMeta.objects.filter(donation=donation, field_key='paypal_subscription_id', field_value=request.GET.get('subscription_id'))
                if len(dpm) >= 1:
                    raise ValueError(_("PayPal subscription id found. Return request from PayPal is already invalid."))
                else:
                    dpm = DonationPaymentMeta(donation=donation, field_key='paypal_subscription_id', field_value=request.GET.get('subscription_id'))
                    dpm.save()
            elif request.GET.get('token', None):
                # raise error if paypal_token already found in DonationPaymentMeta
                dpm = DonationPaymentMeta.objects.filter(donation=donation, field_key='paypal_token', field_value=request.GET.get('token'))
                if len(dpm) >= 1:
                    raise ValueError(_("PayPal token found. Return request from PayPal is already invalid."))
                else:
                    dpm = DonationPaymentMeta(donation=donation, field_key='paypal_token', field_value=request.GET.get('token'))
                    dpm.save()
            return Factory_Paypal.initGateway(request, donation, None, **kwargs)
        except Donation.DoesNotExist:
            raise ValueError(_("Donation object not found by id: ")+str(donation_id))
