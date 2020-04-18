# Generated by Django 3.0.5 on 2020-04-17 13:57

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0006_adminemails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminemails',
            name='setting_parent',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_emails', to='site_settings.GlobalSettings'),
        ),
    ]