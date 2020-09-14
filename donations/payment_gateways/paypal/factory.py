from donations.payment_gateways.gateway_factory import PaymentGatewayFactory
from donations.payment_gateways.paypal.gateway import Gateway_Paypal


class Factory_Paypal(PaymentGatewayFactory):
    @staticmethod
    def initGateway(request, donation, subscription):
        return Gateway_Paypal(request, donation, subscription)

    @staticmethod
    def initGatewayByVerification(request):
        pass

    @staticmethod
    def initGatewayByReturn(request):
        pass
