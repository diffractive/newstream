from decimal import Decimal
import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.contrib.auth import get_user_model
from django.forms.widgets import RadioSelect
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtailautocomplete.edit_handlers import AutocompletePanel
from wagtailmodelchooser import register_model_chooser
from i18nfield.fields import I18nCharField, I18nTextField
from newstream.fields import I18nRichTextField

from site_settings.models import I18nAbstractFormField
from newstream.edit_handlers import ReadOnlyPanel

User = get_user_model()

# Donation/Subscription Statuses
STATUS_ACTIVE = 'active'
STATUS_INACTIVE = 'inactive'
STATUS_COMPLETE = 'complete'
STATUS_REFUNDED = 'refunded'
STATUS_REVOKED = 'revoked'
STATUS_FAILED = 'failed'
STATUS_CANCELLED = 'cancelled'
STATUS_PAUSED = 'paused'
STATUS_PROCESSING = 'processing'
STATUS_PAYMENT_FAILED = 'payment_failed'

# Temp Donation Statuses
STATUS_PENDING = 'pending'
STATUS_PROCESSED = 'processed'


class DonationMetaField(I18nAbstractFormField):
    form = ParentalKey('DonationForm', on_delete=models.CASCADE,
                       related_name='donation_meta_fields')


class AmountStep(models.Model):
    form = ParentalKey('DonationForm', on_delete=models.CASCADE,
                       related_name='amount_steps')
    step = models.DecimalField(default=Decimal(
        0), max_digits=20, decimal_places=2)
    default = models.BooleanField(default=False)

    panels = [
        FieldPanel('step', heading=_('Step')),
        FieldPanel('default', heading=_('Is Default?'), classname='is-default-amount-step'),
    ]

    class Meta:
        unique_together = ['form', 'step']


@register_model_chooser
class DonationForm(ClusterableModel):
    AMOUNT_TYPE_CHOICES = [
        ('fixed', _('Fixed Amount')),
        ('stepped', _('Fixed Steps')),
        ('custom', _('Custom Amount')),
        ('stepped_custom', _('Fixed Steps with Custom Amount Option')),
    ]
    DEFAULT_FREQ_CHOICES = [
        ('onetime', _('One-time')),
        ('monthly', _('Monthly')),
    ]
    title = I18nCharField(max_length=191, unique=True)
    description = I18nTextField(blank=True)
    default_frequency = models.CharField(
        max_length=20, choices=DEFAULT_FREQ_CHOICES, blank=False, default='onetime')
    amount_type = models.CharField(
        max_length=20, choices=AMOUNT_TYPE_CHOICES)
    fixed_amount = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=2,
                                       help_text=_('Define fixed donation amount if you chose "Fixed Amount" for your Amount Type.'))
    max_amount = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=2,
                                       help_text=_('Define maximum amount per donation.'))
    allowed_gateways = models.ManyToManyField('site_settings.PaymentGateway')
    donation_footer_text = I18nRichTextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    panels = [
        FieldPanel('title', heading=_('Title')),
        FieldPanel('description', heading=_('Description')),
        FieldPanel('default_frequency', heading=_('Default Donation Frequency'), widget=RadioSelect),
        FieldPanel('amount_type', heading=_('Donation amount Type')),
        FieldPanel(
            'fixed_amount', heading=_('Define Fixed Donation amount')),
        FieldPanel(
            'max_amount', heading=_('Define Maxium per-Donation amount')),
        InlinePanel('amount_steps', label=_('Fixed Amount Steps'), heading=_('Define Fixed Donation amount Steps'),
                    help_text=_('Define fixed donation amount steps if you chose "Fixed Steps" for your Amount Type.')),
        AutocompletePanel('allowed_gateways', heading=_(
            'Allowed Payment Gateways')),
        InlinePanel('donation_meta_fields', label=_(
            'Donation Meta Fields'), heading=_('Donation Meta Fields')),
        FieldPanel('donation_footer_text', heading=_('Footer Text(Under Donation Details Form)'),
                   help_text=_('Footer text to be displayed under the "Donation Details" Form (Step 2 of payment)'))
    ]

    class Meta:
        ordering = ['title']
        verbose_name = _('Donation Form')
        verbose_name_plural = _('Donation Forms')

    def __str__(self):
        return str(self.title)

    def isDefaultMonthly(self):
        return self.default_frequency == 'monthly'

    def isAmountFixed(self):
        return self.amount_type == 'fixed'

    def isAmountStepped(self):
        return self.amount_type == 'stepped'

    def isAmountCustom(self):
        return self.amount_type == 'custom'

    def isAmountSteppedCustom(self):
        return self.amount_type == 'stepped_custom'


