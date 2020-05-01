from django import forms
from django.db import models
from django.conf import settings
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, RichTextField
from wagtailautocomplete.edit_handlers import AutocompletePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.contrib.forms.models import AbstractFormField


class EmailTemplate(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    plain_text = models.TextField()
    html_body = RichTextField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('subject'),
        FieldPanel('plain_text'),
        FieldPanel('html_body'),
    ]

    def __str__(self):
        return self.title


class TargetGroup(ClusterableModel):
    title = models.CharField(max_length=255)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='target_groups', verbose_name='Users (Only opted-in and verified users are listed here)', limit_choices_to={'is_email_verified': True, 'opt_in_mailing_list': True})

    panels = [
        FieldPanel('title'),
        # neither help_text or heading works for users field below, switched to verbose_name above
        FieldPanel('users', widget=forms.CheckboxSelectMultiple),
    ]

    def __str__(self):
        return self.title


class Campaign(ClusterableModel):
    title = models.CharField(max_length=255)
    from_address = models.EmailField()
    recipients = models.ManyToManyField(TargetGroup)
    template = models.ForeignKey(
        EmailTemplate, on_delete=models.SET_NULL, null=True)
    sent = models.BooleanField(default=False, editable=False)
    sent_at = models.DateTimeField(blank=True, null=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('from_address'),
        FieldPanel('template'),
        AutocompletePanel('recipients'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
