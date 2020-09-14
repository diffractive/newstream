import stripe

from donations.payment_gateways.setting_classes import getStripeSettings


def initStripeApiKey(request):
    stripeSettings = getStripeSettings(request)
    stripe.api_key = stripeSettings.secret_key