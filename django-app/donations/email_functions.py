import re
import html
from pprint import pprint
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from allauth.account.utils import send_email_confirmation

from newstream.functions import get_site_settings_from_default_site, set_default_from_email
from donations.functions import getDonationEmail


def textify(html):
    # Copy links out of the anchor tags and append to text (anchor tags will be stripped next step)
    # e.g. <a href="https://google.com">Google</a> becomes <a href="https://google.com">Google(link: https://google.com)</a>
    # Below is a modified regex from https://regexr.com/39rsv that gets 4 capture groups:
    # 1. opening anchor tag
    # 2. the href link
    # 3. the wrapped text (that should not have "http")
    # 4. closing anchor tag
    html = re.sub(r'(<a(?:[^>]+)href="(?!mailto)([^"]+)"(?:[^>]*)>)((?!http)(?:.(?!\<\/a\>))*.)(<\/a>)', r'\1\3(link: \2)\4', html)
    # Remove html tags and continuous whitespaces
    text_only = re.sub('[ \t]+', ' ', strip_tags(html))
    # Strip single spaces in the beginning of each line
    text_only = text_only.replace('\n ', '\n').strip()
    # Reduce 3 or more consecutive new lines into just 2 (to fix the large empty space between title and email body)
    return re.sub('\n{3,}', '\n\n', text_only)


def setDonorLanguagePreference(user):
    if user.language_preference:
        translation.activate(user.language_preference)


def sendEmailNotificationsToDonor(user_email, subject, htmlStr):
    # setDonorLanguagePreference(user)
    site_settings = get_site_settings_from_default_site()
    # default_from_name is an I18nCharField
    if str(site_settings.default_from_name):
        from_email = '%s <%s>' % (str(site_settings.default_from_name), site_settings.default_from_email)
    else:
        from_email = site_settings.default_from_email

    try:
        send_mail(
            str(subject),
            textify(htmlStr),
            from_email,
            [user_email],
            html_message=htmlStr
        )
    except Exception as e:
        print("Cannot send '"+str(subject)+"' to '" +
              user_email+"': "+str(e), flush=True)


def sendEmailNotificationsToAdmins(site_settings, subject, htmlStr):
    # set default language for admins' emails
    # translation.activate(settings.LANGUAGE_CODE)

    # get admin_list from env vars if none is defined on wagtail admin
    db_admin_emails = site_settings.admin_emails.all()
    if len(db_admin_emails) > 0:
        admin_list = [
            admin_email.email for admin_email in site_settings.admin_emails.all()]
    elif settings.NEWSTREAM_ADMIN_EMAILS is not None:
        admin_list = settings.NEWSTREAM_ADMIN_EMAILS.split(',')

    # default_from_name is an I18nCharField
    if str(site_settings.default_from_name):
        from_email = '%s <%s>' % (str(site_settings.default_from_name), site_settings.default_from_email)
    else:
        from_email = site_settings.default_from_email
    try:
        send_mail(
            str(subject),
            textify(htmlStr),
            from_email,
            admin_list,  # requires admin list to be set in site_settings
            html_message=htmlStr
        )
    except Exception as e:
        print("Cannot send '"+str(subject) +
              "' emails to admins: "+str(e), flush=True)


def sendDonationErrorNotifToAdmins(donation, error_title, error_description):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("Donation Error")
    if site_settings.notify_admin_donation_error:
        sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
            'donations/email_templates/donation_error_admin.html', context={'donation': donation, 'mail_title': mail_title, 'error_title': error_title, 'error_description': error_description}))


def sendDonationNotifToAdmins(donation):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("New One-off Donation")
    if site_settings.notify_admin_new_donation:
        sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
            'donations/email_templates/new_donation.html', context={'donation': donation, 'mail_title': mail_title}))


def sendDonationReceiptToDonor(donation):
    mail_title = _("Thank you for your Donation")
    sendEmailNotificationsToDonor(getDonationEmail(donation), mail_title, render_to_string('donations/email_templates/donation_receipt.html', context={'donation': donation, 'mail_title': mail_title}))


def sendDonationRevokedToAdmins(donation):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("A Donation is revoked")
    if site_settings.notify_admin_donation_revoked:
        sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
            'donations/email_templates/donation_revoked_admin.html', context={'donation': donation, 'mail_title': mail_title}))


def sendDonationRevokedToDonor(donation):
    mail_title = _("Your Donation is Revoked")
    sendEmailNotificationsToDonor(getDonationEmail(donation), mail_title, render_to_string('donations/email_templates/donation_revoked_donor.html', context={'donation': donation, 'mail_title': mail_title}))


