# Generated by Django 3.0.8 on 2020-12-17 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0019_auto_20201204_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='donation_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 17, 18, 8, 47, 734301)),
            preserve_default=False,
        ),
    ]
