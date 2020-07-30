# Generated by Django 3.0.8 on 2020-07-18 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('donations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='linked_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='donationmetafield',
            name='form',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='donation_meta_fields', to='donations.DonationForm'),
        ),
        migrations.AddField(
            model_name='donationmeta',
            name='donation',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='metas', to='donations.Donation'),
        ),
        migrations.AddField(
            model_name='donationform',
            name='allowed_gateways',
            field=models.ManyToManyField(to='donations.PaymentGateway'),
        ),
        migrations.AddField(
            model_name='donation',
            name='donor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='donations.Donor'),
        ),
        migrations.AddField(
            model_name='donation',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='donations.DonationForm'),
        ),
        migrations.AddField(
            model_name='donation',
            name='gateway',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='donations.PaymentGateway'),
        ),
        migrations.AddField(
            model_name='donation',
            name='parent_donation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='donations.Donation'),
        ),
        migrations.AddField(
            model_name='amountstep',
            name='form',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount_steps', to='donations.DonationForm'),
        ),
        migrations.AlterUniqueTogether(
            name='amountstep',
            unique_together={('form', 'step')},
        ),
    ]