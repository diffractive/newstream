from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from omp.functions import raiseObjectNone
from wagtail.contrib.forms.forms import FormBuilder
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
    'opt_in_mailing_list',
    'is_create_account'
]


class DonationWebForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=255)
    last_name = forms.CharField(label='Last Name', max_length=255)
    email = forms.EmailField(label='Email Address', max_length=255)
    opt_in_mailing_list = forms.BooleanField(
        label='Opt in Mailing List?', required=False)
    donation_frequency = forms.ChoiceField(choices=[
        ('monthly', 'Monthly'),
        ('onetime', 'One-time'),
    ])
    is_create_account = forms.BooleanField(
        label='Create a member account', required=False)

    def __init__(self, *args, request=None, blueprint=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not request:
            raiseObjectNone('Please provide request object')
        if not blueprint:
            raiseObjectNone('Please provide a DonationForm blueprint')
        form = blueprint
        # set footer_html property from blueprint
        self.footer_html = form.footer_text

        # pop fields and set readonly if user logged in
        if request.user.is_authenticated:
            self.fields["first_name"].widget.attrs['readonly'] = True
            self.fields["last_name"].widget.attrs['readonly'] = True
            self.fields["email"].widget.attrs['readonly'] = True
            self.fields["first_name"].widget.attrs['value'] = request.user.first_name
            self.fields["last_name"].widget.attrs['value'] = request.user.last_name
            self.fields["email"].widget.attrs['value'] = request.user.email
            self.fields.pop('opt_in_mailing_list')
            self.fields.pop('is_create_account')

        # construct payment gateway field
        gateways = form.allowed_gateways.all()
        self.fields["payment_gateway"] = forms.ChoiceField(
            choices=[(x.id, x.frontend_label) for x in gateways], label="Payment method")

        # construct donor meta fields from form configuration
        if not request.user.is_authenticated:
            donormetafields = form.donor_meta_fields.all()
            fb = FormBuilder(donormetafields)
            for key, val in fb.formfields.items():
                self.fields["donormeta_"+key] = val

        # construct donation amount field
        if form.isAmountFixed():
            self.fields["donation_amount"] = forms.DecimalField(
                initial=form.fixed_amount)
            self.fields["donation_amount"].widget.attrs['readonly'] = True
        elif form.isAmountStepped():
            amountSteps = form.amount_steps.all()
            self.fields["donation_amount"] = forms.ChoiceField(
                choices=[(x.step, x.step) for x in amountSteps])
        elif form.isAmountCustom():
            self.fields["donation_amount"] = forms.DecimalField()

        # construct donation meta fields from form configuration
        donationmetafields = form.donation_meta_fields.all()
        fb = FormBuilder(donationmetafields)
        for key, val in fb.formfields.items():
            self.fields["donationmeta_"+key] = val

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Email has already been taken. Login if you already have an account.")
        return email
