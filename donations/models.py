from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtailautocomplete.edit_handlers import AutocompletePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.forms.models import AbstractFormField


class PaymentGateway(models.Model):
    title = models.CharField(max_length=255)
    list_order = models.IntegerField(default=0)

    panels = [
        FieldPanel('title'),
        FieldPanel('list_order'),
    ]

    class Meta:
        ordering = ['list_order']

    def __str__(self):
        return self.title


class MoreFormField(AbstractFormField):
    form = ParentalKey('DonationForm', on_delete=models.CASCADE, related_name='more_form_fields')


class AmountStep(models.Model):
    form = ParentalKey('DonationForm', on_delete=models.CASCADE, related_name='amount_steps')
    step = models.FloatField(default=0)

    panels = [
        FieldPanel('step'),
    ]


class DonationForm(ClusterableModel):
    AMOUNT_TYPE_CHOICES = [
        ('fixed', 'Fixed Amount'),
        ('stepped', 'Fixed Steps'),
        ('custom', 'Custom Amount'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)
    amount_type = models.CharField(max_length=20, choices=AMOUNT_TYPE_CHOICES, verbose_name='Donation Amount Type')
    fixed_amount = models.FloatField(blank=True, null=True, verbose_name='Define Fixed Donation Amount', help_text='Define fixed donation amount if you chose "Fixed Amount" for your Amount Type')
    allowed_gateways = models.ManyToManyField('PaymentGateway')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('is_recurring'),
        FieldPanel('amount_type'),
        FieldPanel('fixed_amount', help_text='Define your fixed donation amount if you chose "Fixed Amount" for your Amount Type.'),
        InlinePanel('amount_steps', label='Fixed Amount Steps', heading='Define Fixed Donation Amount Steps', help_text='Define fixed donation amount steps if you chose "Fixed Steps" for your Amount Type.'),
        AutocompletePanel('allowed_gateways'),
        InlinePanel('more_form_fields', label='More Form Fields'),
    ]

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class CustomFormFields(models.Model):
    field_key = models.CharField(max_length=255)
    field_label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=20)
    field_options = models.TextField(blank=True)
    list_order = models.IntegerField(default=0)

    panels = [
        FieldPanel('field_label')
    ]

    class Meta:
        ordering = ['list_order']

    def __str__(self):
        return self.field_label


class Donor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    opt_in_mailing_list = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    panels = [
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('email'),
        FieldPanel('contact_number'),
        FieldPanel('opt_in_mailing_list'),
    ]

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return ' '.join([self.title, self.first_name, self.last_name])


class Donation(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('complete', 'Complete'),
        ('pending', 'Pending'),
        ('refunded', 'Refunded'),
        ('revoked', 'Revoked'),
        ('failed', 'Failed'),
        ('cacnelled', 'Cancelled'),
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
    order_number = models.CharField(max_length=255)
    donation_amount = models.FloatField()
    is_recurring = models.BooleanField(default=False)
    currency = models.CharField(max_length=20)
    is_create_account = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '#'+self.id+' - '+self.donor


class DonationMeta(models.Model):
    donation = models.ForeignKey(
        'Donation',
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
