from django.db import models
from django.contrib.auth.models import User
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtailautocomplete.edit_handlers import AutocompletePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.forms.models import AbstractFormField

GATEWAY_2C2P = '2C2P'
GATEWAY_PAYPAL = 'PayPal'
GATEWAY_STRIPE = 'Stripe'

STATUS_ONGOING = 'on-going'
STATUS_COMPLETE = 'complete'
STATUS_PENDING = 'pending'
STATUS_REFUNDED = 'refunded'
STATUS_REVOKED = 'revoked'
STATUS_FAILED = 'failed'
STATUS_CANCELLED = 'cancelled'
STATUS_NONRECURRING = 'non-recurring'


class PaymentGateway(models.Model):
    title = models.CharField(max_length=255, unique=True)
    list_order = models.IntegerField(default=0)

    panels = [
        FieldPanel('title'),
        FieldPanel('list_order'),
    ]

    class Meta:
        ordering = ['list_order']

    def __str__(self):
        return self.title

    def is_2c2p(self):
        return self.title == GATEWAY_2C2P

    def is_paypal(self):
        return self.title == GATEWAY_PAYPAL

    def is_stripe(self):
        return self.title == GATEWAY_STRIPE


class MoreFormField(AbstractFormField):
    form = ParentalKey('DonationForm', on_delete=models.CASCADE,
                       related_name='more_form_fields')


class AmountStep(models.Model):
    form = ParentalKey('DonationForm', on_delete=models.CASCADE,
                       related_name='amount_steps')
    step = models.FloatField(default=0)

    panels = [
        FieldPanel('step'),
    ]

    class Meta:
        unique_together = ['form', 'step']


class DonationForm(ClusterableModel):
    AMOUNT_TYPE_CHOICES = [
        ('fixed', 'Fixed Amount'),
        ('stepped', 'Fixed Steps'),
        ('custom', 'Custom Amount'),
    ]
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)
    amount_type = models.CharField(
        max_length=20, choices=AMOUNT_TYPE_CHOICES, verbose_name='Donation Amount Type')
    fixed_amount = models.FloatField(blank=True, null=True, verbose_name='Define Fixed Donation Amount',
                                     help_text='Define fixed donation amount if you chose "Fixed Amount" for your Amount Type')
    allowed_gateways = models.ManyToManyField('PaymentGateway')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('is_recurring'),
        FieldPanel('amount_type'),
        FieldPanel(
            'fixed_amount', help_text='Define your fixed donation amount if you chose "Fixed Amount" for your Amount Type.'),
        InlinePanel('amount_steps', label='Fixed Amount Steps', heading='Define Fixed Donation Amount Steps',
                    help_text='Define fixed donation amount steps if you chose "Fixed Steps" for your Amount Type.'),
        AutocompletePanel('allowed_gateways'),
        InlinePanel('more_form_fields', label='More Form Fields'),
    ]

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def isAmountFixed(self):
        return self.amount_type == 'fixed'

    def isAmountStepped(self):
        return self.amount_type == 'stepped'

    def isAmountCustom(self):
        return self.amount_type == 'custom'


class Donor(models.Model):
    linked_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    opt_in_mailing_list = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    panels = [
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('email'),
        FieldPanel('opt_in_mailing_list'),
    ]

    class Meta:
        ordering = ['-created_at']
        unique_together = ['first_name', 'last_name', 'email']

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])

    @property
    def fullname(self):
        return ' '.join([self.first_name, self.last_name])

    @fullname.setter
    def fullname(self, val):
        pass

    def optInMailing(self):
        return 'Yes' if self.opt_in_mailing_list else 'No'


class Donation(ClusterableModel):
    PAYMENT_STATUS_CHOICES = [
        (STATUS_COMPLETE, STATUS_COMPLETE.capitalize()),
        (STATUS_PENDING, STATUS_PENDING.capitalize()),
        (STATUS_REFUNDED, STATUS_REFUNDED.capitalize()),
        (STATUS_REVOKED, STATUS_REVOKED.capitalize()),
        (STATUS_FAILED, STATUS_FAILED.capitalize()),
        (STATUS_CANCELLED, STATUS_CANCELLED.capitalize()),
    ]
    RECURRING_STATUS_CHOICES = [
        (STATUS_ONGOING, STATUS_ONGOING.capitalize()),
        (STATUS_CANCELLED, STATUS_CANCELLED.capitalize()),
        (STATUS_NONRECURRING, STATUS_NONRECURRING.capitalize()),
    ]
    donor = models.ForeignKey(
        'Donor',
        on_delete=models.CASCADE,
    )
    form = models.ForeignKey(
        'DonationForm',
        on_delete=models.CASCADE,
    )
    gateway = models.ForeignKey(
        'PaymentGateway',
        on_delete=models.CASCADE,
    )
    parent_donation = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    order_number = models.CharField(max_length=255, unique=True)
    donation_amount = models.FloatField()
    is_recurring = models.BooleanField(default=False)
    currency = models.CharField(max_length=20)
    is_create_account = models.BooleanField(default=False)
    payment_status = models.CharField(
        max_length=255, choices=PAYMENT_STATUS_CHOICES)
    recurring_status = models.CharField(
        max_length=255, choices=RECURRING_STATUS_CHOICES, default=STATUS_NONRECURRING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    panels = [
        FieldPanel('order_number'),
        FieldPanel('donation_amount'),
        FieldPanel('is_recurring'),
        FieldPanel('currency'),
        FieldPanel('is_create_account'),
        FieldPanel('payment_status'),
        FieldPanel('recurring_status'),
        InlinePanel('metas', label='Donation Meta', heading='Donation Meta Data',
                    help_text='Meta data about this donation is recorded here'),
    ]

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '#'+str(self.id)+' - '+str(self.donor)

    def isRecurring(self):
        return 'Yes' if self.is_recurring else 'No'

    def isCreateAccount(self):
        return 'Yes' if self.is_create_account else 'No'

    def isOnGoing(self):
        return 'Yes' if self.recurring_status == STATUS_ONGOING else 'No'


class DonationMeta(models.Model):
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

    def __str__(self):
        return self.field_key
