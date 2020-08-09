import re
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.forms.forms import FormBuilder

from allauth.utils import email_address_exists
from allauth.account import app_settings as allauth_settings
from allauth.account.models import EmailAddress
from allauth.account.utils import filter_users_by_email, user_email
from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from newstream.functions import raiseObjectNone, setDefaultFromEmail, getSiteSettings, getSiteSettings_from_default_site
from newstream_user.models import UserMeta


class PersonalInfoForm(forms.Form):
    email = forms.EmailField(label=_('Primary Email Address'),
                             max_length=255, required=False)
    first_name = forms.CharField(label=_('First Name'), max_length=255)
    last_name = forms.CharField(label=_('Last Name'), max_length=255)
    opt_in_mailing_list = forms.BooleanField(
        label=_('Opt in Mailing List?'), required=False)
    personal_info_fields = [
        'first_name',
        'last_name',
        'email',
        'opt_in_mailing_list',
    ]

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not request:
            raiseObjectNone(_('Please provide request object'))
        site_settings = getSiteSettings(request)
        usermeta_dict = {}
        for um in request.user.metas.all():
            usermeta_dict[um.field_key] = um.field_value

        # construct user meta fields from site settings configuration
        usermetafields = site_settings.user_meta_fields.all()
        fb = FormBuilder(usermetafields)
        for key, val in fb.formfields.items():
            if isinstance(val, forms.MultipleChoiceField):
                self.fields["usermetalist_"+key] = val
                self.fields["usermetalist_" +
                            key].initial = usermeta_dict[key].split(',\n') if key in usermeta_dict else None
            else:
                self.fields["usermeta_"+key] = val
                self.fields["usermeta_" +
                            key].initial = usermeta_dict[key] if key in usermeta_dict else None

        # Fill up values
        self.fields["first_name"].widget.attrs['value'] = request.user.first_name
        self.fields["last_name"].widget.attrs['value'] = request.user.last_name
        self.fields["email"].widget.attrs['value'] = request.user.email
        self.fields["email"].widget.attrs['disabled'] = True
        self.fields["email"].label += ' ' + \
            request.user.email_verification_status()
        self.fields["opt_in_mailing_list"].initial = request.user.opt_in_mailing_list


class NewstreamSAAdapter(DefaultSocialAccountAdapter):

    def is_auto_signup_allowed(self, request, sociallogin):
        # Very Important: if connect is made in pre_social_login, this method should then be never called! (According to allauth source code)
        # then decide if social login can skip signup form (draw flag from siteSettings)
        siteSettings = getSiteSettings(request)
        return siteSettings.social_skip_signup

    def pre_social_login(self, request, sociallogin):
        # social account already exists, so this is just a login
        if sociallogin.is_existing:
            return

        # some social logins don't have an email address
        if not sociallogin.email_addresses:
            return

        # find the first verified email that we get from this sociallogin
        verified_email = None
        for email in sociallogin.email_addresses:
            if email.verified:
                verified_email = email
                break

        # no verified emails found, nothing more to do
        if not verified_email:
            return

        # check if given email address already exists as a verified email on
        # an existing user's account
        try:
            existing_email = EmailAddress.objects.get(
                email__iexact=email.email, verified=True)
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        sociallogin.connect(request, existing_email.user)


class DeleteAccountForm(forms.Form):
    CONFIRM_TEXT = 'Delete My Account'
    confirm_text = forms.CharField(
        label=_('Enter Confirmation Text'), max_length=255)

    def clean_confirm_text(self):
        input_text = self.cleaned_data['confirm_text']
        if input_text != DeleteAccountForm.CONFIRM_TEXT:
            raise ValidationError(_("Your confirmation text is incorrect, please enter exactly %(target)s" % {'target': DeleteAccountForm.CONFIRM_TEXT}
                                    ))
        return input_text
