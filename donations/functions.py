import os
import secrets
import re
import html
from pprint import pprint
from datetime import datetime, timedelta
from pytz import timezone
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from .includes.currency_dictionary import currency_dict
from newstream.functions import getSiteSettings, getSuperUserTimezone
from newstream.functions import evTokenGenerator, raiseObjectNone, getSiteName
from donations.models import DonationMeta


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
    siteSettings = getSiteSettings(request)
    return siteSettings.sandbox_mode


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


def process_donation_meta(request):
    donation_metas = []
    for key, val in request.POST.items():
        donationmeta_key = re.match("^donationmeta_([a-z_-]+)$", key)
        donationmetalist_key = re.match("^donationmetalist_([a-z_-]+)$", key)
        if donationmeta_key:
            donation_metas.append(DonationMeta(
                field_key=donationmeta_key.group(1), field_value=val))
        elif donationmetalist_key:
            listval = request.POST.getlist(key)
            if len(listval) > 0:
                # using comma-linebreak as the separator
                donation_metas.append(DonationMeta(
                    field_key=donationmetalist_key.group(1), field_value=',\n'.join(listval)))
    return donation_metas


def displayDonationAmountWithCurrency(donation):
    currency_set = getCurrencyDictAt(donation.currency)
    return mark_safe(html.unescape(currency_set['symbol']+" "+str(donation.donation_amount if currency_set['setting']['number_decimals'] != 0 else int(donation.donation_amount))))


def displayRecurringAmountWithCurrency(subscription):
    currency_set = getCurrencyDictAt(subscription.currency)
    return mark_safe(html.unescape(currency_set['symbol']+" "+str(subscription.recurring_amount if currency_set['setting']['number_decimals'] != 0 else int(subscription.recurring_amount))))
