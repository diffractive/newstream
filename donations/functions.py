import os
import secrets
import re
from pprint import pprint
from site_settings.models import GlobalSettings, Settings2C2P
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from pytz import timezone
from .includes.currency_dictionary import currency_dict
from omp.functions import raiseObjectNone
User = get_user_model()


def getCurrencyDict():
    return currency_dict


def getCurrencyDictAt(key):
    if key in currency_dict:
        return currency_dict[key]
    return None


def getCurrencyFromCode(code):
    for key, val in currency_dict.items():
        if val['code'] == str(code):
            return currency_dict[key]
    return None


def isTestMode(request):
    globalSettings = GlobalSettings.for_site(request.site)
    return globalSettings.test_mode


def get2C2PSettings(request):
    return Settings2C2P.for_site(request.site)


def getGlobalSettings(request):
    return GlobalSettings.for_site(request.site)


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
    su = User.objects.get(is_superuser=1)
    if not su:
        raiseObjectNone('Superuser not found')
    return su.wagtail_userprofile.get_current_time_zone()


def getSuperUserEmail():
    """ For sending out password reset emails """
    su = User.objects.get(is_superuser=1)
    if not su:
        raiseObjectNone('Superuser not found')
    return su.email


def getNextDateFromRecurringInterval(days, format):
    tz = timezone(getSuperUserTimezone())
    loc_dt = datetime.now(tz)
    new_dt = loc_dt + timedelta(days=days)
    return new_dt.strftime(format)


def getRecurringDateNextMonth(format):
    try:
        tz = timezone(getSuperUserTimezone())
        loc_dt = datetime.now(tz)
        nextmonthdate = loc_dt.replace(month=loc_dt.month+1)
    except ValueError:
        if loc_dt.month == 12:
            nextmonthdate = loc_dt.replace(year=loc_dt.year+1, month=1)
        else:
            """
            next month is too short to have "same date", recur at start of the next-next month
            just like how paypal solve this: https://developer.paypal.com/docs/paypal-payments-standard/integration-guide/subscription-billing-cycles/
            """
            nextmonthdate = loc_dt.replace(month=loc_dt.month+2, day=1)
    return nextmonthdate.strftime(format)
