import stripe
from decimal import Decimal

from donations.payment_gateways.setting_classes import getStripeSettings
from donations.functions import getCurrencyDictAt
from django.conf import settings


def initStripeApiKey():
    stripeSettings = getStripeSettings()
    stripe.api_key = stripeSettings.secret_key
    stripe.api_base = settings.STRIPE_API_BASE or stripe.api_base
    if settings.STRIPE_API_VERSION:
        stripe.api_version = settings.STRIPE_API_VERSION
    # see Network errors: https://stripe.com/docs/error-handling#network-errors
    stripe.max_network_retries = 2


def formatDonationAmount(amount, currency_code):
    currency = getCurrencyDictAt(currency_code)
    if currency['setting']['number_decimals'] != 0:
        # amount must now be a whole integer since number_decimals is at most 2
        amount *= 100
    formatted_str = str(int(amount))
    return formatted_str


def formatDonationAmountFromGateway(amount_str, currency_code):
    currency = getCurrencyDictAt(currency_code)
    if currency['setting']['number_decimals'] != 0:
        # need to divide amount by 100
        return Decimal(amount_str)/100
    return Decimal(amount_str)
