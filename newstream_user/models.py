from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    opt_in_mailing_list = models.BooleanField(default=False)

    def email_verification_status(self):
        if self.is_email_verified:
            return '(Verified)'
        return '(Unverified)'

    @property
    def fullname(self):
        return ' '.join([self.first_name, self.last_name])

    @fullname.setter
    def fullname(self, val):
        pass
