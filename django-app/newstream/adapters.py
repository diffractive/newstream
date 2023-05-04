from django.utils.encoding import force_str

from allauth.account import app_settings
from allauth.account.adapter import DefaultAccountAdapter

# This custom adapter is created to solely override the buggy format_email_subject,
# such that ACCOUNT_EMAIL_SUBJECT_PREFIX is allowed to set None to give an empty email subject prefix
class NewstreamAccountAdapter(DefaultAccountAdapter):
    def format_email_subject(self, subject):
        prefix = app_settings.EMAIL_SUBJECT_PREFIX
        if prefix is None:
            prefix = ''
        return prefix + force_str(subject)