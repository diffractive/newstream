from site_settings.models import SiteSettings
from django.conf import settings

def load_test_data():
    load_settings()

def load_settings():
    siteSettings = SiteSettings.objects.all()

    for setting in siteSettings:
        if not setting.default_from_email:
            setting.default_from_email = settings.DEFAULT_FROM_EMAIL
            setting.save()
