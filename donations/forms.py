from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from omp.functions import raiseObjectNone
from wagtail.contrib.forms.forms import FormBuilder
User = get_user_model()


class DonationWebForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=255)
    last_name = forms.CharField(label='Last Name', max_length=255)
    email = forms.EmailField(label='Email Address', max_length=255)
    opt_in_mailing_list = forms.BooleanField(
        label='Opt in Mailing List?', required=False)
    is_recurring = forms.BooleanField(
        widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, request=None, blueprint=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not request:
            raiseObjectNone('Please provide request object')
        if not blueprint:
            raiseObjectNone('Please provide a DonationForm blueprint')
        form = blueprint

        # pop fields if user logged in
        if request.user.is_authenticated:
            self.fields.pop('first_name')
            self.fields.pop('last_name')
            self.fields.pop('email')
            self.fields.pop('opt_in_mailing_list')

        # set is_recurring value and construct is_create_account field
        self.fields["is_recurring"].widget.attrs['value'] = 'True' if form.is_recurring else 'False'
        # if user is logged in, is_create_account field will not exist in the form
        if not request.user.is_authenticated:
            if form.is_recurring:
                self.fields["is_create_account"] = forms.BooleanField(widget=forms.HiddenInput(
                ), label='Create Account?', required=False, initial=form.is_recurring)
            else:
                self.fields["is_create_account"] = forms.BooleanField(
                    label='Create Account?', required=False, initial=form.is_recurring)

        # construct payment gateway field
        gateways = form.allowed_gateways.all()
        self.fields["payment_gateway"] = forms.ChoiceField(
            choices=[(x.id, x.title) for x in gateways])

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
