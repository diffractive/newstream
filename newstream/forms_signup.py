import re
from django import forms

from wagtail.contrib.forms.forms import FormBuilder

from newstream.functions import setDefaultFromEmail, getSiteSettings_from_default_site, process_user_meta
from newstream_user.models import UserMeta


class BaseSignupForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=255)
    last_name = forms.CharField(label='Last Name', max_length=255)
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
        user.metas = user_metas
        user.save()

        # save to session to remember user's registration
        request.session['first_time_registration'] = True

        # set DEFAULT_FROM_EMAIL for allauth
        setDefaultFromEmail(request)
