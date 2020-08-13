from django.shortcuts import render
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import translation
from django.http import HttpResponseRedirect
# from django.utils.encoding import iri_to_uri

from allauth.account.signals import user_logged_in

from newstream.functions import trans_next_url
# User = get_user_model()


@receiver(user_logged_in)
def newstream_user_logged_in(sender, request, response, user, **kwargs):
    # if 'user' in kwargs.keys() and 'request' in kwargs.keys() and 'response' in kwargs.keys():
        # user = kwargs['user']
    if user.language_preference:
        user_language = user.language_preference
        translation.activate(user_language)
        request.LANGUAGE_CODE = translation.get_language()
        response['Location'] = trans_next_url(response.url, user_language)
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME, user_language)
