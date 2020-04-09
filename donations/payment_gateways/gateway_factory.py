from donations.functions import raiseObjectNone
from donations.payment_gateways.core import PaymentGatewayManager
from donations.payment_gateways._2c2p import Gateway_2C2P
from donations.payment_gateways.paypal import Gateway_Paypal
from donations.models import Donation
# todo: Add Stripe's payment gateway import


class PaymentGatewayFactory(object):

    @staticmethod
    def initGateway(request, donation):
        """ Instantiate the specific type of payment gateway manager with current request and specified gateway and donation record """
        if not donation:
            raiseObjectNone(
                'Donation object cannot be none while initializing BasePaymentGateway class')
        if donation.gateway.is_2c2p():
            return Gateway_2C2P(request, donation)
        elif donation.gateway.is_paypal():
            return Gateway_Paypal(request, donation)
        # todo: Add Stripe's Gateway init line
        else:
            raiseObjectNone(
                'The Provided gateway has not been implemented yet')

    @staticmethod
    def initGatewayByVerification(request):
        """ Instantiate the specific type of payment gateway manager with current request (expected to be a form of verification response from gateway server) """
        if 'user_defined_1' in request.POST:
            donation = Donation.objects.get(
                pk=int(request.POST['user_defined_1']))
            if not donation:
                raiseObjectNone(
                    'Donation id - {} from user_defined_1 is not found in the omp database.'.format(request.POST['user_defined_1']))
            else:
                return Gateway_2C2P(request, donation)
        # todo: add paypal and stripe's verification listener logic
