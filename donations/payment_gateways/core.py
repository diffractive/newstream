from donations.functions import raiseObjectNone, isTestMode
from django.shortcuts import redirect
from abc import ABC, abstractmethod


class PaymentGatewayManager(ABC):

    def __init__(self, request, gateway):
        # stores the request object from django
        self.request = request
        # stores the PaymentGateway object in omp
        if not gateway:
            raiseObjectNone(
                'PaymentGateway object cannot be none while initializing BasePaymentGateway class')
        self.gateway = gateway
        # stores whether current app is in test mode or not
        self.testing_mode = isTestMode(self.request)

    @abstractmethod
    def base_live_redirect_url(self):
        """ Override to return the base of live(production) redirect url for this payment gateway """
        pass

    @abstractmethod
    def base_testmode_redirect_url(self):
        """ Override to return the base of testmode(staging) redirect url for this payment gateway """
        pass

    @abstractmethod
    def build_redirect_url_params(self):
        """ Override to build the query string containing the important post data, to be appended to the redirect url """
        pass

    def get_built_redirect_url(self):
        return self.base_gateway_redirect_url() + '?' + self.build_redirect_url_params()

    def base_gateway_redirect_url(self):
        if not self.testing_mode:
            return self.base_live_redirect_url()
        return self.base_testmode_redirect_url()

    def redirect_to_gateway_url(self):
        return redirect(self.get_built_redirect_url())
