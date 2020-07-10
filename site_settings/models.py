import html
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from donations.includes.currency_dictionary import currency_dict


class CustomTabbedInterface(TabbedInterface):
    template = "wagtailadmin/edit_handlers/custom_tabbed_interface.html"


class AdminEmails(models.Model):
    title = models.CharField(max_length=255)
    email = models.EmailField()
    setting_parent = ParentalKey(
        'GlobalSettings', on_delete=models.CASCADE, related_name='admin_emails')

    panels = [
        FieldPanel('title'),
        FieldPanel('email'),
    ]

    def __str__(self):
        return self.title+" "+'({})'.format(self.email)


@register_setting
class AppearanceSettings(BaseSetting):
    """ Customize site outlook here """
    brand_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    site_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('brand_logo'),
        ImageChooserPanel('site_icon'),
    ]


@register_setting
class GlobalSettings(BaseSetting, ClusterableModel):
    """Top level settings for this omp app"""
    # todo: make supported currencies for each payment gateway
    # todo: check against being-in-use gateways' supported currencies with this setting
    test_mode = models.BooleanField(default=True)
    currency = models.CharField(default='USD', max_length=10, choices=[(key, html.unescape(
        val['admin_label'])) for key, val in currency_dict.items()])

    panels = [
        FieldPanel('test_mode'),
        FieldPanel('currency'),
        InlinePanel('admin_emails', label="Admin Email", heading="List of Admins' Emails",
                    help_text='Email notifications such as new donations will be sent to this list.'),
    ]


@register_setting
class Settings2C2P(BaseSetting):
    """Settings for the 2c2p api."""

    merchant_id = models.CharField(
        max_length=255, blank=True, null=True, help_text="Merchant ID")
    secret_key = models.CharField(
        max_length=255, blank=True, null=True, help_text="Secret Key")
    log_filename = models.CharField(
        max_length=255, blank=True, null=True, help_text="Log Filename")

    panels = [
        MultiFieldPanel([
            FieldPanel("merchant_id"),
            FieldPanel("secret_key"),
            FieldPanel("log_filename"),
        ], heading="2C2P API Test Settings")
    ]

    class Meta:
        verbose_name = '2C2P Settings'


@register_setting
class TestGeneralSettings(BaseSetting):

    field_1 = models.CharField(
        max_length=255, blank=True, null=True)
    field_2 = models.CharField(
        max_length=255, blank=True, null=True)
    field_3 = models.CharField(
        max_length=255, blank=True, null=True)
    field_4 = models.CharField(
        max_length=255, blank=True, null=True)
    field_5 = models.CharField(
        max_length=255, blank=True, null=True)
    field_6 = models.CharField(
        max_length=255, blank=True, null=True)

    general_tab_panels = [
        FieldPanel('field_1'),
        FieldPanel('field_2'),
    ]
    language_tab_panels = [
        FieldPanel('field_3'),
        FieldPanel('field_4'),
    ]
    specific_tab_panels = [
        FieldPanel('field_5'),
        FieldPanel('field_6'),
    ]

    edit_handler = CustomTabbedInterface([
        TabbedInterface([
            ObjectList(general_tab_panels, heading='General'),
            ObjectList(language_tab_panels, heading='Languages'),
        ], heading="First Tab"),
        TabbedInterface([
            ObjectList(specific_tab_panels, heading='Specifics'),
        ], heading="Second Tab"),
    ])
