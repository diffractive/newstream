from donations.functions import raiseObjectNone
from donations.payment_gateways.core import PaymentGatewayManager
from donations.payment_gateways._2c2p import Gateway_2C2P
from donations.payment_gateways.paypal import Gateway_Paypal
# todo: Add Stripe's payment gateway import


class PaymentGatewayFactory(object):

    @classmethod
    def initGateway(cls, request, gateway):
        if not gateway:
            raiseObjectNone(
                'PaymentGateway object cannot be none while initializing BasePaymentGateway class')
        if gateway.is_2c2p():
            return Gateway_2C2P(request, gateway)
        elif gateway.is_paypal():
            return Gateway_Paypal(request, gateway)
        # todo: Add Stripe's Gateway init line
        else:
            raiseObjectNone(
                'The Provided gateway has not been implemented yet')
