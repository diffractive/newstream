from abc import ABC, abstractmethod
from django.shortcuts import redirect

from newstream.functions import raiseObjectNone, getSiteSettings
from donations.functions import isTestMode


class PaymentGatewayManager(ABC):

    def __init__(self, request, donation, subscription):
        # stores the request object from django
        self.request = request
        # either one of the donation or subscription object cannot be None
        if not donation and not subscription:
            raiseObjectNone(
                'Either one of donation or subscription has to be defined while initializing BasePaymentGateway class')
        self.donation = donation
        self.subscription = subscription
        # stores whether current app is in test mode or not
        self.testing_mode = isTestMode(self.request)
        # set global settings object
        self.global_settings = getSiteSettings(request)

    @abstractmethod
    def redirect_to_gateway_url(self):
        """ Override to customize the behavior of redirecting donor to payment gateway page """
        pass

    @abstractmethod
    def process_webhook_response(self):
        """ Override to process the webhook response from this payment gateway after verifying it """
        pass

    @abstractmethod
    def update_recurring_payment(self):
        """ Override to implement the specific logic of the payment gateway of updating a recurring payment """
        pass

    @abstractmethod
    def cancel_recurring_payment(self):
        """ Override to implement the specific logic of the payment gateway of cancelling a recurring payment """
        pass
