# Generated by Django 3.0.5 on 2020-04-30 09:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('email_campaigns', '0002_auto_20200430_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='targetgroup',
            name='users',
            field=models.ManyToManyField(limit_choices_to={'is_email_verified': True, 'opt_in_mailing_list': True}, related_name='target_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
