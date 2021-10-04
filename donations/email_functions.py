import html
from pprint import pprint
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from allauth.account.utils import send_email_confirmation

from newstream.functions import get_site_settings_from_default_site, set_default_from_email
from donations.functions import getDonationEmail
from donations.templates.donations.email_templates.plain_texts import get_donation_revoked_admin_text, get_donation_revoked_donor_text, get_new_donation_admin_text, get_donation_receipt_text, get_donation_status_change_text, get_new_recurring_admin_text, get_new_recurring_donor_text, get_recurring_rescheduled_admin_text, get_recurring_rescheduled_donor_text, get_subscription_status_change_text, get_new_renewal_text, get_renewal_receipt_text, get_recurring_adjusted_admin_text, get_recurring_adjusted_donor_text, get_recurring_paused_admin_text, get_recurring_paused_donor_text, get_recurring_resumed_admin_text, get_recurring_resumed_donor_text, get_recurring_cancelled_admin_text, get_recurring_cancel_request_admin_text, get_recurring_cancelled_donor_text, get_account_created_admin_text, get_account_deleted_admin_text, get_account_deleted_donor_text, get_donation_error_admin_text


def setDonorLanguagePreference(user):
    if user.language_preference:
        translation.activate(user.language_preference)


def sendEmailNotificationsToDonor(user_email, subject, textStr, htmlStr):
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
            textStr,
            from_email,
            [user_email],
            html_message=htmlStr
        )
    except Exception as e:
        print("Cannot send '"+str(subject)+"' to '" +
              user_email+"': "+str(e), flush=True)


def sendEmailNotificationsToAdmins(site_settings, subject, textStr, htmlStr):
    # set default language for admins' emails
    # translation.activate(settings.LANGUAGE_CODE)

    admin_list = [
        admin_email.email for admin_email in site_settings.admin_emails.all()]
    # default_from_name is an I18nCharField
    if str(site_settings.default_from_name):
        from_email = '%s <%s>' % (str(site_settings.default_from_name), site_settings.default_from_email)
    else:
        from_email = site_settings.default_from_email
    try:
        send_mail(
            str(subject),
            textStr,
            from_email,
            admin_list,  # requires admin list to be set in site_settings
            html_message=htmlStr
        )
    except Exception as e:
        print("Cannot send '"+str(subject) +
              "' emails to admins: "+str(e), flush=True)


def sendDonationErrorNotifToAdmins(donation, error_title, error_description):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("Donation Error")
    if siteSettings.admin_receive_donation_error_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_donation_error_admin_text(donation, error_title, error_description), render_to_string(
            'donations/email_templates/donation_error_admin.html', context={'donation': donation, 'mail_title': mail_title, 'error_title': error_title, 'error_description': error_description}))


def sendDonationNotifToAdmins(donation):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("New One-off Donation")
    if siteSettings.admin_receive_checkout_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_new_donation_admin_text(donation), render_to_string(
            'donations/email_templates/new_donation.html', context={'donation': donation, 'mail_title': mail_title}))


def sendDonationReceiptToDonor(donation):
    mail_title = _("Thank you for your Donation")
    sendEmailNotificationsToDonor(getDonationEmail(donation), mail_title, get_donation_receipt_text(donation), render_to_string('donations/email_templates/donation_receipt.html', context={'donation': donation, 'mail_title': mail_title}))


def sendDonationRevokedToAdmins(donation):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("A Donation is revoked")
    if siteSettings.admin_receive_revoked_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_donation_revoked_admin_text(donation), render_to_string(
            'donations/email_templates/donation_revoked_admin.html', context={'donation': donation, 'mail_title': mail_title}))


def sendDonationRevokedToDonor(donation):
    mail_title = _("Your Donation is Revoked")
    sendEmailNotificationsToDonor(getDonationEmail(donation), mail_title, get_donation_revoked_donor_text(donation), render_to_string('donations/email_templates/donation_revoked_donor.html', context={'donation': donation, 'mail_title': mail_title}))


def sendDonationStatusChangeToDonor(donation):
    mail_title = _("Your Donation Status is Updated")
    sendEmailNotificationsToDonor(getDonationEmail(donation), mail_title, get_donation_status_change_text(donation), render_to_string('donations/email_templates/donation_status_change.html', context={'donation': donation, 'mail_title': mail_title}))


def sendSubscriptionStatusChangeToDonor(subscription):
    mail_title = _("Your Recurring Donation Status is Updated")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, get_subscription_status_change_text(subscription), render_to_string('donations/email_templates/subscription_status_change.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRenewalNotifToAdmins(donation):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("New Renewal Donation")
    if siteSettings.admin_receive_renewal_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_new_renewal_text(donation), render_to_string(
            'donations/email_templates/new_renewal.html', context={'donation': donation, 'mail_title': mail_title}))


