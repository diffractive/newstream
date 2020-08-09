import re
import os
import json
from pprint import pprint
from hashlib import blake2b
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


def getFullReverseUrl(request, urlname, kwargs=None):
    return ('https' if os.environ.get('HTTPS') == 'on' else 'http') + '://' + request.get_host() + reverse(urlname, kwargs=kwargs)


def getSiteName(request):
    return request.site.site_name if request.site.site_name else '[SiteName]'


def getSiteSettings(request):
    return SiteSettings.for_site(request.site)


def getSiteSettings_from_default_site():
    '''
    The usual way of getting the site object is from the request object.
    But since newstream is very unlikely to support multi-site functionality,
    I would provide a method to get the default site object from db directly,
    so that places where code has no access to request can still have access to SiteSettings.

    The prerequisites for this method is the default site object being created at the start of wagtail core migrations.
    '''

    site = Site.objects.get(is_default_site=True)
    return SiteSettings.for_site(site)


def process_user_meta(request):
    user_metas = []
    for key, val in request.POST.items():
        usermeta_key = re.match("^usermeta_([a-z_-]+)$", key)
        usermetalist_key = re.match("^usermetalist_([a-z_-]+)$", key)
        if usermeta_key:
            user_metas.append(UserMeta(
                field_key=usermeta_key.group(1), field_value=val))
        elif usermetalist_key:
            listval = request.POST.getlist(key)
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
    return su.wagtail_userprofile.get_current_time_zone()


def getSuperUserEmail():
    """ For sending out password reset emails """
    su = User.objects.get(is_superuser=1)
    if not su:
        raiseObjectNone(_('Superuser not found'))
    return su.email


def setDefaultFromEmail(request):
    conf.settings.DEFAULT_FROM_EMAIL = getDefaultFromEmail(request)


def getDefaultFromEmail(request):
    siteSettings = getSiteSettings(request)
    return siteSettings.default_from_email if siteSettings.default_from_email else getSuperUserEmail()


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
