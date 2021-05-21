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
from donations.templates.donations.email_templates.plain_texts import get_donation_revoked_admin_text, get_donation_revoked_donor_text, get_new_donation_text, get_donation_receipt_text, get_donation_status_change_text, get_new_recurring_admin_text, get_new_recurring_donor_text, get_recurring_rescheduled_admin_text, get_recurring_rescheduled_donor_text, get_subscription_status_change_text, get_new_renewal_text, get_renewal_receipt_text, get_recurring_adjusted_admin_text, get_recurring_adjusted_donor_text, get_recurring_paused_admin_text, get_recurring_paused_donor_text, get_recurring_resumed_admin_text, get_recurring_resumed_donor_text, get_recurring_cancelled_admin_text, get_recurring_cancel_request_admin_text, get_recurring_cancelled_donor_text, get_account_created_admin_text, get_account_deleted_admin_text, get_account_deleted_donor_text, get_donation_error_admin_text


def setDonorLanguagePreference(user):
    if user.language_preference:
        translation.activate(user.language_preference)


def sendEmailNotificationsToDonor(user_email, subject, textStr, htmlStr):
    # setDonorLanguagePreference(user)
    site_settings = get_site_settings_from_default_site()

    try:
        send_mail(
            subject,
            textStr,
            site_settings.default_from_email,
            [user_email],
            html_message=htmlStr
        )
    except Exception as e:
        print("Cannot send '"+subject+"' to '" +
              user_email+"': "+str(e), flush=True)


def sendEmailNotificationsToAdmins(site_settings, subject, textStr, htmlStr):
    # set default language for admins' emails
    # translation.activate(settings.LANGUAGE_CODE)

    admin_list = [
        admin_email.email for admin_email in site_settings.admin_emails.all()]
    try:
        send_mail(
            subject,
            textStr,
            site_settings.default_from_email,
            admin_list,  # requires admin list to be set in site_settings
            html_message=htmlStr
        )
    except Exception as e:
        print("Cannot send '"+subject +
              "' emails to admins: "+str(e), flush=True)


def sendDonationErrorNotifToAdmins(donation, error_title, error_description):
    siteSettings = get_site_settings_from_default_site()
    if siteSettings.admin_receive_donation_error_emails:
        sendEmailNotificationsToAdmins(siteSettings, str(_("Donation Error")), get_donation_error_admin_text(donation, error_title, error_description), render_to_string(
            'donations/email_templates/donation_error_admin.html', context={'donation': donation, 'error_title': error_title, 'error_description': error_description}))


def sendDonationNotifToAdmins(donation):
    siteSettings = get_site_settings_from_default_site()
    mail_title = str(_("New Donation"))
    if siteSettings.admin_receive_checkout_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_new_donation_text(donation), render_to_string(
            'donations/email_templates/new_donation.html', context={'donation': donation}))


def sendDonationReceiptToDonor(donation):
    mail_title = str(_("Thank You! This is your Donation Receipt."))
    sendEmailNotificationsToDonor(getDonationEmail(donation), mail_title, get_donation_receipt_text(donation), render_to_string('donations/email_templates/donation_receipt.html', context={'donation': donation}))


def sendDonationRevokedToAdmins(donation):
    siteSettings = get_site_settings_from_default_site()
    mail_title = str(_("A Donation is revoked"))
    if siteSettings.admin_receive_revoked_emails:
        sendEmailNotificationsToAdmins(siteSettings, mail_title, get_donation_revoked_admin_text(donation), render_to_string(
            'donations/email_templates/donation_revoked_admin.html', context={'donation': donation}))


def sendDonationRevokedToDonor(donation):
    mail_title = str(_("Your Donation is revoked."))
    sendEmailNotificationsToDonor(getDonationEmail(donation), mail_title, get_donation_revoked_donor_text(donation), render_to_string('donations/email_templates/donation_revoked_donor.html', context={'donation': donation}))


def sendDonationStatusChangeToDonor(donation):
    mail_title = str(_("Your Donation Payment Status has been updated."))
    sendEmailNotificationsToDonor(getDonationEmail(donation), mail_title, get_donation_status_change_text(donation), render_to_string('donations/email_templates/donation_status_change.html', context={'donation': donation}))


def sendSubscriptionStatusChangeToDonor(subscription):
    mail_title = str(_("Your Recurring Donation Status has been updated."))
    sendEmailNotificationsToDonor(subscription.user.email, mail_title, get_subscription_status_change_text(subscription), render_to_string('donations/email_templates/subscription_status_change.html', context={'subscription': subscription}))


def sendRenewalNotifToAdmins(donation):
    siteSettings = get_site_settings_from_default_site()
    if siteSettings.admin_receive_renewal_emails:
        sendEmailNotificationsToAdmins(siteSettings, str(_("New Renewal Donation")), get_new_renewal_text(donation), render_to_string(
            'donations/email_templates/new_renewal.html', context={'donation': donation}))


def sendRenewalReceiptToDonor(donation):
    sendEmailNotificationsToDonor(donation.user.email, str(_("Thank You! This is your Renewal Donation Receipt.")), get_renewal_receipt_text(donation), render_to_string('donations/email_templates/renewal_receipt.html', context={'donation': donation}))


def sendRecurringAdjustedNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    if siteSettings.admin_receive_adjusted_recurring_emails:
        sendEmailNotificationsToAdmins(siteSettings, "A Recurring Donation Amount is Adjusted", get_recurring_adjusted_admin_text(subscription), render_to_string(
            'donations/email_templates/recurring_adjusted_admin.html', context={'subscription': subscription}))


