# Generated by Django 3.0.8 on 2020-12-17 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0014_auto_20201217_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='donations_soft_delete_mode',
            field=models.BooleanField(default=True, help_text='Enabling this will ensure Donations and Subscriptions will still exist in the database even after being deleted from wagtail admin'),
        ),
    ]