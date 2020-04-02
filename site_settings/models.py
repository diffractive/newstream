from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
#from wagtail.admin.edit_handlers import TabbedInterface, ObjectList

@register_setting
class Settings2C2P(BaseSetting):
    """Settings for the 2c2p api."""

    merchant_id = models.CharField(max_length=255, blank=True, null=True, help_text="Merchant ID")
    secret_key = models.CharField(max_length=255, blank=True, null=True, help_text="Secret Key")
    currency_code = models.CharField(max_length=255, blank=True, null=True, help_text="Currency Code")
    log_filename = models.CharField(max_length=255, blank=True, null=True, help_text="Log Filename")

    panels = [
        MultiFieldPanel([
            FieldPanel("merchant_id"),
            FieldPanel("secret_key"),
            FieldPanel("currency_code"),
            FieldPanel("log_filename"),
        ], heading="2C2P API Test Settings")
    ]

    class Meta:
        verbose_name = '2C2P Settings'

