# Generated by Django 3.0.8 on 2020-07-25 14:26

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0006_remove_donationform_personal_footer_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationPaymentMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_key', models.CharField(max_length=255)),
                ('field_value', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('donation', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_metas', to='donations.Donation')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]