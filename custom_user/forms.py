from django import forms
from django.utils.translation import ugettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm


class CustomUserEditForm(UserEditForm):
    is_email_verified = forms.BooleanField(
        label=_("Is Email Verified"), required=False)
    opt_in_mailing_list = forms.BooleanField(
        required=False, label=_("Opt in Mailing List"))


class CustomUserCreationForm(UserCreationForm):
    is_email_verified = forms.BooleanField(
        label=_("Is Email Verified"), required=False)
    opt_in_mailing_list = forms.BooleanField(
        required=False, label=_("Opt in Mailing List"))
