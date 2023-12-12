from django.db import models
from django.conf import settings
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel, InlinePanel
from i18nfield.fields import I18nCharField, I18nTextField
from wagtail.contrib.forms.models import AbstractFormField

from wagtailautocomplete.edit_handlers import AutocompletePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel

from newstream.fields import I18nRichTextField


class CustomCheckboxMultiple(CheckboxSelectMultiple):
    template_name = 'django/forms/widgets/custom_checkbox_select.html'


class EmailTemplate(models.Model):
    title = I18nCharField(max_length=255)
    subject = I18nCharField(max_length=255)
    plain_text = I18nTextField()
    html_body = I18nRichTextField(blank=True)

    panels = [
        FieldPanel('title', heading=_('Title')),
        FieldPanel('subject', heading=_('Subject')),
        FieldPanel('plain_text', heading=_('Plain Text Body')),
        FieldPanel('html_body', heading=_('HTML Body')),
    ]

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _('Email Template')
        verbose_name_plural = _('Email Templates')


class TargetGroup(ClusterableModel):
    title = I18nCharField(max_length=255)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='target_groups', limit_choices_to={'opt_in_mailing_list': True})

    panels = [
        FieldPanel('title', heading=_('Title')),
        # neither help_text or heading works for users field below, switched to verbose_name above
        FieldPanel('users', heading=_('Users (Only opted-in and verified users are listed here)'),
                   widget=CustomCheckboxMultiple),
    ]

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _('Target Group')
        verbose_name_plural = _('Target Groups')


class Campaign(ClusterableModel):
    title = I18nCharField(max_length=255)
    from_address = models.EmailField()
    recipients = models.ManyToManyField(TargetGroup)
    template = models.ForeignKey(
        EmailTemplate, on_delete=models.SET_NULL, null=True)
    sent = models.BooleanField(default=False, editable=False)
    sent_at = models.DateTimeField(blank=True, null=True)

    panels = [
        FieldPanel('title', heading=_('Title')),
        FieldPanel('from_address', heading=_('From Address')),
        FieldPanel('template', heading=_('Template')),
        AutocompletePanel('recipients', heading=_('Recipients')),
    ]

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-id']
        verbose_name = _('Campaign')
        verbose_name_plural = _('Campaigns')
