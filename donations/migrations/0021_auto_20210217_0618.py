# Generated by Django 3.0.8 on 2021-02-17 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0020_donation_donation_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='order_number',
            new_name='transaction_id',
        ),
    ]