def sendRecurringAdjustedNotifToDonor(subscription):
    sendEmailNotificationsToDonor(subscription.user.email, "Your Recurring Donation is Adjusted", get_recurring_adjusted_donor_text(subscription), render_to_string('donations/email_templates/recurring_adjusted_donor.html', context={'subscription': subscription}))


def sendNewRecurringNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    if siteSettings.admin_receive_new_recurring_emails:
        sendEmailNotificationsToAdmins(siteSettings, "New Recurring Donation", get_new_recurring_admin_text(subscription), render_to_string(
            'donations/email_templates/new_recurring_donation.html', context={'subscription': subscription}))


def sendNewRecurringNotifToDonor(subscription):
    sendEmailNotificationsToDonor(subscription.user.email, "Your New Recurring Donation is Activated", get_new_recurring_donor_text(subscription), render_to_string('donations/email_templates/recurring_activated.html', context={'subscription': subscription}))


def sendRecurringRescheduledNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    if siteSettings.admin_receive_rescheduled_recurring_emails:
        sendEmailNotificationsToAdmins(siteSettings, "A Recurring Donation is Rescheduled", get_recurring_rescheduled_admin_text(subscription), render_to_string(
            'donations/email_templates/recurring_rescheduled_admin.html', context={'subscription': subscription}))


def sendRecurringRescheduledNotifToDonor(subscription):
    sendEmailNotificationsToDonor(subscription.user.email, "Your Recurring Donation is Rescheduled", get_recurring_rescheduled_donor_text(subscription), render_to_string('donations/email_templates/recurring_rescheduled_donor.html', context={'subscription': subscription}))


def sendRecurringPausedNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    if siteSettings.admin_receive_pause_recurring_emails:
        sendEmailNotificationsToAdmins(siteSettings, str(_("A Recurring Donation is paused")), get_recurring_paused_admin_text(subscription), render_to_string(
            'donations/email_templates/recurring_paused_admin.html', context={'subscription': subscription}))


def sendRecurringPausedNotifToDonor(subscription):
    sendEmailNotificationsToDonor(subscription.user.email, str(_("Your Recurring Donation is paused")), get_recurring_paused_donor_text(subscription), render_to_string('donations/email_templates/recurring_paused_donor.html', context={'subscription': subscription}))


def sendRecurringResumedNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    if siteSettings.admin_receive_resume_recurring_emails:
        sendEmailNotificationsToAdmins(siteSettings, str(_("A Recurring Donation is resumed")), get_recurring_resumed_admin_text(subscription), render_to_string(
            'donations/email_templates/recurring_resumed_admin.html', context={'subscription': subscription}))


def sendRecurringResumedNotifToDonor(subscription):
    sendEmailNotificationsToDonor(subscription.user.email, str(_("Your Recurring Donation is resumed")), get_recurring_resumed_donor_text(subscription), render_to_string('donations/email_templates/recurring_resumed_donor.html', context={'subscription': subscription}))


def sendRecurringCancelledNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    if siteSettings.admin_receive_cancel_recurring_emails:
        sendEmailNotificationsToAdmins(siteSettings, str(_("A Recurring Donation is cancelled")), get_recurring_cancelled_admin_text(subscription), render_to_string(
            'donations/email_templates/recurring_cancelled_admin.html', context={'subscription': subscription}))


def sendRecurringCancelRequestNotifToAdmins(subscription):
    siteSettings = get_site_settings_from_default_site()
    sendEmailNotificationsToAdmins(siteSettings, str(_("Cancellation to a Recurring Donation is requested")), get_recurring_cancel_request_admin_text(subscription), render_to_string(
        'donations/email_templates/recurring_cancel_request_admin.html', context={'subscription': subscription}))


def sendRecurringCancelledNotifToDonor(subscription):
    sendEmailNotificationsToDonor(subscription.user.email, str(_("Your Recurring Donation is cancelled")), get_recurring_cancelled_donor_text(subscription), render_to_string('donations/email_templates/recurring_cancelled_donor.html', context={'subscription': subscription}))


def sendAccountCreatedNotifToAdmins(user):
    siteSettings = get_site_settings_from_default_site()
    if siteSettings.admin_receive_account_created_emails:
        sendEmailNotificationsToAdmins(siteSettings, str(_("A Donor Account is created")), get_account_created_admin_text(user), render_to_string(
            'donations/email_templates/account_created_admin.html', context={'user': user}))


def sendAccountDeletedNotifToAdmins(user):
    siteSettings = get_site_settings_from_default_site()
    if siteSettings.admin_receive_account_deleted_emails:
        sendEmailNotificationsToAdmins(siteSettings, str(_("A Donor Account is deleted")), get_account_deleted_admin_text(user), render_to_string(
            'donations/email_templates/account_deleted_admin.html', context={'user': user}))


def sendAccountDeletedNotifToDonor(user):
    sendEmailNotificationsToDonor(user.email, str(_("Your Account is deleted")), get_account_deleted_donor_text(user), render_to_string('donations/email_templates/account_deleted_donor.html', context={'user': user}))


def sendVerificationEmail(user):
    set_default_from_email()
    # allauth's email confirmation uses DEFAULT_FROM_EMAIL
    send_email_confirmation(user, True)
