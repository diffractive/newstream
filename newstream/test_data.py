from newstream.functions import get_site_settings_from_default_site
from site_settings.models import AdminEmails, SiteSettings
from django.conf import settings

def load_test_data():
    load_settings()

def load_settings():
    """ Load necessary settings in order to let the app run smoothly e.g. sending emails ok
    """
    site_settings = SiteSettings.objects.get(pk=1)

    # set default from email address
    site_settings.default_from_email = settings.DEFAULT_FROM_EMAIL
    site_settings.default_from_name = 'Admin'
    
    # set default admin_emails list
    site_settings.admin_emails.add(AdminEmails(
        title="Admin",
        email=settings.DEFAULT_ADMIN_EMAIL,
    ))
    site_settings.save()
