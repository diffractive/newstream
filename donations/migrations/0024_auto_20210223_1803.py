# Generated by Django 3.0.8 on 2021-02-23 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0023_auto_20210223_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='donation_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscribe_date',
            field=models.DateTimeField(),
        ),
    ]
