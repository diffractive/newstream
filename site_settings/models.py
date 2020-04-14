import html
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
#from wagtail.admin.edit_handlers import TabbedInterface, ObjectList

from donations.includes.currency_dictionary import currency_dict


@register_setting
class GlobalSettings(BaseSetting):
    """Top level settings for this omp app"""
    # todo: make supported currencies for each payment gateway
    # todo: check against being-in-use gateways' supported currencies with this setting
    test_mode = models.BooleanField(default=True)
    currency = models.CharField(default='USD', max_length=10, choices=[(key, html.unescape(
        val['admin_label'])) for key, val in currency_dict.items()])

    panels = [
        FieldPanel('test_mode'),
        FieldPanel('currency'),
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
