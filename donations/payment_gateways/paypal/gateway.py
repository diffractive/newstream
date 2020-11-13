from paypalcheckoutsdk.core import PayPalHttpClient
from django.shortcuts import render

from donations.payment_gateways.gateway_manager import PaymentGatewayManager
from donations.payment_gateways.setting_classes import getPayPalSettings


class Gateway_Paypal(PaymentGatewayManager):
    def __init__(self, request, donation=None, subscription=None, **kwargs):
        super().__init__(request, donation, subscription)
        # set paypal settings object
        self.settings = getPayPalSettings(request)
        # init paypal http client
        self.client = PayPalHttpClient(self.settings.environment)
        # saves all remaining kwargs into the manager, e.g. order_id, order_status
        self.__dict__.update(kwargs)

    def redirect_to_gateway_url(self):
        """ Overriding parent implementation as PayPal redirects with js on client browser """

        # save donation id in session for use in later checkout session creation
        self.request.session['donation_id'] = self.donation.id

        return render(self.request, 'donations/redirection_paypal.html', {'client_id': self.settings.client_id, 'currency': self.donation.currency})

    def process_webhook_response(self):
        pass

    def update_recurring_payment(self):
        pass

    def cancel_recurring_payment(self):
        pass
