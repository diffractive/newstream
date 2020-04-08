from donations.payment_gateways.core import PaymentGatewayManager


class Gateway_Paypal(PaymentGatewayManager):

    def base_live_redirect_url(self):
        pass

    def base_testmode_redirect_url(self):
        return 'https://www.yahoo.com'

    def build_redirect_url_params(self):
        return ''
