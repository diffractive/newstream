from allauth.account.signals import email_confirmed
from django.dispatch import receiver


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.is_email_verified = True

    user.save()
