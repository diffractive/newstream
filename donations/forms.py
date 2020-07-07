import html
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from newstream.functions import raiseObjectNone, getGlobalSettings
from donations.functions import getCurrencyDictAt
from wagtail.contrib.forms.forms import FormBuilder
from .models import Donor
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
        ('monthly', 'Monthly'),
        ('onetime', 'One-time'),
    ])
    currency = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, request=None, blueprint=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not request:
            raiseObjectNone('Please provide request object')
        if not blueprint:
            raiseObjectNone('Please provide a DonationForm blueprint')
        form = blueprint
        # set footer_html property from blueprint
        self.request = request
        self.footer_html = form.footer_text
        self.global_settings = getGlobalSettings(request)
        self.fields["currency"].initial = self.global_settings.currency

        # construct payment gateway field
        gateways = form.allowed_gateways.all()
        self.fields["payment_gateway"] = forms.ChoiceField(
            choices=[(x.id, x.frontend_label) for x in gateways], label="Payment method")

        # construct donation amount field
        currency_set = getCurrencyDictAt(self.global_settings.currency)
        if form.isAmountFixed():
            self.fields["donation_amount"] = forms.DecimalField(
                initial=form.fixed_amount)
            self.fields["donation_amount"].widget.attrs['readonly'] = True
        elif form.isAmountStepped():
            amountSteps = form.amount_steps.all()
            self.fields["donation_amount"] = forms.ChoiceField(
                choices=[(x.step, html.unescape(currency_set['symbol']) + ' ' + str(x.step)) for x in amountSteps])
        elif form.isAmountCustom():
            self.fields["donation_amount"] = forms.DecimalField()
        self.fields["donation_amount"].label = "Donation amount in " + html.unescape(
            currency_set['admin_label'])

        # construct donation meta fields from form configuration
        donationmetafields = form.donation_meta_fields.all()
        fb = FormBuilder(donationmetafields)
        for key, val in fb.formfields.items():
            self.fields["donationmeta_"+key] = val


class PersonalInfoForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=255)
    last_name = forms.CharField(label='Last Name', max_length=255)
    email = forms.EmailField(label='Email Address', max_length=255)
    opt_in_mailing_list = forms.BooleanField(
        label='Opt in Mailing List?', required=False)

    def __init__(self, *args, request=None, blueprint=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not request:
            raiseObjectNone('Please provide request object')
        if not blueprint:
            raiseObjectNone('Please provide a DonationForm blueprint')
        form = blueprint
        # set footer_html property from blueprint
        # todo: differentiate step 1 and 2 footer_text
        self.request = request
        self.footer_html = form.footer_text
        self.global_settings = getGlobalSettings(request)

        # construct donor meta fields from form configuration
        donormetafields = form.donor_meta_fields.all()
        fb = FormBuilder(donormetafields)
        for key, val in fb.formfields.items():
            self.fields["donormeta_"+key] = val

    def clean_email(self):
        email = self.cleaned_data['email']
        # check if email input is taken by existing donor records
        # by current design, one user can be linked to by multiple donor records, and only one donor record is "active" for that user having the same email; this situation occurs only because of email changes by that user
        if Donor.objects.filter(email=email).exists():
            raise ValidationError(
                "Email has already been taken. Login if you already have an account.")
        return email
