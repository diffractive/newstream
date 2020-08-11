# Generated by Django 3.0.8 on 2020-08-11 20:50

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='signup_footer_text_en',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='signup_footer_text_id_id',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='signup_footer_text_ms_my',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='signup_footer_text_tl_ph',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='signup_footer_text_zh_tw',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='choices_en',
            field=models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', null=True, verbose_name='choices'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='choices_id_id',
            field=models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', null=True, verbose_name='choices'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='choices_ms_my',
            field=models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', null=True, verbose_name='choices'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='choices_tl_ph',
            field=models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', null=True, verbose_name='choices'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='choices_zh_tw',
            field=models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', null=True, verbose_name='choices'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='default_value_en',
            field=models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, null=True, verbose_name='default value'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='default_value_id_id',
            field=models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, null=True, verbose_name='default value'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='default_value_ms_my',
            field=models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, null=True, verbose_name='default value'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='default_value_tl_ph',
            field=models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, null=True, verbose_name='default value'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='default_value_zh_tw',
            field=models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, null=True, verbose_name='default value'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='help_text_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='help text'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='help_text_id_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='help text'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='help_text_ms_my',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='help text'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='help_text_tl_ph',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='help text'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='help_text_zh_tw',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='help text'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='label_en',
            field=models.CharField(help_text='The label of the form field', max_length=255, null=True, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='label_id_id',
            field=models.CharField(help_text='The label of the form field', max_length=255, null=True, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='label_ms_my',
            field=models.CharField(help_text='The label of the form field', max_length=255, null=True, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='label_tl_ph',
            field=models.CharField(help_text='The label of the form field', max_length=255, null=True, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='usermetafield',
            name='label_zh_tw',
            field=models.CharField(help_text='The label of the form field', max_length=255, null=True, verbose_name='label'),
        ),
    ]
