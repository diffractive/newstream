from django.core.management.base import BaseCommand

from site_settings.models import SiteSettings

class Command(BaseCommand):
    """ This command exists for testing Newstream to get value from env vars
        for null site settings. Since due to previous migration files, True/False values
        are stored into these fields instead of None, we could use this command to reset
        them back to None.
    """
    help = 'Resets nullable site settings fields to None'

    def handle(self, *args, **options):
        ss = SiteSettings.objects.get(pk=1)
        
        ss.notify_admin_account_created = None
        ss.notify_admin_account_deleted = None
        ss.notify_admin_new_donation = None
        ss.notify_admin_donation_revoked = None
        ss.notify_admin_monthly_renewal = None
        ss.notify_admin_new_recurring = None
        ss.notify_admin_recurring_adjusted = None
        ss.notify_admin_recurring_rescheduled = None
        ss.notify_admin_recurring_paused = None
        ss.notify_admin_recurring_resumed = None
        ss.notify_admin_recurring_cancelled = None
        ss.notify_admin_donation_error = None

        ss.social_login_enabled = None
        ss.social_skip_signup = None
        
        ss.google_login_enabled = None
        ss.facebook_login_enabled = None
        ss.twitter_login_enabled = None

        ss.sandbox_mode = None
        ss.currency = "None"

        ss.donation_updates_rate_limiter = None
        ss.donations_soft_delete_mode = None
        
        ss.save()
        print("Nullable Site Settings fields set to None √")
