from donations.functions import isTestMode
from django.shortcuts import redirect
from newstream.functions import raiseObjectNone, getSiteSettings
from abc import ABC, abstractmethod


class PaymentGatewayManager(ABC):

    def __init__(self, request, donation):
        # stores the request object from django
        self.request = request
        # stores the donation object
        if not donation:
            raiseObjectNone(
                'Donation object cannot be none while initializing BasePaymentGateway class')
        self.donation = donation
        # stores whether current app is in test mode or not
        self.testing_mode = isTestMode(self.request)
        # set global settings object
        self.global_settings = getSiteSettings(request)

    @abstractmethod
    def base_live_redirect_url(self):
        """ Override to return the base of live(production) redirect url for this payment gateway """
        return ''

    @abstractmethod
    def base_testmode_redirect_url(self):
        """ Override to return the base of testmode(staging) redirect url for this payment gateway """
        return ''

    @abstractmethod
    def build_redirect_url_params(self):
        """ Override to build the query string containing the important post data, to be appended to the redirect url """
        return ''

    @abstractmethod
    def verify_gateway_response(self):
        """ Override to verify the response from this payment gateway after payments, returns boolean """
        return False

    def get_built_redirect_url(self):
        return self.base_gateway_redirect_url() + '?' + self.build_redirect_url_params()

    def base_gateway_redirect_url(self):
        if not self.testing_mode:
            return self.base_live_redirect_url()
        return self.base_testmode_redirect_url()

    def redirect_to_gateway_url(self):
        return redirect(self.get_built_redirect_url())
