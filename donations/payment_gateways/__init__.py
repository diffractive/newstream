from django.utils.translation import gettext_lazy as _

from site_settings.models import GATEWAY_STRIPE, GATEWAY_PAYPAL, GATEWAY_2C2P, GATEWAY_OFFLINE, GATEWAY_PAYPAL_LEGACY, GATEWAY_CAN_EDIT_SUBSCRIPTION, GATEWAY_CAN_TOGGLE_SUBSCRIPTION, GATEWAY_CAN_CANCEL_SUBSCRIPTION
from donations.payment_gateways._2c2p.factory import Factory_2C2P
from donations.payment_gateways.paypal.factory import Factory_Paypal
from donations.payment_gateways.paypal_legacy.factory import Factory_Paypal_Legacy
from donations.payment_gateways.stripe.factory import Factory_Stripe
from donations.payment_gateways.offline.factory import Factory_Offline
from donations.payment_gateways._2c2p.forms import RecurringPaymentForm_2C2P
from donations.payment_gateways.paypal.forms import RecurringPaymentForm_Paypal
from donations.payment_gateways.stripe.forms import RecurringPaymentForm_Stripe
from donations.payment_gateways.offline.forms import RecurringPaymentForm_Offline
from donations.payment_gateways._2c2p.constants import API_CAPABILITIES as _2C2P_API_CAPABILITIES
from donations.payment_gateways.paypal.constants import API_CAPABILITIES as PAYPAL_API_CAPABILITIES
from donations.payment_gateways.paypal_legacy.constants import API_CAPABILITIES as PAYPAL_LEGACY_API_CAPABILITIES
from donations.payment_gateways.stripe.constants import API_CAPABILITIES as STRIPE_API_CAPABILITIES
from donations.payment_gateways.offline.constants import API_CAPABILITIES as OFFLINE_API_CAPABILITIES


def InitPaymentGateway(request, donation=None, subscription=None):
    """ Instantiate the specific type of payment gateway manager with current request and specified gateway and donation record """
    if not donation and not subscription:
        raise ValueError(_('Either one of donation or subscription has to be defined while initializing BasePaymentGateway class'))
    paymentObj = donation or subscription
    if paymentObj.gateway.is_2c2p():
        return Factory_2C2P.initGateway(request, donation, subscription)
    elif paymentObj.gateway.is_paypal():
        return Factory_Paypal.initGateway(request, donation, subscription)
    elif paymentObj.gateway.is_paypal_legacy():
        return Factory_Paypal_Legacy.initGateway(request, donation, subscription)
    elif paymentObj.gateway.is_stripe():
        return Factory_Stripe.initGateway(request, donation, subscription)
    elif paymentObj.gateway.is_offline():
        return Factory_Offline.initGateway(request, donation, subscription)
    else:
        raise ValueError(_('The Provided gateway has not been implemented yet'))


def InitEditRecurringPaymentForm(request, subscription):
    if not subscription:
        raise ValueError(_('Needs subscription to init the edit form for the recurring payment'))
    if subscription.gateway.is_2c2p():
        form =  RecurringPaymentForm_2C2P(request.POST, request=request, subscription=subscription, label_suffix='') if request.method == 'POST' else RecurringPaymentForm_2C2P(request=request, subscription=subscription, label_suffix='')
        form.order_fields(
            ['subscription_id', 'currency', 'recurring_amount', 'billing_cycle_now'])
        return form
    elif subscription.gateway.is_paypal():
        return RecurringPaymentForm_Paypal(request.POST, request=request, subscription=subscription, label_suffix='') if request.method == 'POST' else RecurringPaymentForm_Paypal(request=request, subscription=subscription, label_suffix='')
    elif subscription.gateway.is_stripe():
        form = RecurringPaymentForm_Stripe(request.POST, request=request, subscription=subscription, label_suffix='') if request.method == 'POST' else RecurringPaymentForm_Stripe(request=request, subscription=subscription, label_suffix='')
        form.order_fields(
            ['subscription_id', 'currency', 'recurring_amount', 'billing_cycle_now'])
        return form
    elif subscription.gateway.is_offline():
        return RecurringPaymentForm_Offline(request.POST, request=request, subscription=subscription, label_suffix='') if request.method == 'POST' else RecurringPaymentForm_Offline(request=request, subscription=subscription, label_suffix='')
    else:
        raise ValueError(_('The Provided gateway has not been implemented yet'))


def getEditRecurringPaymentHtml(subscription):
    if not subscription:
        raise ValueError(_('Needs subscription to init the edit form for the recurring payment'))
    if subscription.gateway.is_2c2p():
        return 'donations/edit_2c2p_recurring_payment_form.html'
    elif subscription.gateway.is_paypal():
        return 'donations/edit_paypal_recurring_payment_form.html'
    elif subscription.gateway.is_stripe():
        return 'donations/edit_stripe_recurring_payment_form.html'
    elif subscription.gateway.is_offline():
        return 'donations/edit_offline_recurring_payment_form.html'
    else:
        raise ValueError(_('The Provided gateway has not been implemented yet'))


def getAPICapabilitiesFromPaymentGateway(paymentGateway):
    if paymentGateway.title == GATEWAY_STRIPE:
        return STRIPE_API_CAPABILITIES
    elif paymentGateway.title == GATEWAY_PAYPAL:
        return PAYPAL_API_CAPABILITIES
    elif paymentGateway.title == GATEWAY_2C2P:
        return _2C2P_API_CAPABILITIES
    elif paymentGateway.title == GATEWAY_OFFLINE:
        return OFFLINE_API_CAPABILITIES
    elif paymentGateway.title == GATEWAY_PAYPAL_LEGACY:
        return PAYPAL_LEGACY_API_CAPABILITIES
    else:
        return []


def isGatewayEditSubSupported(gateway):
    if GATEWAY_CAN_EDIT_SUBSCRIPTION in getAPICapabilitiesFromPaymentGateway(gateway):
        return True
    return False


def isGatewayToggleSubSupported(gateway):
    if GATEWAY_CAN_TOGGLE_SUBSCRIPTION in getAPICapabilitiesFromPaymentGateway(gateway):
        return True
    return False


def isGatewayCancelSubSupported(gateway):
    if GATEWAY_CAN_CANCEL_SUBSCRIPTION in getAPICapabilitiesFromPaymentGateway(gateway):
        return True
    return False