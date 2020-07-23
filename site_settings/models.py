import html
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList, RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.contrib.forms.models import AbstractFormField
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from donations.includes.currency_dictionary import currency_dict


class TopTabbedInterface(TabbedInterface):
    template = "wagtailadmin/edit_handlers/top_tabbed_interface.html"


class SubTabbedInterface(TabbedInterface):
    template = "wagtailadmin/edit_handlers/sub_tabbed_interface.html"


class SubObjectList(ObjectList):
    def __init__(self, *args, **kwargs):
        self.slug = kwargs.pop('slug', None)
        super().__init__(*args, **kwargs)

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs['slug'] = self.slug
        return kwargs


class AdminEmails(models.Model):
    title = models.CharField(max_length=255)
    email = models.EmailField()
    setting_parent = ParentalKey(
        'SiteSettings', on_delete=models.CASCADE, related_name='admin_emails')

    panels = [
        FieldPanel('title'),
        FieldPanel('email'),
    ]

    def __str__(self):
        return self.title+" "+'({})'.format(self.email)


class UserMetaField(AbstractFormField):
    parent = ParentalKey('SiteSettings', on_delete=models.CASCADE,
                         related_name='user_meta_fields')


@register_setting
class SiteSettings(BaseSetting, ClusterableModel):
    default_from_email = models.EmailField()
    general_general_panels = [
        FieldPanel('default_from_email'),
        InlinePanel('admin_emails', label="Admin Email", heading="List of Admins' Emails",
                    help_text='Email notifications such as new donations will be sent to this list.')
    ]
    social_skip_signup = models.BooleanField(default=False)
    signup_footer_text = RichTextField(blank=True)
    general_user_panels = [
        FieldPanel('social_skip_signup',
                   heading='Allow Firsttime Social Logins bypass Signup Form?'),
        FieldPanel('signup_footer_text',
                   heading='Footer Text(Under Signup Form)'),
        InlinePanel('user_meta_fields', label='User Meta Fields',
                    help_text='Add extra fields for the user signup form for additional data you want to collect from them.'),
    ]

    # todo: make supported currencies for each payment gateway
    # todo: check against being-in-use gateways' supported currencies with this setting
    sandbox_mode = models.BooleanField(default=True)
    currency = models.CharField(default='USD', max_length=10, choices=[(key, html.unescape(
        val['admin_label'])) for key, val in currency_dict.items()])

    gateways_general_panels = [
        FieldPanel('sandbox_mode'),
        FieldPanel('currency')
    ]

    _2c2p_merchant_id = models.CharField(
        max_length=255, blank=True, null=True, help_text="Merchant ID")
    _2c2p_secret_key = models.CharField(
        max_length=255, blank=True, null=True, help_text="Secret Key")
    _2c2p_log_filename = models.CharField(
        max_length=255, blank=True, null=True, help_text="Log Filename")

    gateways_2c2p_panels = [
        MultiFieldPanel([
            FieldPanel("_2c2p_merchant_id"),
            FieldPanel("_2c2p_secret_key"),
            FieldPanel("_2c2p_log_filename"),
        ], heading="2C2P API Sandbox Settings")
    ]

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

    appearance_general_panels = [
        ImageChooserPanel('brand_logo'),
        ImageChooserPanel('site_icon'),
    ]

    edit_handler = TopTabbedInterface([
        SubTabbedInterface([
            SubObjectList(general_general_panels, slug='general-general',
                          heading='General'),
            SubObjectList(general_user_panels, slug='general-user',
                          heading='User Settings'),
        ], heading="General"),
        SubTabbedInterface([
            SubObjectList(gateways_general_panels,
                          heading='General', slug='gateways-general'),
            SubObjectList(gateways_2c2p_panels,
                          heading='2C2P(Credit Card)', slug='gateways-2c2p'),
        ], heading="Gateways"),
        SubTabbedInterface([
            SubObjectList(appearance_general_panels,
                          heading='General', slug='appearance-general'),
        ], heading="Appearance"),
    ])
