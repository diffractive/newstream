import re
import site_settings
import sys
import os
import uuid
import logging
logger = logging.getLogger('newstream')
from pytz import timezone
from pprint import pprint
from datetime import datetime
from hashlib import blake2b
from decimal import Decimal, ROUND_HALF_UP
import django.conf as conf
from django.conf import settings
from django.urls import reverse
from django.core.mail import get_connection, EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from wagtail.core.models import Site

from site_settings.models import SiteSettings
from newstream_user.models import UserMeta
User = get_user_model()


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Truncate microseconds so that tokens are consistent even if the
        # database doesn't support microseconds.
        joined_timestamp = user.date_joined.replace(microsecond=0, tzinfo=None)
        return str(user.pk) + str(joined_timestamp) + str(timestamp)


evTokenGenerator = EmailVerificationTokenGenerator()


def _debug(msg):
    logger.debug(msg)


def _error(msg):
    logger.error(msg)


def _exception(msg):
    logger.exception(msg)


def object_to_json(json_data):
    """
    Function to print all json data in an organized readable manner
    """
    result = {}
    itr = json_data.__dict__.items() if not isinstance(json_data, dict) else json_data.items()
    for key,value in itr:
        # Skip internal attributes.
        if key.startswith("__"):
            continue
        result[key] = array_to_json_array(value) if isinstance(value, list) else\
                    object_to_json(value) if not is_primittive(value) else\
                        value
    return result


def array_to_json_array(json_array):
    result =[]
    if isinstance(json_array, list):
        for item in json_array:
            result.append(object_to_json(item) if  not is_primittive(item) \
                            else array_to_json_array(item) if isinstance(item, list) else item)
    return result


def is_primittive(data):
    return isinstance(data, str) or isinstance(data, int)


def round_half_up(value, precision=0):
    '''
    Returns a Decimal instance constructed from the value and precision provided
    Decimal instances can be constructed from integers, strings, floats, or tuples. Construction from an integer or a float performs an exact conversion of the value of that integer or float. Decimal numbers include special values such as NaN which stands for “Not a number”, positive and negative Infinity, and -0.
    '''
    exponent = '1.' + '0' * precision if precision > 0 else '1'
    return Decimal(value).quantize(Decimal(exponent), rounding=ROUND_HALF_UP)


def get_default_site():
    return Site.objects.get(is_default_site=True)


def get_site_url():
    """
    Returns the site's hostname with the correct protocol prefixed
    the HTTPS environment variable is being set to 'on' in wsgi.py
    """
    default_site = get_default_site()
    return ('https' if os.environ.get('HTTPS') == 'on' else 'http') + '://' + re.sub(r'^(https://|http://)', '', default_site.hostname)


def reverse_with_site_url(urlname, kwargs=None):
    """
    Returns the site url concatenated with the relative url fetched from reverse(urlname, kwargs=kwargs)
    """
    site_url = get_site_url()
    return site_url + reverse(urlname, kwargs=kwargs)


def uuid4_str():
    return str(uuid.uuid4())


def get_site_name():
    default_site = get_default_site()
    return default_site.site_name if default_site.site_name else '[SiteName]'


def get_site_settings_from_default_site():
    """
    The prerequisites for this method are:
    1. the default site object should be created at the start of wagtail core migrations.
    2. There should be one site which is also the default site, ideally no other sites are allowed exist.
    """

    site = get_default_site()
    instance = SiteSettings.for_site(site)

    # get from environment variables if nothing is defined in the database
    for field in instance.fields:
        db_value = getattr(instance, field, None)
        if isinstance(db_value, str) and (db_value == "" or db_value == "None") or db_value == None:
            # map to the corresponding env var key
            envkey = "NEWSTREAM_"+field.upper()
            settings_value = getattr(settings, envkey, None)
            # set attribute of SiteSettings instance using value from env var
            if settings_value is not None:
                setattr(instance, field, settings_value)
    
    return instance


def trans_next_url(next_url, lang_code):
    parts = next_url.split('/')
    lang_codes = [x[0] for x in settings.LANGUAGES]
    if parts[1] in lang_codes:
        parts[1] = lang_code
    else:
        parts.insert(1, lang_code)
    trans_url = '/'.join(parts)
    return trans_url


def process_user_meta(post_dict):
    user_metas = []
    for key, val in post_dict.items():
        usermeta_key = re.match("^usermeta_([a-z_-]+)$", key)
        usermetalist_key = re.match("^usermetalist_([a-z_-]+)$", key)
        if usermeta_key:
            user_metas.append(UserMeta(
                field_key=usermeta_key.group(1), field_value=val))
        elif usermetalist_key:
            listval = post_dict.getlist(key)
            if len(listval) > 0:
                # using comma-linebreak as the separator
                user_metas.append(UserMeta(
                    field_key=usermetalist_key.group(1), field_value=',\n'.join(listval)))
    return user_metas


def raiseObjectNone(message=''):
    raise ObjectDoesNotExist(message)


def getSuperUserTimezone():
    """
    For the calculation of correct datetimes for payment gateways on when exactly to charge recurring payments
    Assumption: the superuser has set the correct local timezone which matches with the payment gateway's timezone setting
    """
    su = User.objects.get(is_superuser=1)
    if not su:
        raiseObjectNone(_('Superuser not found'))
    if su.wagtail_userprofile.get_current_time_zone():
        return su.wagtail_userprofile.get_current_time_zone()
    return 'UTC'


def getUserTimezone(user):
    if user.wagtail_userprofile.get_current_time_zone():
        return user.wagtail_userprofile.get_current_time_zone()
    return 'UTC'

def getAdminTodayDate(format):
    tz = timezone(getSuperUserTimezone())
    loc_dt = datetime.now(tz)
    return loc_dt.strftime(format)


def getSuperUserEmail():
    """ For sending out password reset emails """
    su = User.objects.get(is_superuser=1)
    if not su:
        raiseObjectNone(_('Superuser not found'))
    return su.email


def set_default_from_email():
    site_settings = get_site_settings_from_default_site()
    conf.settings.DEFAULT_FROM_EMAIL = site_settings.default_from_email


def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None,
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    For more details on the various smtp exceptions and source code on how it handles them, see:
    https://docs.python.org/3/library/smtplib.html#module-smtplib

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


def generateIDSecretHash(id):
    h = blake2b(digest_size=20)
    ogbytes = (str(id) + settings.SECRET_KEY).encode()
    h.update(ogbytes)
    return h.hexdigest()


def printvars(obj):
    print("---Vars(obj)---", flush=True)
    pprint(vars(obj))
    sys.stdout.flush()
