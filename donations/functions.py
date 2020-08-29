import os
import secrets
import re
import traceback
from pprint import pprint
from datetime import datetime, timedelta
from pytz import timezone
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from allauth.account.utils import send_email_confirmation

from .includes.currency_dictionary import currency_dict
from .templates.donations.email_templates.plain_texts import get_new_donation_text, get_donation_receipt_text
from newstream.functions import getSiteSettings, getDefaultFromEmail, setDefaultFromEmail, getSuperUserTimezone
from newstream.functions import evTokenGenerator, raiseObjectNone, getSiteName
from newstream.templates.registration.email_templates.plain_texts import get_verify_your_email_text
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


def formatAmountCentsDecimal(amount_cents, currency_code):
    if amount_cents.is_integer():
        formatted_str = str(int(amount_cents))
        return formatted_str
    currency = getCurrencyDictAt(currency_code)
    decimal_places = (currency['setting']['number_decimals'] -
                      2) if currency and currency['setting']['number_decimals'] >= 2 else 0
    formatted_str = '{:.{decimals}f}'.format(
        amount_cents, decimals=decimal_places)
    return formatted_str


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


def sendDonationNotifToAdmins(request, donation):
    siteSettings = getSiteSettings(request)
    admin_list = [
        admin_email.email for admin_email in siteSettings.admin_emails.all()]
    try:
        send_mail(
            "New Donation",
            get_new_donation_text(
                request, donation),
            getDefaultFromEmail(request),
            admin_list,  # requires admin list to be set in siteSettings
            html_message=render_to_string('donations/email_templates/new_donation.html', context={
                'donation': donation}, request=request)
        )
    except Exception as e:
        print("Cannot send emails to admins: "+str(e), flush=True)


def sendDonationReceipt(request, donation):
    try:
        send_mail(
            "Donation Receipt",
            get_donation_receipt_text(
                request, donation),
            getDefaultFromEmail(request),
            [donation.user.email],
            html_message=render_to_string('donations/email_templates/donation_receipt.html', context={
                'donation': donation}, request=request)
        )
    except Exception as e:
        print("Cannot send receipt to user: "+str(e), flush=True)


def sendVerificationEmail(request, user):
    setDefaultFromEmail(request)
    # allauth's email confirmation uses DEFAULT_FROM_EMAIL
    send_email_confirmation(request, user, True)
