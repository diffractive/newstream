import html
import re
import secrets
from django import forms
from django.contrib.auth import get_user_model, login
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.forms import FormBuilder

from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import email_address_exists

from newstream.functions import raiseObjectNone, getSiteSettings
from donations.functions import getCurrencyDictAt
from .models import DonationForm
User = get_user_model()


# These lists are for the categorization of fields
# Used for rendering conditions in donation_form.html
DONATION_DETAILS_FIELDS = [
    'payment_gateway',
    'donation_frequency',
    'donation_amount'
]
PERSONAL_INFO_FIELDS = [
    'first_name',
    'last_name',
    'email'
]
OTHER_FIELDS = [
    'opt_in_mailing_list'
]


class DonationDetailsForm(forms.Form):
    donation_frequency = forms.ChoiceField(choices=[
        ('monthly', _('Monthly')),
        ('onetime', _('One-time')),
    ])
    currency = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, request=None, blueprint=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not request:
            raiseObjectNone('Please provide request object')
        if not blueprint:
            raiseObjectNone('Please provide a DonationForm blueprint')
        form = blueprint
        self.request = request
        self.footer_html = form.donation_footer_text
        self.global_settings = getSiteSettings(request)
        self.fields["currency"].initial = self.global_settings.currency

        # construct payment gateway field
        gateways = form.allowed_gateways.all()
        self.fields["payment_gateway"] = forms.ChoiceField(
            choices=[(x.id, x.frontend_label) for x in gateways], label=_("Payment method"))

        # construct donation amount field
        currency_set = getCurrencyDictAt(self.global_settings.currency)
        if form.isAmountFixed():
            self.fields["donation_amount"] = forms.DecimalField(
                initial=form.fixed_amount, label=_('Donation Amount'))
            self.fields["donation_amount"].widget.attrs['readonly'] = True
        elif form.isAmountStepped():
            amountSteps = form.amount_steps.all()
            self.fields["donation_amount"] = forms.ChoiceField(
                choices=[(x.step, html.unescape(currency_set['symbol']) + ' ' + str(x.step)) for x in amountSteps], label=_('Donation Amount'))
        elif form.isAmountCustom():
            self.fields["donation_amount"] = forms.DecimalField(
                label=_('Donation Amount'))
        self.fields["donation_amount"].label = "Donation amount in " + html.unescape(
            currency_set['admin_label'])

        # construct donation meta fields from form configuration
        # todo: translations: how to translate donationmeta fields
        donationmetafields = form.donation_meta_fields.all()
        fb = FormBuilder(donationmetafields)
        for key, val in fb.formfields.items():
            if isinstance(val, forms.MultipleChoiceField):
                self.fields["donationmetalist_"+key] = val
            else:
                self.fields["donationmeta_"+key] = val
