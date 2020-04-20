from django.db import models
from django_use_email_as_username.models import BaseUser, BaseUserManager


class User(BaseUser):
    is_email_verified = models.BooleanField(default=False)
    objects = BaseUserManager()

    def email_verification_status(self):
        if self.is_email_verified:
            return '&#x2714;'
        return '&#x2718;'

    @property
    def fullname(self):
        return ' '.join([self.first_name, self.last_name])

    @fullname.setter
    def fullname(self, val):
        pass
