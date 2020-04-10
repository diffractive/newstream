# Generated by Django 3.0.5 on 2020-04-10 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0013_donation_recurring_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='parent_donation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='donations.Donation'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='recurring_status',
            field=models.CharField(blank=True, choices=[('on-going', 'On-going'), ('cancelled', 'Cancelled'), ('non-recurring', 'Non-recurring')], default='non-recurring', max_length=255, null=True),
        ),
    ]
