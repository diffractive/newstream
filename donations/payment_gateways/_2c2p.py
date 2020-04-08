from donations.payment_gateways.core import PaymentGatewayManager


class Gateway_2C2P(PaymentGatewayManager):

    def base_live_redirect_url(self):
        pass

    def base_testmode_redirect_url(self):
        return 'https://www.google.com'

    def build_redirect_url_params(self):
        return 'q=happy'
