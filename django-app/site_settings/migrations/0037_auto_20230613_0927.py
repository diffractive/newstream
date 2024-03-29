# Generated by Django 3.1.11 on 2023-06-13 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0036_updates_for_envvar_compatibility'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='allow_daily_subscription',
            field=models.BooleanField(default=False, help_text='Enabling this adds "Daily" as a donation frequency option for recurring donations'),
        ),
    ]
