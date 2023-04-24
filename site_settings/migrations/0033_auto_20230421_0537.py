# Generated by Django 3.1.11 on 2023-04-21 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0032_sitesettings_default_from_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='full_org_name',
            field=models.CharField(blank=True, help_text='The full organisation name that will display in e-mails', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='org_contact_email',
            field=models.EmailField(blank=True, help_text='The e-mail users may use to contact the organisation', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='short_org_name',
            field=models.CharField(blank=True, help_text='The short form of the organisation that will be used as a signature in e-mails', max_length=255, null=True),
        ),
    ]
