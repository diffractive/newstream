import os
import json
import jsonpickle
from hashlib import blake2b
from django.conf import settings
from django.urls import reverse
from django.core.mail import get_connection, EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from site_settings.models import GlobalSettings


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


def getGlobalSettings(request):
    return GlobalSettings.for_site(request.site)


def raiseObjectNone(message=''):
    raise ObjectDoesNotExist(message)


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


def pickleprint(obj):
    serialized = jsonpickle.encode(obj)
    print(json.dumps(json.loads(serialized), indent=4))
