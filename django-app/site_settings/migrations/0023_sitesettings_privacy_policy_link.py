# Generated by Django 3.0.8 on 2021-03-08 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0022_auto_20210225_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='privacy_policy_link',
            field=models.URLField(blank=True, default='#'),
        ),
    ]