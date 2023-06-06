# Generated by Django 3.1.11 on 2023-05-17 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0033_auto_20230421_0537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sitesettings',
            old_name='limit_fiveactions_per_fivemins',
            new_name='donation_updates_rate_limiter',
        ),
        migrations.RenameField(
            model_name='sitesettings',
            old_name='admin_receive_account_created_emails',
            new_name='notify_admin_account_created',
        ),
        migrations.RenameField(
            model_name='sitesettings',
            old_name='admin_receive_account_deleted_emails',
            new_name='notify_admin_account_deleted',
        ),
        migrations.RenameField(
            model_name='sitesettings',
            old_name='admin_receive_revoked_emails',
            new_name='notify_admin_donation_revoked',
        ),
        migrations.RenameField(
            model_name='sitesettings',
            old_name='admin_receive_renewal_emails',
            new_name='notify_admin_monthly_renewal',
        ),
        migrations.RenameField(
            model_name='sitesettings',
            old_name='admin_receive_checkout_emails',
            new_name='notify_admin_new_donation',
        ),
        migrations.RenameField(
            model_name='sitesettings',
            old_name='admin_receive_new_recurring_emails',
            new_name='notify_admin_new_recurring',
        ),
        migrations.RenameField(
            model_name='sitesettings',
            old_name='admin_receive_adjusted_recurring_emails',
            new_name='notify_admin_recurring_adjusted',
        ),
        migrations.RenameField(
            model_name='sitesettings',
            old_name='admin_receive_cancel_recurring_emails',
            new_name='notify_admin_recurring_cancelled',
        ),
        migrations.RenameField(
            model_name='sitesettings',
            old_name='admin_receive_pause_recurring_emails',
            new_name='notify_admin_recurring_paused',
        ),
        migrations.RenameField(
            model_name='sitesettings',
            old_name='admin_receive_rescheduled_recurring_emails',
            new_name='notify_admin_recurring_rescheduled',
        ),
        migrations.RenameField(
            model_name='sitesettings',
            old_name='admin_receive_resume_recurring_emails',
            new_name='notify_admin_recurring_resumed',
        ),
        migrations.RenameField(
            model_name='sitesettings',
            old_name='admin_receive_donation_error_emails',
            new_name='notify_admin_donation_error',
        ),
    ]