def sendRenewalReceiptToDonor(donation):
    mail_title = _("Thank you for your Monthly Donation")
    sendEmailNotificationsToDonor(donation.user.email, mail_title, get_renewal_receipt_text(donation), render_to_string('donations/email_templates/renewal_receipt.html', context={'donation': donation, 'mail_title': mail_title}))


def sendRecurringAdjustedNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("A Recurring Donation Amount is Adjusted")
    if siteSettings.admin_receive_adjusted_recurring_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_recurring_adjusted_admin_text(subscription), render_to_string(
            'donations/email_templates/recurring_adjusted_admin.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringAdjustedNotifToDonor(subscription):
    mail_title = _("Your Recurring Donation Amount is Adjusted")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, get_recurring_adjusted_donor_text(subscription), render_to_string('donations/email_templates/recurring_adjusted_donor.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendNewRecurringNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("New Recurring Donation")
    if siteSettings.admin_receive_new_recurring_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_new_recurring_admin_text(subscription), render_to_string(
            'donations/email_templates/new_recurring_donation.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendNewRecurringNotifToDonor(subscription):
    mail_title = _("Thank you for setting up a Recurring Donation")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, get_new_recurring_donor_text(subscription), render_to_string('donations/email_templates/recurring_new_donor.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringRescheduledNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("A Recurring Donation is Rescheduled")
    if siteSettings.admin_receive_rescheduled_recurring_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_recurring_rescheduled_admin_text(subscription), render_to_string(
            'donations/email_templates/recurring_rescheduled_admin.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringRescheduledNotifToDonor(subscription):
    mail_title = _("Your Recurring Donation is Rescheduled")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, get_recurring_rescheduled_donor_text(subscription), render_to_string('donations/email_templates/recurring_rescheduled_donor.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringPausedNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("A Recurring Donation is paused")
    if siteSettings.admin_receive_pause_recurring_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_recurring_paused_admin_text(subscription), render_to_string(
            'donations/email_templates/recurring_paused_admin.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringPausedNotifToDonor(subscription):
    mail_title = _("Your Recurring Donation is Paused")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, get_recurring_paused_donor_text(subscription), render_to_string('donations/email_templates/recurring_paused_donor.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringResumedNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("A Recurring Donation is resumed")
    if siteSettings.admin_receive_resume_recurring_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_recurring_resumed_admin_text(subscription), render_to_string(
            'donations/email_templates/recurring_resumed_admin.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringResumedNotifToDonor(subscription):
    mail_title = _("Your Recurring Donation is Resumed")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, get_recurring_resumed_donor_text(subscription), render_to_string('donations/email_templates/recurring_resumed_donor.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringCancelledNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("A Recurring Donation is cancelled")
    if siteSettings.admin_receive_cancel_recurring_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_recurring_cancelled_admin_text(subscription), render_to_string(
            'donations/email_templates/recurring_cancelled_admin.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringCancelRequestNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("Cancellation to a Recurring Donation is requested")
    sendEmailNotificationsToAdmins(siteSettings, mail_title, get_recurring_cancel_request_admin_text(subscription), render_to_string(
        'donations/email_templates/recurring_cancel_request_admin.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendRecurringCancelledNotifToDonor(subscription):
    mail_title = _("Your Recurring Donation is Cancelled")
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, get_recurring_cancelled_donor_text(subscription), render_to_string('donations/email_templates/recurring_cancelled_donor.html', context={'subscription': subscription, 'mail_title': mail_title}))


def sendAccountCreatedNotifToAdmins(user):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("A Donor Account is created")
    if siteSettings.admin_receive_account_created_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_account_created_admin_text(user), render_to_string(
            'donations/email_templates/account_created_admin.html', context={'user': user, 'mail_title': mail_title}))


def sendAccountDeletedNotifToAdmins(user):
    siteSettings = get_site_settings_from_default_site()
    mail_title = _("A Donor Account is deleted")
    if siteSettings.admin_receive_account_deleted_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_account_deleted_admin_text(user), render_to_string(
            'donations/email_templates/account_deleted_admin.html', context={'user': user, 'mail_title': mail_title}))


def sendAccountDeletedNotifToDonor(user):
    mail_title = _("Your Account is Deleted")
    sendEmailNotificationsToDonor(user.email, mail_title, get_account_deleted_donor_text(user), render_to_string('donations/email_templates/account_deleted_donor.html', context={'user': user, 'mail_title': mail_title}))


def sendVerificationEmail(user):
    set_default_from_email()
    # allauth's email confirmation uses DEFAULT_FROM_EMAIL
    send_email_confirmation(user, True)
