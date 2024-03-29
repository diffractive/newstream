# Generated by Django 3.0.8 on 2021-03-31 15:46

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0027_auto_20210331_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='guest_email',
            field=models.EmailField(blank=True, default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tempdonation',
            name='guest_email',
            field=models.EmailField(blank=True, default=None, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tempdonationmeta',
            name='donation',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='temp_metas', to='donations.TempDonation'),
        ),
    ]