from donations.payment_gateways.gateway_factory import PaymentGatewayFactory
from donations.payment_gateways.offline.gateway import Gateway_Offline


class Factory_Offline(PaymentGatewayFactory):
    @staticmethod
    def initGateway(request, donation, subscription, **kwargs):
        return Gateway_Offline(request, donation, subscription, **kwargs)

    @staticmethod
    def initGatewayByVerification(request):
        pass

    @staticmethod
    def initGatewayByReturn(request):
        pass
