from django.db import models
from django.contrib.auth.models import AbstractUser

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from allauth.account.models import EmailAddress


class UserMeta(models.Model):
    user = ParentalKey(
        'User',
        related_name='metas',
        on_delete=models.CASCADE,
    )
    field_key = models.CharField(max_length=255)
    field_value = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.field_key


class User(AbstractUser, ClusterableModel):
    # todo: let admin view/edit user meta at admin panel
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

    def optInMailing(self):
        return 'Yes' if self.opt_in_mailing_list else 'No'

    def optInMailingIcon(self):
        return '<span class="yes-icon block"></span>' if self.opt_in_mailing_list else '<span class="no-icon block"></span>'

    @is_email_verified.setter
    def is_email_verified(self, val):
        pass

    @property
    def fullname(self):
        return ' '.join([self.first_name, self.last_name])

    @fullname.setter
    def fullname(self, val):
        pass

    class Meta:
        ordering = ['-date_joined']