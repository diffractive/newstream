import re
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.conf import settings

from wagtail.contrib.forms.forms import FormBuilder

from newstream.functions import setDefaultFromEmail, getSiteSettings_from_default_site, process_user_meta
from newstream_user.models import UserMeta


class BaseSignupForm(forms.Form):
    first_name = forms.CharField(label=_('First Name'), max_length=255)
    last_name = forms.CharField(label=_('Last Name'), max_length=255)
    opt_in_mailing_list = forms.BooleanField(
        label=_('Opt in Mailing List?'), required=False)
    language_preference = forms.ChoiceField(label=_('Language Preference'),
                                            required=False, choices=settings.LANGUAGES)
    personal_info_fields = [
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2'
    ]
    other_fields = [
        'language_preference',
        'opt_in_mailing_list'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        site_settings = getSiteSettings_from_default_site()
        self.footer_html = site_settings.signup_footer_text

        # construct user meta fields from site settings configuration
        usermetafields = site_settings.user_meta_fields.all()
        fb = FormBuilder(usermetafields)
        for key, val in fb.formfields.items():
            if isinstance(val, forms.MultipleChoiceField):
                self.fields["usermetalist_"+key] = val
            else:
                self.fields["usermeta_"+key] = val

    def signup(self, request, user):
        # process meta data
        user_metas = process_user_meta(request)

        # save user data
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.opt_in_mailing_list = self.cleaned_data['opt_in_mailing_list']
        user.language_preference = self.cleaned_data['language_preference']
        user.metas = user_metas
        user.save()

        # set language for email_confirmation_subject/message.txt
        # todo: translation: tested but email message does not seem to translate
        if user.language_preference:
            translation.activate(user.language_preference)

        # save to session to remember user's registration
        request.session['first_time_registration'] = True

        # set DEFAULT_FROM_EMAIL for allauth
        setDefaultFromEmail(request)
