# Generated by Django 3.1.11 on 2021-05-31 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0025_usermetafield_clean_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitesettings',
            name='_2c2p_frontend_label_en',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='_2c2p_frontend_label_id_id',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='_2c2p_frontend_label_ms',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='_2c2p_frontend_label_tl',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='_2c2p_frontend_label_zh_hant',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='manual_frontend_label_en',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='manual_frontend_label_id_id',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='manual_frontend_label_ms',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='manual_frontend_label_tl',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='manual_frontend_label_zh_hant',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_frontend_label_en',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_frontend_label_id_id',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_frontend_label_ms',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_frontend_label_tl',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_frontend_label_zh_hant',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_instructions_text_en',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_instructions_text_id_id',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_instructions_text_ms',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_instructions_text_tl',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_instructions_text_zh_hant',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_thankyou_text_en',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_thankyou_text_id_id',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_thankyou_text_ms',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_thankyou_text_tl',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='offline_thankyou_text_zh_hant',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='paypal_frontend_label_en',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='paypal_frontend_label_id_id',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='paypal_frontend_label_ms',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='paypal_frontend_label_tl',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='paypal_frontend_label_zh_hant',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='paypal_legacy_frontend_label_en',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='paypal_legacy_frontend_label_id_id',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='paypal_legacy_frontend_label_ms',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='paypal_legacy_frontend_label_tl',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='paypal_legacy_frontend_label_zh_hant',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='signup_footer_text_en',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='signup_footer_text_id_id',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='signup_footer_text_ms',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='signup_footer_text_tl',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='signup_footer_text_zh_hant',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='stripe_frontend_label_en',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='stripe_frontend_label_id_id',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='stripe_frontend_label_ms',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='stripe_frontend_label_tl',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='stripe_frontend_label_zh_hant',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='choices_en',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='choices_id_id',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='choices_ms',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='choices_tl',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='choices_zh_hant',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='default_value_en',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='default_value_id_id',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='default_value_ms',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='default_value_tl',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='default_value_zh_hant',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='help_text_en',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='help_text_id_id',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='help_text_ms',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='help_text_tl',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='help_text_zh_hant',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='label_en',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='label_id_id',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='label_ms',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='label_tl',
        ),
        migrations.RemoveField(
            model_name='usermetafield',
            name='label_zh_hant',
        ),
    ]