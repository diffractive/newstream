from django.dispatch import receiver
from django.conf import settings
from django.utils import translation

from allauth.account.signals import user_logged_in, user_signed_up
from django.contrib import messages

from newstream.functions import trans_next_url
from donations.email_functions import sendAccountCreatedNotifToAdmins
from donations.models import SubscriptionInstance, STATUS_CANCELLED, STATUS_PAYMENT_FAILED


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
    
    # show respective warnings if user has failing/failed recurring donations
    failed_subs = SubscriptionInstance.objects.filter(user=user, recurring_status=STATUS_CANCELLED, cancel_reason=SubscriptionInstance.CancelReason.PAYMENTS_FAILED, deleted=False)
    failing_subs = SubscriptionInstance.objects.filter(user=user, recurring_status=STATUS_PAYMENT_FAILED, deleted=False)
    if len(failed_subs) + len(failing_subs) > 1:
        messages.add_message(request, messages.ERROR, "You have multiple recently failed recurring payments. Please reactivate your recurring donations.", extra_tags="static-notif cta-manage-donations")    
    elif len(failed_subs) == 1:
        messages.add_message(request, messages.ERROR, "Your recurring donation has been cancelled due to multiple failed payments. Please create a new recurring donation.", extra_tags="static-notif cta-new-donation")    
    elif len(failing_subs) == 1:
        request.session["sub_instance_id"] = failing_subs[0].id
        messages.add_message(request, messages.WARNING, "A recent payment of your recurring donation has failed. Please update the corresponding payment method.", extra_tags="static-notif cta-update-card")


@receiver(user_signed_up)
def newstream_user_signed_up(sender, request, user, **kwargs):
    # email notifications
    sendAccountCreatedNotifToAdmins(user)