def sendDonationStatusChangeToDonor(donation):
    mail_title = _("Your Donation Status is Updated")
    sendEmailNotificationsToDonor(getDonationEmail(donation), mail_title, render_to_string('donations/email_templates/donation_status_change.html', context={'donation': donation, 'mail_title': mail_title}))


def sendSubscriptionStatusChangeToDonor(subscription):
    mail_title = _("Your Recurring Donation Status is Updated")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, render_to_string('donations/email_templates/subscription_status_change.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRenewalNotifToAdmins(donation):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("New Renewal Donation")
    if site_settings.notify_admin_monthly_renewal:
        sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
            'donations/email_templates/new_renewal.html', context={'donation': donation, 'mail_title': mail_title}))


def sendRenewalReceiptToDonor(donation):
    mail_title = _("Thank you for your Monthly Donation")
    sendEmailNotificationsToDonor(donation.user.email, mail_title, render_to_string('donations/email_templates/renewal_receipt.html', context={'donation': donation, 'mail_title': mail_title}))


def sendRecurringAdjustedNotifToAdmins(subscription):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("A Recurring Donation Amount is Adjusted")
    if site_settings.notify_admin_recurring_adjusted:
        sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
            'donations/email_templates/recurring_adjusted_admin.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringAdjustedNotifToDonor(subscription):
    mail_title = _("Your Recurring Donation Amount is Adjusted")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, render_to_string('donations/email_templates/recurring_adjusted_donor.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendNewRecurringNotifToAdmins(subscription):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("New Recurring Donation")
    if site_settings.notify_admin_new_recurring:
        sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
            'donations/email_templates/new_recurring_donation.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendNewRecurringNotifToDonor(subscription):
    mail_title = _("Thank you for setting up a Recurring Donation")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, render_to_string('donations/email_templates/recurring_new_donor.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringRescheduledNotifToAdmins(subscription):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("A Recurring Donation is Rescheduled")
    if site_settings.notify_admin_recurring_rescheduled:
        sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
            'donations/email_templates/recurring_rescheduled_admin.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringRescheduledNotifToDonor(subscription):
    mail_title = _("Your Recurring Donation is Rescheduled")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, render_to_string('donations/email_templates/recurring_rescheduled_donor.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringPausedNotifToAdmins(subscription):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("A Recurring Donation is paused")
    if site_settings.notify_admin_recurring_paused:
        sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
            'donations/email_templates/recurring_paused_admin.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringPausedNotifToDonor(subscription):
    mail_title = _("Your Recurring Donation is Paused")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, render_to_string('donations/email_templates/recurring_paused_donor.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringResumedNotifToAdmins(subscription):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("A Recurring Donation is resumed")
    if site_settings.notify_admin_recurring_resumed:
        sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
            'donations/email_templates/recurring_resumed_admin.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringResumedNotifToDonor(subscription):
    mail_title = _("Your Recurring Donation is Resumed")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, render_to_string('donations/email_templates/recurring_resumed_donor.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringCancelledNotifToAdmins(subscription):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("A Recurring Donation is cancelled")
    if site_settings.notify_admin_recurring_cancelled:
        sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
            'donations/email_templates/recurring_cancelled_admin.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringCancelRequestNotifToAdmins(subscription):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("Cancellation to a Recurring Donation is requested")
    sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
        'donations/email_templates/recurring_cancel_request_admin.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringCancelledNotifToDonor(subscription):
    mail_title = _("Your Recurring Donation is Cancelled")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, render_to_string('donations/email_templates/recurring_cancelled_donor.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendAccountCreatedNotifToAdmins(user):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("A Donor Account is created")
    if site_settings.notify_admin_account_created:
        sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
            'donations/email_templates/account_created_admin.html', context={'user': user, 'mail_title': mail_title}))


def sendAccountDeletedNotifToAdmins(user):
    site_settings = get_site_settings_from_default_site()
    mail_title = _("A Donor Account is deleted")
    if site_settings.notify_admin_account_deleted:
        sendEmailNotificationsToAdmins(site_settings, mail_title, render_to_string(
            'donations/email_templates/account_deleted_admin.html', context={'user': user, 'mail_title': mail_title}))


def sendAccountDeletedNotifToDonor(user):
    mail_title = _("Your Account is Deleted")
    sendEmailNotificationsToDonor(user.email, mail_title, render_to_string('donations/email_templates/account_deleted_donor.html', context={'user': user, 'mail_title': mail_title}))


def sendVerificationEmail(user):
    set_default_from_email()
    # allauth's email confirmation uses DEFAULT_FROM_EMAIL
    send_email_confirmation(user, True)
