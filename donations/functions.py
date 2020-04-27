import os
import secrets
import re
import traceback
from pprint import pprint
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from site_settings.models import Settings2C2P
from omp.functions import getGlobalSettings
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from pytz import timezone
from .includes.currency_dictionary import currency_dict
from .templates.donations.email_templates.plain_texts import get_new_donation_text, get_donation_receipt_text
from omp.functions import evTokenGenerator, raiseObjectNone, getFullReverseUrl, getSiteName
from omp.templates.registration.email_templates.plain_texts import get_verify_your_email_text
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
    globalSettings = getGlobalSettings(request)
    return globalSettings.test_mode


def get2C2PSettings(request):
    return Settings2C2P.for_site(request.site)


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


def sendDonationNotifToAdmins(request, donation):
    globalSettings = getGlobalSettings(request)
    admin_list = [
        admin_email.email for admin_email in globalSettings.admin_emails.all()]
    try:
        send_mail(
            "New Donation",
            get_new_donation_text(
                request, donation),
            getSuperUserEmail(),
            admin_list,  # requires admin list to be set in globalsettings
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
            getSuperUserEmail(),
            [donation.donor.email],
            html_message=render_to_string('donations/email_templates/donation_receipt.html', context={
                'donation': donation}, request=request)
        )
    except Exception as e:
        print("Cannot send receipt to donor: "+str(e), flush=True)


def sendVerificationEmail(request, user):
    try:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = evTokenGenerator.make_token(user)
        fullurl = getFullReverseUrl(
            request, 'verify-email', kwargs={'uidb64': uid, 'token': token})
        ms = send_mail(
            "Please verify your email at "+getSiteName(request),
            get_verify_your_email_text(
                request, user.fullname, fullurl),
            getSuperUserEmail(),
            [user.email],
            html_message=render_to_string('registration/email_templates/verify_your_email.html', context={
                'fullname': user.fullname, 'fullurl': fullurl}, request=request)
        )
        print("Number of email verifications sent: " +
              str(ms), flush=True)
    except Exception as e:
        print("Cannot send verification email to donor: " +
              str(e), flush=True)
        print(traceback.format_exc(), flush=True)
