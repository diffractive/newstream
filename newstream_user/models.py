from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.models import EmailAddress


class User(AbstractUser):
    opt_in_mailing_list = models.BooleanField(default=False)

    def email_verification_status(self):
        if self.is_email_verified:
            return '(Verified)'
        return '(Unverified)'

    @property
    def is_email_verified(self):
        ''' It is the primary email which decides this user's email verification status. '''
        return EmailAddress.objects.filter(
            user=self, primary=True, verified=True).exists()

    @is_email_verified.setter
    def is_email_verified(self, val):
        pass

    @property
    def fullname(self):
        return ' '.join([self.first_name, self.last_name])

    @fullname.setter
    def fullname(self, val):
        pass
