# Generated by Django 3.0.8 on 2021-01-06 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0015_auto_20201217_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='recaptcha_private_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='recaptcha_public_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
