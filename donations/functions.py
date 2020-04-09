from pprint import pprint
from site_settings.models import GeneralSettings, Settings2C2P
import secrets
import re
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from pytz import timezone


def raiseObjectNone(message=''):
    raise django.core.exceptions.ObjectDoesNotExist(message)


def isTestMode(request):
    generalSettings = GeneralSettings.for_site(request.site)
    return generalSettings.test_mode


def get2C2PSettings(request):
    return Settings2C2P.for_site(request.site)


def getFullReverseUrl(request, urlname):
    return request.scheme + '://' + request.get_host() + reverse(urlname)


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


def gen_order_prefix_2c2p():
    return 'P' + secrets.token_hex(7)


def getSuperUserTimezone():
    """ 
    For the calculation of correct datetimes for payment gateways on when exactly to charge recurring payments 
    Assumption: the superuser has set the correct local timezone which matches with the payment gateway's timezone setting
    """
    su = User.objects.filter(is_superuser=1)[0]
    if not su:
        raiseObjectNone('Superuser not found')
    return su.wagtail_userprofile.get_current_time_zone()


def getNextDateFromRecurringInterval(days, format):
    tz = timezone(getSuperUserTimezone())
    loc_dt = datetime.now(tz)
    new_dt = loc_dt + timedelta(days=days)
    return new_dt.strftime(format)
