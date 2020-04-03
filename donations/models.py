from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtailautocomplete.edit_handlers import AutocompletePanel


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

class DonationForm(models.Model):
    AMOUNT_TYPE_CHOICES = [
        ('fixed', 'Fixed Amount'),
        ('stepped', 'Fixed Steps'),
        ('custom', 'Custom Amount'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)
    amount_type = models.CharField(max_length=20, choices=AMOUNT_TYPE_CHOICES)
    fixed_amount = models.FloatField(blank=True, null=True)
    amount_steps = models.TextField(blank=True)
    allowed_gateways = models.ManyToManyField('PaymentGateway')

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('is_recurring'),
        FieldPanel('amount_type'),
        AutocompletePanel('allowed_gateways'),
    ]

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
