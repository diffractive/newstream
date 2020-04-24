import os
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import PasswordResetTokenGenerator


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


def raiseObjectNone(message=''):
    raise ObjectDoesNotExist(message)
