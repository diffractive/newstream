from abc import ABC, abstractmethod


class PaymentGatewayFactory(ABC):
    @staticmethod
    @abstractmethod
    def initGateway(request, donation=None, subscription=None):
        """ 
        Override to instantiate the gateway manager
        * No checks are done on how many arguments concrete implementations take.
        """
        pass

    @staticmethod
    @abstractmethod
    def initGatewayByVerification(request):
        """ Override to instantiate the specific type of payment gateway manager with current request (expected to be a form of verification response from gateway server) """
        pass

    @staticmethod
    @abstractmethod
    def initGatewayByReturn(request):
        """ Override to instantiate the specific type of payment gateway manager with current request (expected to be a redirect response from gateway payment page) """
        pass
