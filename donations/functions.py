import secrets
import re
import html
from datetime import datetime, timedelta, timezone as dt_timezone
from pytz import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .includes.currency_dictionary import currency_dict
from newstream.functions import getSiteSettings, getSuperUserTimezone, _debug, getSiteSettings_from_default_site
from donations.models import DonationMeta, TempDonationMeta
from newstream_user.models import UserSubscriptionUpdatesLog, UserDonationUpdatesLog


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


def currencyCodeToKey(code):
    for key, val in currency_dict.items():
        if val['code'] == str(code):
            return key
    return None


def isTestMode(request):
    siteSettings = getSiteSettings(request)
    return siteSettings.sandbox_mode


def getDonationEmail(donation):
    if donation.user:
        return donation.user.email
    else:
        return donation.guest_email


def isUpdateSubsFrequencyLimitationPassed(gatewayManager):
    if gatewayManager.global_settings.limit_fiveactions_per_fivemins:
        # get count of the actions carried out by the same donor in the last 5 minutes
        nowdt = datetime.now(dt_timezone.utc)
        fiveminsbf = nowdt - timedelta(minutes=5)
        count = UserSubscriptionUpdatesLog.objects.filter(user=gatewayManager.subscription.user, created_at__gte=fiveminsbf).count()
        _debug('Count of Subscription Actions done by {} within five minutes: {}'.format(gatewayManager.subscription.user.fullname, count))
        if count >= 5:
            return False
    return True


def addUpdateSubsActionLog(subscription, action_type, action_notes='', user=None):
    ''' This might be called either by donor or by admin'''
    log = UserSubscriptionUpdatesLog(
        user=subscription.user if user == None else user,
        subscription=subscription,
        action_type=action_type,
        action_notes=action_notes
    )
    log.save()


def addUpdateDonationActionLog(donation, action_type, action_notes='', user=None):
    ''' This might be called either by donor or by admin'''
    log = UserDonationUpdatesLog(
        user=donation.user if user == None else user,
        donation=donation,
        action_type=action_type,
        action_notes=action_notes
    )
    log.save()


def gen_transaction_id(gateway=None):
    if not gateway:
        raise ValueError(_('Please provide a payment gateway object'))
    if gateway.is_2c2p():
        transaction_id = secrets.token_hex(10)
    elif gateway.is_paypal():
        transaction_id = secrets.token_hex(16)
    elif gateway.is_stripe():
        transaction_id = secrets.token_hex(16)
    else:
        transaction_id = secrets.token_hex(16)
    return transaction_id


def gen_order_prefix_2c2p():
    return 'P' + secrets.token_hex(7)


def getNextDateFromRecurringInterval(days, date_format):
    tz = timezone(getSuperUserTimezone())
    loc_dt = datetime.now(tz)
    new_dt = loc_dt + timedelta(days=days)
    return new_dt.strftime(date_format)


def getRecurringDateNextMonth(date_format):
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
    return nextmonthdate.strftime(date_format)


def process_temp_donation_meta(request):
    donation_metas = []
    for key, val in request.POST.items():
        donationmeta_key = re.match("^donationmeta_([a-z_-]+)$", key)
        donationmetalist_key = re.match("^donationmetalist_([a-z_-]+)$", key)
        if donationmeta_key:
            donation_metas.append(TempDonationMeta(
                field_key=donationmeta_key.group(1), field_value=val))
        elif donationmetalist_key:
            listval = request.POST.getlist(key)
            if len(listval) > 0:
                # using comma-linebreak as the separator
                donation_metas.append(TempDonationMeta(
                    field_key=donationmetalist_key.group(1), field_value=',\n'.join(listval)))
    return donation_metas


def displayGateway(instance):
    ''' instance can be either TempDonation, Donation or Subscription'''
    siteSettings = getSiteSettings_from_default_site()
    return getattr(siteSettings, instance.gateway.frontend_label_attr_name, instance.gateway.title)


def displayAmountWithCurrency(currency_code, amount, trim_decimals=False):
    currency_set = getCurrencyDictAt(currency_code)
    if trim_decimals and (amount % 1 == 0):
        amount = int(amount)
    return mark_safe(html.unescape(currency_code+" "+currency_set['symbol']+str(amount if currency_set['setting']['number_decimals'] != 0 else int(amount))))

def displayDonationAmountWithCurrency(donation):
    return displayAmountWithCurrency(donation.currency, donation.donation_amount)


def displayRecurringAmountWithCurrency(subscription):
    return displayAmountWithCurrency(subscription.currency, subscription.recurring_amount)