class DonationMeta(models.Model):
    '''
    DonationMeta is used for storing meta data entered by the donor in the frontend, which is defined by the website admin at first.
    '''
    donation = ParentalKey(
        'Donation',
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
        verbose_name = _('Donation Meta')
        verbose_name_plural = _('Donation Metas')

    def __str__(self):
        return self.field_key


class TempDonationMeta(models.Model):
    '''
    TempDonationMeta is used for storing meta data entered by the donor in the frontend, which is defined by the website admin at first.
    '''
    donation = ParentalKey(
        'TempDonation',
        related_name='temp_metas',
        on_delete=models.CASCADE,
    )
    field_key = models.CharField(max_length=255)
    field_value = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = _('Temp Donation Meta')
        verbose_name_plural = _('Temp Donation Metas')

    def __str__(self):
        return self.field_key


class DonationPaymentMeta(models.Model):
    '''
    DonationPaymentMeta is used for storing meta data mainly used by the code or system itself.
    '''
    donation = ParentalKey(
        'Donation',
        related_name='payment_metas',
        on_delete=models.CASCADE,
    )
    field_key = models.CharField(max_length=255)
    field_value = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = _('Donation Payment Meta')
        verbose_name_plural = _('Donation Payment Metas')

    def __str__(self):
        return self.field_key


class SubscriptionPaymentMeta(models.Model):
    '''
    SubscriptionPaymentMeta is used for storing meta data mainly used by the code or system itself.
    '''
    subscription = ParentalKey(
        'SubscriptionInstance',
        related_name='payment_metas',
        on_delete=models.CASCADE,
    )
    field_key = models.CharField(max_length=255)
    field_value = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = _('Subscription Payment Meta')
        verbose_name_plural = _('Subscription Payment Metas')

    def __str__(self):
        return self.field_key


class Subscription(models.Model):
    """ This model is a parent wrapper for chronically-related SubscriptionInstances
        specifically for the case when users updating payment method on Newstream
        while the system delete the old subscription and create a new subscription
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'newstream_user.User',
        on_delete=models.SET_NULL,
        null=True
    )
    # reason for subscription_created_at field is because when we list Subscriptions on user's recurring donations page,
    # we need to order them by date of subscription, created_at isn't accurate as it might be created by the data migration
    # which is much later than the original subscription date by the user
    # that's why this field should be very close/same as the created_at of its first instance
    subscription_created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'newstream_user.User',
        related_name='subscription_created_by',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    deleted = models.BooleanField(default=False)

    @property
    def first_instance(self):
        # return oldest instance
        # mainly for displaying the subscribe date
        return self.subscription_instances.all().order_by("subscribe_date", "created_at").first()

    @property
    def latest_instance(self):
        # return the latest instance
        # mainly for displaying the current subscription info
        # e.g. amount, currency, profile_id, status
        return self.subscription_instances.all().order_by("subscribe_date", "created_at").last()


class SubscriptionInstance(ClusterableModel):
    """ This model corresponds to the actual Subscription object in the gateways
    """
    RECURRING_STATUS_CHOICES = [
        (STATUS_ACTIVE, _(STATUS_ACTIVE.capitalize())),
        (STATUS_PROCESSING, _(STATUS_PROCESSING.capitalize())),
        (STATUS_PAUSED, _(STATUS_PAUSED.capitalize())),
        (STATUS_CANCELLED, _(STATUS_CANCELLED.capitalize())),
        (STATUS_INACTIVE, _(STATUS_INACTIVE.capitalize())),
        (STATUS_PAYMENT_FAILED, _(STATUS_PAYMENT_FAILED.capitalize())),
    ]
    user = models.ForeignKey(
        'newstream_user.User',
        on_delete=models.SET_NULL,
        null=True
    )
    gateway = models.ForeignKey(
        'site_settings.PaymentGateway',
        on_delete=models.SET_NULL,
        null=True
    )
    parent = models.ForeignKey(
        'Subscription',
        related_name='subscription_instances',
        on_delete=models.SET_NULL,
        null=True
    )
    is_test = models.BooleanField(default=False)
    profile_id = models.CharField(max_length=191, unique=True)
    recurring_amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=20)
    recurring_status = models.CharField(
        max_length=255, choices=RECURRING_STATUS_CHOICES, default=STATUS_INACTIVE, blank=True, null=True)
    subscribe_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'newstream_user.User',
        related_name='subscription_instance_created_by',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    linked_user_deleted = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    panels = [
        AutocompletePanel('user', heading=_(
            'User')),
        FieldPanel('gateway', heading=_('Payment Gateway')),
        FieldPanel('is_test', heading=_('Is Test Subscription?')),
        FieldPanel('profile_id', heading=_('Profile ID')),
        FieldPanel('recurring_amount', heading=_('Recurring Amount')),
        FieldPanel('currency', heading=_('Currency')),
        FieldPanel('recurring_status', heading=_('Recurring Status')),
        FieldPanel('subscribe_date', heading=_('Subscribe Date')),
        FieldPanel('linked_user_deleted', heading=_('Donor User Deleted?')),
    ]

    def __str__(self):
        return '#'+str(self.id)+' - '+self.profile_id

    def isRecurringCancelled(self):
        return True if self.recurring_status == STATUS_CANCELLED else False

    def isRecurringProcessing(self):
        return True if self.recurring_status == STATUS_PROCESSING else False

    class Meta:
        ordering = ['-subscribe_date', '-created_at']
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')


class Donation(ClusterableModel):
    PAYMENT_STATUS_CHOICES = [
        (STATUS_COMPLETE, _(STATUS_COMPLETE.capitalize())),
        (STATUS_PROCESSING, _(STATUS_PROCESSING.capitalize())),
        (STATUS_REFUNDED, _(STATUS_REFUNDED.capitalize())),
        (STATUS_REVOKED, _(STATUS_REVOKED.capitalize())),
        (STATUS_FAILED, _(STATUS_FAILED.capitalize())),
        (STATUS_CANCELLED, _(STATUS_CANCELLED.capitalize())),
    ]
    user = models.ForeignKey(
        'newstream_user.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    form = models.ForeignKey(
        'DonationForm',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    gateway = models.ForeignKey(
        'site_settings.PaymentGateway',
        on_delete=models.SET_NULL,
        null=True
    )
    subscription = models.ForeignKey(
        'SubscriptionInstance',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    is_test = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=191, unique=True)
    donation_amount = models.DecimalField(max_digits=20, decimal_places=2)
    is_recurring = models.BooleanField(default=False)
    currency = models.CharField(max_length=20)
    payment_status = models.CharField(
        max_length=255, choices=PAYMENT_STATUS_CHOICES)
    donation_date = models.DateTimeField()
    guest_email = models.EmailField(blank=True)
    guest_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'newstream_user.User',
        related_name='donation_created_by',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    linked_user_deleted = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    panels = [
        AutocompletePanel('user', heading=_(
            'User')),
        FieldPanel('form', heading=_('Donation Form')),
        FieldPanel('gateway', heading=_('Payment Gateway')),
        FieldPanel('subscription', heading=_('Subscription')),
        FieldPanel('is_test', heading=_('Is Test Donation?')),
        FieldPanel('transaction_id', heading=_('Transaction ID')),
        FieldPanel('donation_amount', heading=_('Donation amount')),
        FieldPanel('guest_email', heading=_('Guest Email - for non-registered donors')),
        FieldPanel('guest_name', heading=_('Guest Name - for non-registered donors')),
        FieldPanel('is_recurring', heading=_('Is Recurring Donation?')),
        FieldPanel('currency', heading=_('Currency')),
        FieldPanel('payment_status', heading=_('Payment status')),
        FieldPanel('donation_date', heading=_('Donation Date')),
        InlinePanel('metas', label=_('Donation Meta'), heading=_('Donation Meta Data'),
                    help_text=_('Meta data about this donation is recorded here')),
        FieldPanel('linked_user_deleted',
                      heading=_("Donor User Deleted?")),
    ]

    class Meta:
        ordering = ['-donation_date', '-created_at']
        verbose_name = _('Donation')
        verbose_name_plural = _('Donations')

    def __str__(self):
        return '#'+str(self.id)+' - '+self.transaction_id

    def isRecurring(self):
        return 'Yes' if self.is_recurring else 'No'

    def display_donor(self):
        return self.donor_name or self.donor_email

    def display_donor_name(self):
        return self.donor_name if self.donor_name else '--'

    def display_donor_email(self):
        return self.donor_email if self.donor_email else '--'

    @property
    def donor_name(self):
        if self.user:
            return self.user.fullname
        else:
            return self.guest_name or ''

    @property
    def donor_email(self):
        if self.user:
            return self.user.email
        else:
            return self.guest_email or ''

    @property
    def is_user_first_donation(self):
        resultSet = DonationPaymentMeta.objects.filter(
            donation_id=self.id, field_key='is_user_first_donation')
        if len(resultSet) == 1:
            return resultSet[0].field_value
        return False

    @is_user_first_donation.setter
    def is_user_first_donation(self, val):
        pass

    @property
    def donation_frequency(self):
        return 'Monthly' if self.is_recurring else 'One-time'

    @donation_frequency.setter
    def donation_frequency(self, val):
        pass

    @property
    def donation_type_stripe(self):
        return 'recurring' if self.is_recurring else 'one_time'

    @donation_type_stripe.setter
    def donation_type_stripe(self, val):
        pass

    def isOnGoing(self):
        return 'Yes' if self.is_recurring and self.subscription.recurring_status == STATUS_ACTIVE else 'No'


class TempDonation(ClusterableModel):
    STATUS_CHOICES = [
        (STATUS_PENDING, _(STATUS_PENDING.capitalize())),
        (STATUS_PROCESSED, _(STATUS_PROCESSED.capitalize())),
    ]
    form = models.ForeignKey(
        'DonationForm',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    gateway = models.ForeignKey(
        'site_settings.PaymentGateway',
        on_delete=models.SET_NULL,
        null=True
    )
    is_test = models.BooleanField(default=False)
    is_amount_custom = models.BooleanField(default=False)
    donation_amount = models.DecimalField(max_digits=20, decimal_places=2)
    is_recurring = models.BooleanField(default=False)
    currency = models.CharField(max_length=20)
    guest_email = models.EmailField(blank=True)
    guest_name = models.CharField(blank=True, max_length=255)
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES)

    class Meta:
        ordering = ['-id']
        verbose_name = _('Temp Donation')
        verbose_name_plural = _('Temp Donations')

    def __str__(self):
        return '#'+str(self.id)

    def isRecurring(self):
        return 'Yes' if self.is_recurring else 'No'

    @property
    def donation_frequency(self):
        return 'Monthly' if self.is_recurring else 'One-time'

    @donation_frequency.setter
    def donation_frequency(self, val):
        pass


@receiver(pre_delete, sender=User)
def update_deleted_users_donations(sender, instance, using, **kwargs):
    donations = Donation.objects.filter(user=instance).all()
    for donation in donations:
        donation.linked_user_deleted = True
        donation.save()
    subscriptions = SubscriptionInstance.objects.filter(user=instance).all()
    for subscription in subscriptions:
        subscription.linked_user_deleted = True
        subscription.save()
