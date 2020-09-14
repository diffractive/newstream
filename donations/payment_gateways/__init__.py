from newstream.functions import raiseObjectNone
from donations.payment_gateways._2c2p.factory import Factory_2C2P
from donations.payment_gateways.paypal.factory import Factory_Paypal
from donations.payment_gateways.stripe.factory import Factory_Stripe
from donations.payment_gateways._2c2p.forms import RecurringPaymentForm_2C2P
from donations.payment_gateways.paypal.forms import RecurringPaymentForm_Paypal
from donations.payment_gateways.stripe.forms import RecurringPaymentForm_Stripe


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


def InitEditRecurringPaymentForm(request, subscription):
    if not subscription:
        raiseObjectNone('Needs subscription to init the edit form for the recurring payment')
    if subscription.gateway.is_2c2p():
        return RecurringPaymentForm_2C2P(request.POST, subscription=subscription) if request.method == 'POST' else RecurringPaymentForm_2C2P(subscription=subscription)
    elif subscription.gateway.is_paypal():
        return RecurringPaymentForm_Paypal(request.POST, subscription=subscription) if request.method == 'POST' else RecurringPaymentForm_Paypal(subscription=subscription)
    elif subscription.gateway.is_stripe():
        return RecurringPaymentForm_Stripe(request.POST, subscription=subscription) if request.method == 'POST' else RecurringPaymentForm_Stripe(subscription=subscription)
    else:
        raiseObjectNone('The Provided gateway has not been implemented yet')


def getEditRecurringPaymentHtml(subscription):
    if not subscription:
        raiseObjectNone('Needs subscription to init the edit form for the recurring payment')
    if subscription.gateway.is_2c2p():
        return 'edit_2c2p_recurring_payment_form.html'
    elif subscription.gateway.is_paypal():
        return 'edit_paypal_recurring_payment_form.html'
    elif subscription.gateway.is_stripe():
        return 'edit_stripe_recurring_payment_form.html'
    else:
        raiseObjectNone('The Provided gateway has not been implemented yet')