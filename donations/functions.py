from pprint import pprint
from site_settings.models import GeneralSettings
import secrets
import re


def raiseObjectNone(message=''):
    raise django.core.exceptions.ObjectDoesNotExist(message)


def isTestMode(request):
    generalSettings = GeneralSettings.for_site(request.site)
    return generalSettings.test_mode


def gen_order_id(gateway=None):
    if not gateway:
        raiseObjectNone('Please provide a payment gateway object')
    if gateway.is_2c2p():
        order_id = secrets.token_hex(10)
    elif gateway.is_paypal():
        order_id = secrets.token_hex(16)
    elif gateway.is_stripe():
        order_id = secrets.token_hex(16)
    else:
        order_id = secrets.token_hex(16)
    return order_id
