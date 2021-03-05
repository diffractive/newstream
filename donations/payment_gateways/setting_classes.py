from paypalcheckoutsdk.core import SandboxEnvironment, LiveEnvironment

from newstream.functions import getSiteSettings


class Settings2C2P:
    def __init__(self, sandbox_mode, merchant_id, secret_key):
        self.sandbox_mode = sandbox_mode
        self.merchant_id = merchant_id
        self.secret_key = secret_key


class SettingsPayPal:
    def __init__(self, sandbox_mode, product_id, client_id, secret_key, webhook_id, environment, api_url):
        self.sandbox_mode = sandbox_mode
        self.product_id = product_id
        self.client_id = client_id
        self.secret_key = secret_key
        self.webhook_id = webhook_id
        self.environment = environment
        self.api_url = api_url


class SettingsPayPalLegacy:
    def __init__(self, sandbox_mode, ipn_url):
        self.sandbox_mode = sandbox_mode
        self.ipn_url = ipn_url


class SettingsStripe:
    def __init__(self, sandbox_mode, webhook_secret, product_id, publishable_key, secret_key):
        self.sandbox_mode = sandbox_mode
        self.webhook_secret = webhook_secret
        self.product_id = product_id
        self.publishable_key = publishable_key
        self.secret_key = secret_key


class SettingsOffline:
    def __init__(self, sandbox_mode, offline_instructions_text, offline_thankyou_text):
        self.sandbox_mode = sandbox_mode
        self.offline_instructions_text = offline_instructions_text
        self.offline_thankyou_text = offline_thankyou_text


def get2C2PSettings(request):
    siteSettings = getSiteSettings(request)
    if (siteSettings.sandbox_mode):
        return Settings2C2P(siteSettings.sandbox_mode, siteSettings._2c2p_testing_merchant_id, siteSettings._2c2p_testing_secret_key)
    return Settings2C2P(siteSettings.sandbox_mode, siteSettings._2c2p_merchant_id, siteSettings._2c2p_secret_key)


def getPayPalSettings(request):
    siteSettings = getSiteSettings(request)
    if (siteSettings.sandbox_mode):
        environment = SandboxEnvironment(client_id=siteSettings.paypal_sandbox_api_client_id, client_secret=siteSettings.paypal_sandbox_api_secret_key)
        api_url = 'https://api-m.sandbox.paypal.com'
        return SettingsPayPal(siteSettings.sandbox_mode, siteSettings.paypal_sandbox_api_product_id, siteSettings.paypal_sandbox_api_client_id, siteSettings.paypal_sandbox_api_secret_key, siteSettings.paypal_sandbox_api_webhook_id, environment, api_url)
    environment = LiveEnvironment(client_id=siteSettings.paypal_api_client_id, client_secret=siteSettings.paypal_api_secret_key)
    api_url = 'https://api-m.paypal.com'
    return SettingsPayPal(siteSettings.sandbox_mode, siteSettings.paypal_api_product_id, siteSettings.paypal_api_client_id, siteSettings.paypal_api_secret_key, siteSettings.paypal_api_webhook_id, environment, api_url)


def getPayPalLegacySettings(request):
    siteSettings = getSiteSettings(request)
    if (siteSettings.sandbox_mode):
        ipn_url = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'
        return SettingsPayPalLegacy(siteSettings.sandbox_mode, ipn_url)
    ipn_url = 'https://ipnpb.paypal.com/cgi-bin/webscr'
    return SettingsPayPalLegacy(siteSettings.sandbox_mode, ipn_url)


def getStripeSettings(request):
    siteSettings = getSiteSettings(request)
    if (siteSettings.sandbox_mode):
        return SettingsStripe(siteSettings.sandbox_mode, siteSettings.stripe_webhook_secret, siteSettings.stripe_testing_product_id, siteSettings.stripe_testing_api_publishable_key, siteSettings.stripe_testing_api_secret_key)
    return SettingsStripe(siteSettings.sandbox_mode, siteSettings.stripe_webhook_secret, siteSettings.stripe_product_id, siteSettings.stripe_api_publishable_key, siteSettings.stripe_api_secret_key)


def getOfflineSettings(request):
    ''' Seems there's no need to have separate sets of sandbox/live settings here '''
    siteSettings = getSiteSettings(request)
    return SettingsOffline(siteSettings.sandbox_mode, siteSettings.offline_instructions_text, siteSettings.offline_thankyou_text)