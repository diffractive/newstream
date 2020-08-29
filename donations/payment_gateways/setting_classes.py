from newstream.functions import getSiteSettings


class Settings2C2P:
    def __init__(self, merchant_id, secret_key):
        self.merchant_id = merchant_id
        self.secret_key = secret_key


class SettingsStripe:
    def __init__(self, webhook_secret, product_id, publishable_key, secret_key):
        self.webhook_secret = webhook_secret
        self.product_id = product_id
        self.publishable_key = publishable_key
        self.secret_key = secret_key


def get2C2PSettings(request):
    siteSettings = getSiteSettings(request)
    if (siteSettings.sandbox_mode):
        return Settings2C2P(siteSettings._2c2p_testing_merchant_id, siteSettings._2c2p_testing_secret_key)
    return Settings2C2P(siteSettings._2c2p_merchant_id, siteSettings._2c2p_secret_key)


def getStripeSettings(request):
    siteSettings = getSiteSettings(request)
    if (siteSettings.sandbox_mode):
        return SettingsStripe(siteSettings.stripe_webhook_secret, siteSettings.stripe_product_id, siteSettings.stripe_testing_api_publishable_key, siteSettings.stripe_testing_api_secret_key)
    return SettingsStripe(siteSettings.stripe_webhook_secret, siteSettings.stripe_product_id, siteSettings.stripe_api_publishable_key, siteSettings.stripe_api_secret_key)
