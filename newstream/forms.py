from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from newstream.functions import raiseObjectNone
# from wagtail.contrib.forms.forms import FormBuilder
from allauth.account.forms import AddEmailForm, SignupForm
from allauth.account.utils import filter_users_by_email
from donations.functions import donor_email_exists
from allauth.utils import email_address_exists
from allauth.account import app_settings as allauth_settings
User = get_user_model()


class PersonalInfoForm(forms.Form):
    email = forms.EmailField(label='Primary Email Address',
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


class NewstreamSignupForm(SignupForm):

    def clean_email(self):
        # check if email input is taken by existing donors or users
        # by current design, one user can be linked to by multiple donor records, and only one donor record is "active" for that user having the same email; this situation occurs only because of user changes his primary email
        email = self.cleaned_data['email']
        if donor_email_exists(email) or email_address_exists(email):
            raise ValidationError(
                "Email has already been taken. Login if you already have an account.")
        return email


class NewstreamAddEmailForm(AddEmailForm):

    def clean_email(self):
        value = self.cleaned_data["email"]
        errors = {
            "this_account": "This e-mail address is already associated"
            " with this account.",
            "different_account": "This e-mail address is already associated"
            " with another account.",
        }
        users = filter_users_by_email(value)
        on_this_account = [u for u in users if u.pk == self.user.pk]
        on_diff_account = [u for u in users if u.pk != self.user.pk]

        if on_this_account:
            raise forms.ValidationError(errors["this_account"])
        if on_diff_account and allauth_settings.UNIQUE_EMAIL:
            raise forms.ValidationError(errors["different_account"])

        # next check if exists as other donors' emails
        if donor_email_exists(value, exclude_user=self.user):
            raise forms.ValidationError(
                "This e-mail address is already associated with another account.")
        return value


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
