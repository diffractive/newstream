import html
import re
import secrets
from django import forms
from django.contrib.auth import get_user_model, login
from django.core.exceptions import ValidationError
from newstream.functions import raiseObjectNone, getSiteSettings
from donations.functions import getCurrencyDictAt
from wagtail.contrib.forms.forms import FormBuilder
from .models import Donor, DonationForm, DonorMeta
from .functions import setDefaultFromEmail, sendVerificationEmail
# from allauth.account.forms import SetPasswordField
from allauth.account.adapter import DefaultAccountAdapter
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
        self.request = request
        self.footer_html = form.donation_footer_text
        self.global_settings = getSiteSettings(request)
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
    # email = forms.EmailField(label='Email Address', max_length=255)
    # password1 = forms.CharField(
    #     min_length=6, widget=forms.PasswordInput, label=("Password"))
    # password2 = forms.CharField(
    #     min_length=6, widget=forms.PasswordInput, label=("Password (again)"))
    opt_in_mailing_list = forms.BooleanField(
        label='Opt in Mailing List?', required=False)
    personal_info_fields = [
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2'
    ]
    other_fields = [
        'opt_in_mailing_list'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if not request:
        #     raiseObjectNone('Please provide request object')
        # if not blueprint:
        #     raiseObjectNone('Please provide a DonationForm blueprint')
        # self.request = request
        # self.global_settings = getSiteSettings(request)
        try:
            form = DonationForm.objects.get(
                is_active__exact=True)
        except Exception as e:
            print("There should be exactly one active DonationForm.", flush=True)
            raise e
        self.footer_html = form.personal_footer_text

        # construct donor meta fields from form configuration
        donormetafields = form.donor_meta_fields.all()
        fb = FormBuilder(donormetafields)
        for key, val in fb.formfields.items():
            self.fields["donormeta_"+key] = val

    def signup(self, request, user):
        # process meta data
        donor_metas = []
        for key, val in request.POST.items():
            donormeta_key = re.match("^donormeta_([a-z_]+)$", key)
            if donormeta_key:
                donor_metas.append(DonorMeta(
                    field_key=donormeta_key.group(1), field_value=val))

        # creates a new donor
        donor = Donor(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            opt_in_mailing_list=self.cleaned_data['opt_in_mailing_list'],
            metas=donor_metas
        )
        donor.save()

        # proceed to create account
        try:
            # user.set_password(self.cleaned_data["password1"])
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.opt_in_mailing_list = self.cleaned_data['opt_in_mailing_list']
            user.is_email_verified = False
            user.save()
            # link donor to user
            donor.linked_user = user
            donor.save()
            # save to session to remember user's registration
            request.session['first_time_registration'] = True
        except Exception as e:
            print("Cannot Create new Django user: " +
                  str(e), flush=True)
            # Should have been checked against duplication in form validation
            # double check again for safety
            raise e

        # set DEFAULT_FROM_EMAIL
        setDefaultFromEmail(request)

        # logs new user in
        # login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # email verification to user
        # sendVerificationEmail(
        #     request, user)


class NewstreamAdapter(DefaultAccountAdapter):

    def clean_email(self, email):
        """
        Validates an email value. You can hook into this if you want to
        (dynamically) restrict what email addresses can be chosen.
        """
        # check if email input is taken by existing donor records
        # by current design, one user can be linked to by multiple donor records, and only one donor record is "active" for that user having the same email; this situation occurs only because of email changes by that user
        if Donor.objects.filter(email=email).exists():
            raise ValidationError(
                "Email has already been taken. Login if you already have an account.")
        return email
