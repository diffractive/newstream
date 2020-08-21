import html
from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList, RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.contrib.forms.models import AbstractFormField
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from donations.includes.currency_dictionary import currency_dict


GATEWAY_2C2P = '2C2P'
GATEWAY_PAYPAL = 'PayPal'
GATEWAY_STRIPE = 'Stripe'


class TopTabbedInterface(TabbedInterface):
    template = "wagtailadmin/edit_handlers/top_tabbed_interface.html"


class SubTabbedInterface(TabbedInterface):
    template = "wagtailadmin/edit_handlers/sub_tabbed_interface.html"


# had to use classname attribute for the section id in sub_tabbed_interface.html
# since source code in wagtail-modeltranslation only transfers heading and classname as extra attributes to the localized panels
class SubObjectList(ObjectList):
    pass


class PaymentGateway(models.Model):
    title = models.CharField(max_length=255, unique=True)
    frontend_label_attr_name = models.CharField(max_length=255)
    list_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['list_order']
        verbose_name = _('Payment Gateway')
        verbose_name_plural = _('Payment Gateways')

    def __str__(self):
        return self.title

    def is_2c2p(self):
        return self.title == GATEWAY_2C2P

    def is_paypal(self):
        return self.title == GATEWAY_PAYPAL

    def is_stripe(self):
        return self.title == GATEWAY_STRIPE


class AdminEmails(models.Model):
    title = models.CharField(max_length=255)
    email = models.EmailField()
    setting_parent = ParentalKey(
        'SiteSettings', on_delete=models.CASCADE, related_name='admin_emails')

    panels = [
        FieldPanel('title', heading=_('Title')),
        FieldPanel('email', heading=_('Email')),
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
        FieldPanel('default_from_email', heading=_('Default From Email')),
        InlinePanel('admin_emails', label=_("Admin Email"), heading=_("List of Admins' Emails"),
                    help_text=_('Email notifications such as new donations will be sent to this list.'))
    ]
    signup_footer_text = RichTextField(blank=True)
    general_signup_panels = [
        FieldPanel('signup_footer_text',
                   heading=_('Footer Text(Under Signup Form)')),
        InlinePanel('user_meta_fields', label=_('User Meta Fields'),
                    help_text=_('Add extra fields for the user signup form for additional data you want to collect from them.')),
    ]

    # todo: make supported currencies for each payment gateway
    # todo: check against being-in-use gateways' supported currencies with this setting
    sandbox_mode = models.BooleanField(default=True)
    currency = models.CharField(default='USD', max_length=10, choices=[(key, html.unescape(
        val['admin_label'])) for key, val in currency_dict.items()])

    gateways_general_panels = [
        FieldPanel('sandbox_mode', heading=_('Sandbox Mode')),
        FieldPanel('currency', heading=_('Currency'))
    ]

    _2c2p_frontend_label = models.CharField(
        max_length=255, default=_("2C2P(Credit Card)"), help_text=_("The Gateway name to be shown on public-facing website."))
    _2c2p_merchant_id = models.CharField(
        max_length=255, blank=True, null=True, help_text=_("Merchant ID"))
    _2c2p_secret_key = models.CharField(
        max_length=255, blank=True, null=True, help_text=_("Secret Key"))
    _2c2p_testing_merchant_id = models.CharField(
        max_length=255, blank=True, null=True, help_text=_("Testing Merchant ID"))
    _2c2p_testing_secret_key = models.CharField(
        max_length=255, blank=True, null=True, help_text=_("Testing Secret Key"))

    gateways_2c2p_panels = [
        FieldPanel("_2c2p_frontend_label", heading=_(
            "2C2P Gateway public-facing label")),
        MultiFieldPanel([
            FieldPanel("_2c2p_testing_merchant_id",
                       heading=_("2C2P Testing Merchant ID")),
            FieldPanel("_2c2p_testing_secret_key",
                       heading=_("2C2P Testing Secret Key")),
        ], heading=_("2C2P API Sandbox Settings")),
        MultiFieldPanel([
            FieldPanel("_2c2p_merchant_id", heading=_("2C2P Merchant ID")),
            FieldPanel("_2c2p_secret_key", heading=_("2C2P Secret Key")),
        ], heading=_("2C2P API Live Settings"))
    ]

    paypal_frontend_label = models.CharField(
        max_length=255, default=_("PayPal"), help_text=_("The Gateway name to be shown on public-facing website."))

    gateways_paypal_panels = [
        FieldPanel("paypal_frontend_label", heading=_(
            "PayPal Gateway public-facing label")),
    ]

    stripe_frontend_label = models.CharField(
        max_length=255, default=_("Stripe"), help_text=_("The Gateway name to be shown on public-facing website."))

    gateways_stripe_panels = [
        FieldPanel("stripe_frontend_label", heading=_(
            "Stripe Gateway public-facing label")),
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
        ImageChooserPanel('brand_logo', heading=('Brand Logo')),
        ImageChooserPanel('site_icon', heading=('Site Icon')),
    ]

    social_login_enabled = models.BooleanField(default=True)
    social_skip_signup = models.BooleanField(default=False)
    social_general_panels = [
        FieldPanel('social_login_enabled',
                   heading=_('Enable Social Login for this site ?')),
        FieldPanel('social_skip_signup',
                   heading=_('Allow Firsttime Social Logins bypass Signup Form ?')),
    ]
    google_login_enabled = models.BooleanField(default=True)
    social_google_panels = [
        FieldPanel('google_login_enabled',
                   heading=_('Enable Google Login ? (Only if Social Login is enabled)')),
    ]
    facebook_login_enabled = models.BooleanField(default=True)
    social_facebook_panels = [
        FieldPanel('facebook_login_enabled',
                   heading=_('Enable Facebook Login ? (Only if Social Login is enabled)')),
    ]
    twitter_login_enabled = models.BooleanField(default=True)
    social_twitter_panels = [
        FieldPanel('twitter_login_enabled',
                   heading=_('Enable Twitter Login ? (Only if Social Login is enabled)')),
    ]

    edit_handler = TopTabbedInterface([
        SubTabbedInterface([
            SubObjectList(general_general_panels, classname='general-general',
                          heading=_('General')),
            SubObjectList(general_signup_panels, classname='general-signup',
                          heading=_('User Signup')),
        ], heading=_("General")),
        SubTabbedInterface([
            SubObjectList(social_general_panels, classname='social-general',
                          heading=_('General')),
            SubObjectList(social_google_panels, classname='social-google',
                          heading=_('Google')),
            SubObjectList(social_facebook_panels, classname='social-facebook',
                          heading=_('Facebook')),
            SubObjectList(social_twitter_panels, classname='social-twitter',
                          heading=_('Twitter')),
        ], heading=_("Social Logins")),
        SubTabbedInterface([
            SubObjectList(gateways_general_panels,
                          heading=_('General'), classname='gateways-general'),
            SubObjectList(gateways_2c2p_panels,
                          heading=_('2C2P(Credit Card)'), classname='gateways-2c2p'),
            SubObjectList(gateways_paypal_panels,
                          heading=_('PayPal'), classname='gateways-paypal'),
            SubObjectList(gateways_stripe_panels,
                          heading=_('Stripe'), classname='gateways-stripe'),
        ], heading=_("Gateways")),
        SubTabbedInterface([
            SubObjectList(appearance_general_panels,
                          heading=_('General'), classname='appearance-general'),
        ], heading=_("Appearance")),
    ])

    class Meta:
        verbose_name = _('Site Setting')
        verbose_name_plural = _('Site Settings')
