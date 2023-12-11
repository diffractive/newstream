import html
import functools
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from i18nfield.fields import I18nCharField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import FieldPanel
from wagtailmodelchooser.edit_handlers import ModelChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.contrib.forms.models import AbstractFormField
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from newstream.fields import I18nRichTextField
from newstream.utils import resolve_i18n_string
from donations.includes.currency_dictionary import currency_dict

GATEWAY_2C2P = '2C2P'
GATEWAY_PAYPAL = 'PayPal'
GATEWAY_PAYPAL_LEGACY = 'PayPal - Legacy'
GATEWAY_STRIPE = 'Stripe'
GATEWAY_MANUAL = 'Manual'
GATEWAY_OFFLINE = 'Offline'

GATEWAY_CAN_EDIT_SUBSCRIPTION = 'gateway-can-edit-subscription'
GATEWAY_CAN_TOGGLE_SUBSCRIPTION = 'gateway-can-toggle-subscription'
GATEWAY_CAN_CANCEL_SUBSCRIPTION = 'gateway-can-cancel-subscription'


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

    def is_paypal_legacy(self):
        return self.title == GATEWAY_PAYPAL_LEGACY

    def is_stripe(self):
        return self.title == GATEWAY_STRIPE

    def is_manual(self):
        return self.title == GATEWAY_MANUAL

    def is_offline(self):
        return self.title == GATEWAY_OFFLINE


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


class I18nAbstractFormField(AbstractFormField):
    label = I18nCharField(
        verbose_name=_('label'),
        max_length=255,
        help_text=_('The label of the form field')
    )
    help_text = I18nCharField(verbose_name=_('help text'), max_length=255, blank=True)


class UserMetaField(I18nAbstractFormField):
    parent = ParentalKey('SiteSettings', on_delete=models.CASCADE,
                         related_name='user_meta_fields')


