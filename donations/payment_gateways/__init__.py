from newstream.functions import raiseObjectNone
from donations.payment_gateways._2c2p.factory import Factory_2C2P
from donations.payment_gateways.paypal.factory import Factory_Paypal
from donations.payment_gateways.stripe.factory import Factory_Stripe


def InitPaymentGateway(request, donation=None, subscription=None):
    """ Instantiate the specific type of payment gateway manager with current request and specified gateway and donation record """
    if not donation and not subscription:
        raiseObjectNone(
            'Either one of donation or subscription has to be defined while initializing BasePaymentGateway class')
    paymentObj = donation or subscription
    if paymentObj.gateway.is_2c2p():
        return Factory_2C2P.initGateway(request, donation, subscription)
    elif paymentObj.gateway.is_paypal():
        return Factory_Paypal.initGateway(request, donation, subscription)
    elif paymentObj.gateway.is_stripe():
        return Factory_Stripe.initGateway(request, donation, subscription)
    else:
        raiseObjectNone(
            'The Provided gateway has not been implemented yet')