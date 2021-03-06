# Generated by Django 3.0.8 on 2020-08-21 10:58

from django.db import migrations

from site_settings.models import GATEWAY_2C2P, GATEWAY_PAYPAL, GATEWAY_STRIPE

def populate_supported_gateways(apps, schema_editor):
    # We can't import the PaymentGateway model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    PaymentGateway = apps.get_model('site_settings', 'PaymentGateway')

    supported_gateways = [
        {
            "title": GATEWAY_2C2P,
            "frontend_label_attr_name": "_2c2p_frontend_label",
            "list_order": 0
        },
        {
            "title": GATEWAY_PAYPAL,
            "frontend_label_attr_name": "paypal_frontend_label",
            "list_order": 1
        },
        {
            "title": GATEWAY_STRIPE,
            "frontend_label_attr_name": "stripe_frontend_label",
            "list_order": 2
        }
    ]

    for gateway_args in supported_gateways:
        gateway = PaymentGateway(**gateway_args)
        gateway.save()

class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_supported_gateways),
    ]