@register_setting
class SiteSettings(BaseSetting, ClusterableModel):
    default_from_email = models.EmailField()
    default_from_name = I18nCharField(
        max_length=255,
        blank=True)
    org_contact_email = models.EmailField(blank=True, null=True,
        help_text=_("The e-mail users may use to contact the organisation"))
    email_general_panels = [
        FieldPanel('default_from_email', heading=_('Default From Email')),
        FieldPanel('default_from_name', heading=_('Default Name for From Email')),
        FieldPanel('org_contact_email', heading=_('Organisation Contact Email')),
        InlinePanel('admin_emails', label=_("Admin Email"), heading=_("List of Admins' Emails"),
                    help_text=_('Email notifications such as new donations will be sent to this list.'))
    ]

    notify_admin_account_created = models.BooleanField(null=True)
    notify_admin_account_deleted = models.BooleanField(null=True)
    notify_admin_new_donation = models.BooleanField(null=True)
    notify_admin_donation_revoked = models.BooleanField(null=True)
    notify_admin_monthly_renewal = models.BooleanField(null=True)
    notify_admin_new_recurring = models.BooleanField(null=True)
    notify_admin_recurring_adjusted = models.BooleanField(null=True)
    notify_admin_recurring_rescheduled = models.BooleanField(null=True)
    notify_admin_recurring_paused = models.BooleanField(null=True)
    notify_admin_recurring_resumed = models.BooleanField(null=True)
    notify_admin_recurring_cancelled = models.BooleanField(null=True)
    notify_admin_donation_error = models.BooleanField(null=True)
    email_admin_panels = [
        FieldPanel('notify_admin_account_created',
                   heading=_('Send admins email notifications of donor accounts being created?')),
        FieldPanel('notify_admin_account_deleted',
                   heading=_('Send admins email notifications of donor accounts being deleted?')),
        FieldPanel('notify_admin_new_donation',
                   heading=_('Send admins email notifications of donation completions? (donor returning from gateway page)')),
        FieldPanel('notify_admin_donation_revoked',
                   heading=_('Send admins email notifications of revoked donations?')),
        FieldPanel('notify_admin_monthly_renewal',
                   heading=_('Send admins email notifications of recurring donation renewals?')),
        FieldPanel('notify_admin_new_recurring',
                   heading=_('Send admins email notifications of new recurring donations?')),
        FieldPanel('notify_admin_recurring_adjusted',
                   heading=_('Send admins email notifications of recurring donations with adjusted amounts?')),
        FieldPanel('notify_admin_recurring_rescheduled',
                   heading=_('Send admins email notifications of recurring donations with rescheduled billing dates?')),
        FieldPanel('notify_admin_recurring_paused',
                   heading=_('Send admins email notifications of recurring donations being paused?')),
        FieldPanel('notify_admin_recurring_resumed',
                   heading=_('Send admins email notifications of recurring donations being resumed?')),
        FieldPanel('notify_admin_recurring_cancelled',
                   heading=_('Send admins email notifications of recurring donations being cancelled?')),
        FieldPanel('notify_admin_donation_error',
                   heading=_('Send admins email notifications of erroneous donations?')),
    ]

    social_login_enabled = models.BooleanField(null=True)
    social_skip_signup = models.BooleanField(null=True)
    signup_footer_text = I18nRichTextField(blank=True)
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
    google_login_enabled = models.BooleanField(null=True)
    signup_google_panels = [
        FieldPanel('google_login_enabled',
                   heading=_('Enable Google Login ? (Only if Social Login is enabled)')),
    ]
    facebook_login_enabled = models.BooleanField(null=True)
    signup_facebook_panels = [
        FieldPanel('facebook_login_enabled',
                   heading=_('Enable Facebook Login ? (Only if Social Login is enabled)')),
    ]
    twitter_login_enabled = models.BooleanField(null=True)
    signup_twitter_panels = [
        FieldPanel('twitter_login_enabled',
                   heading=_('Enable Twitter Login ? (Only if Social Login is enabled)')),
    ]

    sandbox_mode = models.BooleanField(null=True)
    currency = models.CharField(default='None', max_length=10, choices=[(key, html.unescape(
        val['admin_label'])) for key, val in currency_dict.items()])
    donation_form = models.ForeignKey(
        'donations.DonationForm',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    donation_updates_rate_limiter = models.BooleanField(null=True, help_text=_('Enable this will limit donor to only 5 subscription update-actions(edit/pause/resume) every 5 minutes'))
    donations_soft_delete_mode = models.BooleanField(null=True, help_text=_('Enabling this will ensure Donations and Subscriptions will still exist in the database even after being deleted from wagtail admin'))
    donations_general_panels = [
        FieldPanel('sandbox_mode', heading=_('Sandbox Mode')),
        FieldPanel('currency', heading=_('Currency')),
        ModelChooserPanel('donation_form', heading=_(
            'Donation Form to be used')),
        FieldPanel('donation_updates_rate_limiter', heading=_("Frequency Limit on Donors' Subscription Update-Actions(edit/pause/resume)?")),
        FieldPanel('donations_soft_delete_mode', heading=_("Soft Delete Mode(for Donations and Subscriptions only)")),
    ]

    _2c2p_frontend_label = I18nCharField(
        max_length=255,
        default=functools.partial(resolve_i18n_string, "2C2P(Credit Card)"),
        help_text=_("The Gateway name to be shown on the frontend website."))
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

    paypal_frontend_label = I18nCharField(
        max_length=255,
        default=functools.partial(resolve_i18n_string, "PayPal"),
        help_text=_("The Gateway name to be shown on public-facing website."))
    paypal_sandbox_api_product_id = models.CharField(
        max_length=255, blank=True, help_text=_("The Sandbox API Product ID"))
    paypal_sandbox_api_client_id = models.CharField(
        max_length=255, blank=True, help_text=_("The Sandbox API Client ID"))
    paypal_sandbox_api_secret_key = models.CharField(
        max_length=255, blank=True, help_text=_("The Sandbox API secret key"))
    paypal_sandbox_api_webhook_id = models.CharField(
        max_length=255, blank=True, help_text=_("The Sandbox API Webhook ID"))
    paypal_api_product_id = models.CharField(
        max_length=255, blank=True, help_text=_("The Live API Product ID"))
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
            FieldPanel("paypal_sandbox_api_product_id",
                       heading=_("PayPal Sandbox API Product ID")),
            FieldPanel("paypal_sandbox_api_client_id",
                       heading=_("PayPal Sandbox API Client ID")),
            FieldPanel("paypal_sandbox_api_secret_key",
                       heading=_("PayPal Sandbox API Secret Key")),
            FieldPanel("paypal_sandbox_api_webhook_id",
                       heading=_("PayPal Sandbox API Webhook ID")),
        ], heading=_("PayPal API Sandbox Settings")),
        MultiFieldPanel([
            FieldPanel("paypal_api_product_id",
                       heading=_("PayPal Live API Product ID")),
            FieldPanel("paypal_api_client_id",
                       heading=_("PayPal Live API Client ID")),
            FieldPanel("paypal_api_secret_key",
                       heading=_("PayPal Live API Secret Key")),
            FieldPanel("paypal_api_webhook_id",
                       heading=_("PayPal Live API Webhook ID")),
        ], heading=_("PayPal API Live Settings")),
    ]

    paypal_legacy_frontend_label = I18nCharField(
        max_length=255,
        default=functools.partial(resolve_i18n_string, "PayPal - Legacy"),
        help_text=_("The Gateway name to be shown on public-facing website for old Paypal transactions."))
    donations_paypal_legacy_panels = [
        FieldPanel("paypal_legacy_frontend_label", heading=_(
            "PayPal-Old Gateway public-facing label")),
    ]

    stripe_frontend_label = I18nCharField(
        max_length=255,
        default=functools.partial(resolve_i18n_string, "Stripe"),
        help_text=_("The Gateway name to be shown on the frontend website."))
    stripe_testing_webhook_secret = models.CharField(
        max_length=255, blank=True, help_text=_("The Secret for the Testing Webhook used by the server for payment verification"))
    stripe_testing_product_id = models.CharField(max_length=255, blank=True, null=True, help_text=_(
        "Testing Product ID accessible on your Stripe Dashboard"))
    stripe_testing_api_publishable_key = models.CharField(
        max_length=255, blank=True, help_text=_("The Testing API publishable key"))
    stripe_testing_api_secret_key = models.CharField(
        max_length=255, blank=True, help_text=_("The Testing API secret key"))
    stripe_webhook_secret = models.CharField(
        max_length=255, blank=True, help_text=_("The Secret for the Live Webhook used by the server for payment verification"))
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True, help_text=_(
        "Product ID accessible on your Stripe Dashboard"))
    stripe_api_publishable_key = models.CharField(
        max_length=255, blank=True, help_text=_("The Live API publishable key"))
    stripe_api_secret_key = models.CharField(
        max_length=255, blank=True, help_text=_("The Live API secret key"))

    donations_stripe_panels = [
        FieldPanel("stripe_frontend_label", heading=_(
            "Stripe Gateway public-facing label")),
        MultiFieldPanel([
            FieldPanel("stripe_testing_webhook_secret",
                   heading=_("Stripe Testing Webhook Secret")),
            FieldPanel("stripe_testing_product_id", heading=_("Stripe Testing Product ID")),
            FieldPanel("stripe_testing_api_publishable_key",
                       heading=_("Stripe Testing API Publishable Key")),
            FieldPanel("stripe_testing_api_secret_key",
                       heading=_("Stripe Testing API Secret Key")),
        ], heading=_("Stripe API Sandbox Settings")),
        MultiFieldPanel([
            FieldPanel("stripe_webhook_secret",
                   heading=_("Stripe Webhook Secret")),
            FieldPanel("stripe_product_id", heading=_("Stripe Product ID")),
            FieldPanel("stripe_api_publishable_key",
                       heading=_("Stripe Live API Publishable Key")),
            FieldPanel("stripe_api_secret_key",
                       heading=_("Stripe Live API Secret Key")),
        ], heading=_("Stripe API Live Settings")),
    ]

    manual_frontend_label = I18nCharField(
        max_length=255,
        default=functools.partial(resolve_i18n_string, "Manual"),
        help_text=_("The Gateway name to be shown on the frontend website for admin-added donations."))
    offline_frontend_label = I18nCharField(
        max_length=255,
        default=functools.partial(resolve_i18n_string, "Offline"),
        help_text=_("The Gateway name to be shown on the frontend website for offline donations."))
    offline_instructions_text = I18nRichTextField(blank=True)
    offline_thankyou_text = I18nRichTextField(blank=True)

    donations_others_panels = [
        FieldPanel("manual_frontend_label", heading=_(
            "Manual Donations public-facing label")),
        FieldPanel("offline_frontend_label", heading=_(
            "Offline Donations public-facing label")),
        FieldPanel("offline_instructions_text", heading=_(
            "Offline-donations Instructions in the donation form")),
        FieldPanel("offline_thankyou_text", heading=_(
            "Offline-donations Instructions on the thank you page")),
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
    full_org_name = models.CharField(
        max_length=255, blank=True,
        null=True, help_text=_("The full organisation name that will display in e-mails"))
    short_org_name = models.CharField(
        max_length=255, blank=True,
        null=True, help_text=_("The short form of the organisation that will be used as a signature in e-mails"))

    appearance_general_panels = [
        FieldPanel('brand_logo', heading=('Brand Logo')),
        FieldPanel('site_icon', heading=('Site Icon')),
        FieldPanel('full_org_name', heading=_('Full Organisation Name')),
        FieldPanel('short_org_name', heading=_('Short Organisation Name')),
    ]

    privacy_policy_link = models.URLField(max_length=200, default='#', blank=True)

    appearance_footer_panels = [
        FieldPanel("privacy_policy_link", heading=_(
            "Privacy policy url displayed in the footer section")),
    ]

    recaptcha_public_key = models.CharField(max_length=255, blank=True, null=True)
    recaptcha_private_key = models.CharField(max_length=255, blank=True, null=True)
    others_recaptcha_panels = [
        FieldPanel('recaptcha_public_key', heading=_('ReCAPTCHA public key')),
        FieldPanel('recaptcha_private_key', heading=_('ReCAPTCHA private key')),
    ]

    allow_daily_subscription = models.BooleanField(default=False, help_text=_('Enabling this adds "Daily" as a donation frequency option for recurring donations'))
    debug_panels = [
        FieldPanel('allow_daily_subscription', heading=_('Allow Daily Subscriptions')),
    ]

    # We add "child" to the classnames to help identify that they are the inner tabs as opposed to the top ones
    tabs_config = [
        TabbedInterface([
            ObjectList(email_general_panels, classname='child email-general',
                          heading=_('General')),
            ObjectList(email_admin_panels, classname='child email-admin',
                          heading=_('Admin Emails')),
        ], heading=_("Emails")),
        TabbedInterface([
            ObjectList(signup_general_panels, classname='child social-general',
                          heading=_('General')),
            ObjectList(signup_google_panels, classname='child social-google',
                          heading=_('Google')),
            ObjectList(signup_facebook_panels, classname='child social-facebook',
                          heading=_('Facebook')),
            ObjectList(signup_twitter_panels, classname='child social-twitter',
                          heading=_('Twitter')),
        ], heading=_("Donor Signup")),
        TabbedInterface([
            ObjectList(donations_general_panels,
                          heading=_('General'), classname='child gateways-general'),
            ObjectList(donations_2c2p_panels,
                          heading=_('2C2P(Credit Card)'), classname='child gateways-2c2p'),
            ObjectList(donations_paypal_panels,
                          heading=_('PayPal'), classname='child gateways-paypal'),
            ObjectList(donations_paypal_legacy_panels,
                          heading=_('PayPal(Legacy)'), classname='child gateways-paypal-legacy'),
            ObjectList(donations_stripe_panels,
                          heading=_('Stripe'), classname='child gateways-stripe'),
            ObjectList(donations_others_panels,
                          heading=_('Others'), classname='child gateways-others'),
        ], heading=_("Donations")),
        TabbedInterface([
            ObjectList(appearance_general_panels,
                          heading=_('General'), classname='child appearance-general'),
            ObjectList(appearance_footer_panels,
                          heading=_('Footer'), classname='child appearance-footer'),
        ], heading=_("Appearance")),
        TabbedInterface([
            ObjectList(others_recaptcha_panels,
                          heading=_('ReCAPTCHA'), classname='child others-recaptcha'),
        ], heading=_("Others")),
    ]

    if settings.DEBUG:
        tabs_config.append(TabbedInterface([
            ObjectList(debug_panels,
                        heading=_('Donation Settings'), classname='child debug-donation-settings'),
        ], heading=_("Debug")))

    edit_handler = TabbedInterface(tabs_config)

    @property
    def fields(self):
        # the following list doesn't include relational fields like admin_emails
        return [ f.name for f in self._meta.fields + self._meta.many_to_many ]

    class Meta:
        verbose_name = _('Site Setting')
        verbose_name_plural = _('Site Settings')
