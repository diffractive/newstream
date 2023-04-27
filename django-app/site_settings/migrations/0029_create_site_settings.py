#
# Initial Data
#

from django.db import migrations

def initial_data(apps, schema_editor):

    Site = apps.get_model('wagtailcore.Site')
    SiteSettings = apps.get_model('site_settings', 'SiteSettings')
    DonationForm = apps.get_model('donations', 'DonationForm')

    main_form = DonationForm.objects.get(
        title = "Main Form",
    )

    default_site = Site.objects.get(
        hostname='localhost',
    )

    site_settings = SiteSettings.objects.create(
        donation_form = main_form,
        site = default_site,
        social_login_enabled = False,
    )


def remove_initial_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0036_setup_initial_data'),
        ('site_settings', '0028_auto_20210601_0712'),
    ]

    operations = [
         migrations.RunPython(initial_data, remove_initial_data),
    ]
