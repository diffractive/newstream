import html
from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList, RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmodelchooser.edit_handlers import ModelChooserPanel
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
    email_general_panels = [
        FieldPanel('default_from_email', heading=_('Default From Email')),
        InlinePanel('admin_emails', label=_("Admin Email"), heading=_("List of Admins' Emails"),
                    help_text=_('Email notifications such as new donations will be sent to this list.'))
    ]

    admin_receive_account_created_emails = models.BooleanField(default=True)
    admin_receive_account_deleted_emails = models.BooleanField(default=True)
    admin_receive_checkout_emails = models.BooleanField(default=True)
    admin_receive_renewal_emails = models.BooleanField(default=False)
    admin_receive_update_recurring_emails = models.BooleanField(default=True)
    admin_receive_pause_recurring_emails = models.BooleanField(default=True)
    admin_receive_resume_recurring_emails = models.BooleanField(default=True)
    admin_receive_cancel_recurring_emails = models.BooleanField(default=True)
    email_admin_panels = [
        FieldPanel('admin_receive_account_created_emails',
                   heading=_('Allow admins receive notifications of donor accounts being created?')),
        FieldPanel('admin_receive_account_deleted_emails',
                   heading=_('Allow admins receive notifications of donor accounts being deleted?')),
        FieldPanel('admin_receive_checkout_emails',
                   heading=_('Allow admins receive notifications of donation completions? (donor returning from gateway page)')),
        FieldPanel('admin_receive_renewal_emails',
                   heading=_('Allow admins receive notifications of recurring donation renewals?')),
        FieldPanel('admin_receive_update_recurring_emails',
                   heading=_('Allow admins receive notifications of recurring donations being updated?')),
        FieldPanel('admin_receive_pause_recurring_emails',
                   heading=_('Allow admins receive notifications of recurring donations being paused?')),
        FieldPanel('admin_receive_resume_recurring_emails',
                   heading=_('Allow admins receive notifications of recurring donations being resumed?')),
        FieldPanel('admin_receive_cancel_recurring_emails',
                   heading=_('Allow admins receive notifications of recurring donations being cancelled?')),
    ]

    social_login_enabled = models.BooleanField(default=True)
    social_skip_signup = models.BooleanField(default=False)
    signup_footer_text = RichTextField(blank=True)
    signup_general_panels = [
        FieldPanel('social_login_enabled',
                   heading=_('Enable Social Login for this site ?')),
        FieldPanel('social_skip_signup',
                   heading=_('Allow Firsttime Social Logins bypass Signup Form ?')),
        InlinePanel('user_meta_fields', label=_('User Meta Fields'),
                    help_text=_('Add extra fields for the user signup form for additional data you want to collect from them.')),
        FieldPanel('signup_footer_text',
                   heading=_('Footer Text(Under Signup Form)')),
    ]
    google_login_enabled = models.BooleanField(default=True)
    signup_google_panels = [
        FieldPanel('google_login_enabled',
                   heading=_('Enable Google Login ? (Only if Social Login is enabled)')),
    ]
    facebook_login_enabled = models.BooleanField(default=True)
    signup_facebook_panels = [
        FieldPanel('facebook_login_enabled',
                   heading=_('Enable Facebook Login ? (Only if Social Login is enabled)')),
    ]
    twitter_login_enabled = models.BooleanField(default=True)
    signup_twitter_panels = [
        FieldPanel('twitter_login_enabled',
                   heading=_('Enable Twitter Login ? (Only if Social Login is enabled)')),
    ]

    sandbox_mode = models.BooleanField(default=True)
    currency = models.CharField(default='USD', max_length=10, choices=[(key, html.unescape(
        val['admin_label'])) for key, val in currency_dict.items()])
    donation_form = models.ForeignKey(
        'donations.DonationForm',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    donations_general_panels = [
        FieldPanel('sandbox_mode', heading=_('Sandbox Mode')),
        FieldPanel('currency', heading=_('Currency')),
        ModelChooserPanel('donation_form', heading=_(
            'Donation Form to be used')),
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

    donations_2c2p_panels = [
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
    paypal_sandbox_api_client_id = models.CharField(
        max_length=255, blank=True, help_text=_("The Sandbox API Client ID"))
    paypal_sandbox_api_secret_key = models.CharField(
        max_length=255, blank=True, help_text=_("The Sandbox API secret key"))
    paypal_sandbox_api_webhook_id = models.CharField(
        max_length=255, blank=True, help_text=_("The Sandbox API Webhook ID"))
    paypal_api_client_id = models.CharField(
        max_length=255, blank=True, help_text=_("The Live API Client ID"))
    paypal_api_secret_key = models.CharField(
        max_length=255, blank=True, help_text=_("The Live API secret key"))
    paypal_api_webhook_id = models.CharField(
        max_length=255, blank=True, help_text=_("The Live API Webhook ID"))

    donations_paypal_panels = [
        FieldPanel("paypal_frontend_label", heading=_(
            "PayPal Gateway public-facing label")),
        MultiFieldPanel([
            FieldPanel("paypal_sandbox_api_client_id",
                       heading=_("PayPal Sandbox API Client ID")),
            FieldPanel("paypal_sandbox_api_secret_key",
                       heading=_("PayPal Sandbox API Secret Key")),
            FieldPanel("paypal_sandbox_api_webhook_id",
                       heading=_("PayPal Sandbox API Webhook ID")),
        ], heading=_("PayPal API Sandbox Settings")),
        MultiFieldPanel([
            FieldPanel("paypal_api_client_id",
                       heading=_("PayPal Live API Client ID")),
            FieldPanel("paypal_api_secret_key",
                       heading=_("PayPal Live API Secret Key")),
            FieldPanel("paypal_api_webhook_id",
                       heading=_("PayPal Live API Webhook ID")),
        ], heading=_("PayPal API Live Settings")),
    ]

    stripe_frontend_label = models.CharField(
        max_length=255, default=_("Stripe"), help_text=_("The Gateway name to be shown on public-facing website."))
    stripe_webhook_secret = models.CharField(
        max_length=255, blank=True, help_text=_("The Secret for the Webhook used by the server for payment verification"))
    stripe_product_id = models.CharField(max_length=255, blank=False, null=True, help_text=_(
        "Product ID accessible on your Stripe Dashboard"))
    stripe_testing_api_publishable_key = models.CharField(
        max_length=255, blank=True, help_text=_("The Testing API publishable key"))
    stripe_testing_api_secret_key = models.CharField(
        max_length=255, blank=True, help_text=_("The Testing API secret key"))
    stripe_api_publishable_key = models.CharField(
        max_length=255, blank=True, help_text=_("The Live API publishable key"))
    stripe_api_secret_key = models.CharField(
        max_length=255, blank=True, help_text=_("The Live API secret key"))

    donations_stripe_panels = [
        FieldPanel("stripe_frontend_label", heading=_(
            "Stripe Gateway public-facing label")),
        FieldPanel("stripe_webhook_secret",
                   heading=_("Stripe Webhook Secret")),
        FieldPanel("stripe_product_id", heading=_("Stripe Product ID")),
        MultiFieldPanel([
            FieldPanel("stripe_testing_api_publishable_key",
                       heading=_("Stripe Testing API Publishable Key")),
            FieldPanel("stripe_testing_api_secret_key",
                       heading=_("Stripe Testing API Secret Key")),
        ], heading=_("Stripe API Sandbox Settings")),
        MultiFieldPanel([
            FieldPanel("stripe_api_publishable_key",
                       heading=_("Stripe Live API Publishable Key")),
            FieldPanel("stripe_api_secret_key",
                       heading=_("Stripe Live API Secret Key")),
        ], heading=_("Stripe API Live Settings")),
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

    edit_handler = TopTabbedInterface([
        SubTabbedInterface([
            SubObjectList(email_general_panels, classname='email-general',
                          heading=_('General')),
            SubObjectList(email_admin_panels, classname='email-admin',
                          heading=_('Admin Emails')),
        ], heading=_("Emails")),
        SubTabbedInterface([
            SubObjectList(signup_general_panels, classname='social-general',
                          heading=_('General')),
            SubObjectList(signup_google_panels, classname='social-google',
                          heading=_('Google')),
            SubObjectList(signup_facebook_panels, classname='social-facebook',
                          heading=_('Facebook')),
            SubObjectList(signup_twitter_panels, classname='social-twitter',
                          heading=_('Twitter')),
        ], heading=_("Donor Signup")),
        SubTabbedInterface([
            SubObjectList(donations_general_panels,
                          heading=_('General'), classname='gateways-general'),
            SubObjectList(donations_2c2p_panels,
                          heading=_('2C2P(Credit Card)'), classname='gateways-2c2p'),
            SubObjectList(donations_paypal_panels,
                          heading=_('PayPal'), classname='gateways-paypal'),
            SubObjectList(donations_stripe_panels,
                          heading=_('Stripe'), classname='gateways-stripe'),
        ], heading=_("Donations")),
        SubTabbedInterface([
            SubObjectList(appearance_general_panels,
                          heading=_('General'), classname='appearance-general'),
        ], heading=_("Appearance")),
    ])

    class Meta:
        verbose_name = _('Site Setting')
        verbose_name_plural = _('Site Settings')
