from django.dispatch import receiver
from django.conf import settings
from django.utils import translation

from allauth.account.signals import user_logged_in, user_signed_up

from newstream.functions import trans_next_url
from donations.email_functions import sendAccountCreatedNotifToAdmins


# @receiver(user_logged_in)
# def newstream_user_logged_in(sender, request, response, user, **kwargs):
#     # if 'user' in kwargs.keys() and 'request' in kwargs.keys() and 'response' in kwargs.keys():
#     # user = kwargs['user']
#     if user.language_preference:
#         user_language = user.language_preference
#         translation.activate(user_language)
#         request.LANGUAGE_CODE = translation.get_language()
#         response['Location'] = trans_next_url(response.url, user_language)
#         response.set_cookie(
#             settings.LANGUAGE_COOKIE_NAME, user_language)


@receiver(user_signed_up)
def newstream_user_signed_up(sender, request, user, **kwargs):
    # email notifications
    sendAccountCreatedNotifToAdmins(user)
