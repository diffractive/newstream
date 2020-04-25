from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from omp.functions import raiseObjectNone
# from wagtail.contrib.forms.forms import FormBuilder
User = get_user_model()


class PersonalInfoForm(forms.Form):
    email = forms.EmailField(label='Email Address',
                             max_length=255, required=False)
    first_name = forms.CharField(label='First Name', max_length=255)
    last_name = forms.CharField(label='Last Name', max_length=255)
    opt_in_mailing_list = forms.BooleanField(
        label='Opt in Mailing List?', required=False)

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not request:
            raiseObjectNone('Please provide request object')

        # Fill up values
        self.fields["first_name"].widget.attrs['value'] = request.user.first_name
        self.fields["last_name"].widget.attrs['value'] = request.user.last_name
        self.fields["email"].widget.attrs['value'] = request.user.email
        self.fields["email"].widget.attrs['disabled'] = True
        self.fields["email"].label += ' ' + \
            request.user.email_verification_status()
        self.fields["opt_in_mailing_list"].initial = request.user.opt_in_mailing_list


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label='New Email Address',
                             max_length=255)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Email has already been taken.")
        return email


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('old_password')


class DeleteAccountForm(forms.Form):
    CONFIRM_TEXT = 'Delete My Account'
    confirm_text = forms.CharField(
        label='Enter Confirmation Text', max_length=255)

    def clean_confirm_text(self):
        input_text = self.cleaned_data['confirm_text']
        if input_text != DeleteAccountForm.CONFIRM_TEXT:
            raise ValidationError("Your confirmation text is incorrect, please enter exactly '{}'".format(
                DeleteAccountForm.CONFIRM_TEXT))
        return input_text
