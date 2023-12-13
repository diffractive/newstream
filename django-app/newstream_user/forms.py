
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

class NewstreamUserEditForm(UserEditForm):
    opt_in_mailing_list = forms.BooleanField(
        required=False, label=_("Opt in Mailing List"))
    language_preference = forms.ChoiceField(
        required=False, choices=settings.LANGUAGES)


class NewstreamUserCreationForm(UserCreationForm):
    opt_in_mailing_list = forms.BooleanField(
        required=False, label=_("Opt in Mailing List"))
    language_preference = forms.ChoiceField(
        required=False, choices=settings.LANGUAGES)
