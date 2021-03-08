from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from allauth.account.models import EmailAddress

SUBS_ACTION_UPDATE = 'update-subscription'
SUBS_ACTION_PAUSE = 'pause-subscription'
SUBS_ACTION_RESUME = 'resume-subscription'
SUBS_ACTION_CANCEL = 'cancel-subscription'
SUBS_ACTION_MANUAL = 'manual-update-status'
DONATION_ACTION_MANUAL = 'manual-update-status'


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


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
        verbose_name = _('User Meta')
        verbose_name_plural = _('User Metas')

    def __str__(self):
        return self.field_key


class UserSubscriptionUpdatesLog(models.Model):
    SUBS_ACTION_CHOICES = [
        (SUBS_ACTION_UPDATE, SUBS_ACTION_UPDATE),
        (SUBS_ACTION_PAUSE, SUBS_ACTION_PAUSE),
        (SUBS_ACTION_RESUME, SUBS_ACTION_RESUME),
        (SUBS_ACTION_CANCEL, SUBS_ACTION_CANCEL),
        (SUBS_ACTION_MANUAL, SUBS_ACTION_MANUAL),
    ]
    user = ParentalKey(
        'User',
        related_name='subsupdateslogs',
        on_delete=models.CASCADE,
    )
    subscription = models.ForeignKey(
        'donations.Subscription',
        on_delete=models.SET_NULL,
        null=True
    )
    action_type = models.CharField(
        max_length=255, choices=SUBS_ACTION_CHOICES, null=True)
    action_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = _('User Subscription Updates Log')
        verbose_name_plural = _('User Subscription Updates Logs')


class UserDonationUpdatesLog(models.Model):
    DONATION_ACTION_CHOICES = [
        (DONATION_ACTION_MANUAL, DONATION_ACTION_MANUAL),
    ]
    user = ParentalKey(
        'User',
        related_name='donationupdateslogs',
        on_delete=models.CASCADE,
    )
    donation = models.ForeignKey(
        'donations.Donation',
        on_delete=models.SET_NULL,
        null=True
    )
    action_type = models.CharField(
        max_length=255, choices=DONATION_ACTION_CHOICES, null=True)
    action_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = _('User Donation Updates Log')
        verbose_name_plural = _('User Donation Updates Logs')


class User(AbstractUser, ClusterableModel):
    # todo: let admin view/edit user meta at admin panel
    username = None
    email = models.EmailField(_('email address'), unique=True)
    opt_in_mailing_list = models.BooleanField(default=False)
    language_preference = models.CharField(
        max_length=10, choices=settings.LANGUAGES, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    autocomplete_search_field = 'email'

    objects = CustomUserManager()

    def autocomplete_label(self):
        return self.email

    def email_verification_status(self):
        if self.is_email_verified:
            return _('(Verified)')
        return _('(Unverified)')

    @property
    def is_email_verified(self):
        ''' It is the primary email which decides this user's email verification status. '''
        return EmailAddress.objects.filter(
            user=self, primary=True, verified=True).exists()

    def optInMailing(self):
        return _('Yes') if self.opt_in_mailing_list else _('No')

    def optInMailingIcon(self):
        return '<span class="yes-icon block"></span>' if self.opt_in_mailing_list else '<span class="no-icon block"></span>'

    @is_email_verified.setter
    def is_email_verified(self, val):
        pass

    @property
    def fullname(self):
        return ' '.join([self.first_name, self.last_name]) if self.first_name and self.last_name else self.email

    @fullname.setter
    def fullname(self, val):
        pass

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-date_joined']
        verbose_name = _('User')
        verbose_name_plural = _('Users')
