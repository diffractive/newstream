from django import forms
from .functions import raiseObjectNone
from wagtail.contrib.forms.forms import FormBuilder


class DonationWebForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=255)
    last_name = forms.CharField(label='Last Name', max_length=255)
    email = forms.EmailField(label='Email Address', max_length=255)
    opt_in_mailing_list = forms.BooleanField(
        label='Opt in Mailing List?', required=False)
    is_recurring = forms.BooleanField(
        widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, blueprint=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not blueprint:
            raiseObjectNone('Please provide a DonationForm blueprint')
        form = blueprint

        # set is_recurring value and construct is_create_account field
        self.fields["is_recurring"].widget.attrs['value'] = form.is_recurring
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

        # construct custom form fields from form configuration
        morefields = form.more_form_fields.all()
        fb = FormBuilder(morefields)
        for key, val in fb.formfields.items():
            self.fields["omp_more_"+key] = val

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
