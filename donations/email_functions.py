import html
from pprint import pprint
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from allauth.account.utils import send_email_confirmation

from newstream.functions import getSiteSettings, getDefaultFromEmail, setDefaultFromEmail
from donations.functions import getDonationEmail
from donations.templates.donations.email_templates.plain_texts import get_donation_revoked_admin_text, get_donation_revoked_donor_text, get_new_donation_text, get_donation_receipt_text, get_donation_status_change_text, get_new_recurring_admin_text, get_new_recurring_donor_text, get_recurring_rescheduled_admin_text, get_recurring_rescheduled_donor_text, get_subscription_status_change_text, get_new_renewal_text, get_renewal_receipt_text, get_recurring_adjusted_admin_text, get_recurring_adjusted_donor_text, get_recurring_paused_admin_text, get_recurring_paused_donor_text, get_recurring_resumed_admin_text, get_recurring_resumed_donor_text, get_recurring_cancelled_admin_text, get_recurring_cancel_request_admin_text, get_recurring_cancelled_donor_text, get_account_created_admin_text, get_account_deleted_admin_text, get_account_deleted_donor_text, get_donation_error_admin_text


def setDonorLanguagePreference(user):
    if user.language_preference:
        translation.activate(user.language_preference)


def sendEmailNotificationsToDonor(request, user_email, subject, textStr, htmlStr):
    # setDonorLanguagePreference(user)
    try:
        send_mail(
            subject,
            textStr,
            getDefaultFromEmail(request),
            [user_email],
            html_message=htmlStr
        )
    except Exception as e:
        print("Cannot send '"+subject+"' to '" +
              user_email+"': "+str(e), flush=True)


def sendEmailNotificationsToAdmins(request, siteSettings, subject, textStr, htmlStr):
    # set default language for admins' emails
    # translation.activate(settings.LANGUAGE_CODE)

    admin_list = [
        admin_email.email for admin_email in siteSettings.admin_emails.all()]
    try:
        send_mail(
            subject,
            textStr,
            getDefaultFromEmail(request),
            admin_list,  # requires admin list to be set in siteSettings
            html_message=htmlStr
        )
    except Exception as e:
        print("Cannot send '"+subject +
              "' emails to admins: "+str(e), flush=True)


def sendDonationErrorNotifToAdmins(request, donation, error_title, error_description):
    siteSettings = getSiteSettings(request)
    if siteSettings.admin_receive_donation_error_emails:
        sendEmailNotificationsToAdmins(request, siteSettings, str(_("Donation Error")), get_donation_error_admin_text(request, donation, error_title, error_description), render_to_string(
            'donations/email_templates/donation_error_admin.html', context={'donation': donation, 'error_title': error_title, 'error_description': error_description}, request=request))


def sendDonationNotifToAdmins(request, donation):
    siteSettings = getSiteSettings(request)
    mail_title = str(_("New Donation"))
    if siteSettings.admin_receive_checkout_emails:
        sendEmailNotificationsToAdmins(request, siteSettings, mail_title, get_new_donation_text(request, donation), render_to_string(
            'donations/email_templates/new_donation.html', context={'donation': donation}, request=request))


def sendDonationReceiptToDonor(request, donation):
    mail_title = str(_("Thank You! This is your Donation Receipt."))
    sendEmailNotificationsToDonor(request, getDonationEmail(donation), mail_title, get_donation_receipt_text(
        request, donation), render_to_string('donations/email_templates/donation_receipt.html', context={'donation': donation}, request=request))


def sendDonationRevokedToAdmins(request, donation):
    siteSettings = getSiteSettings(request)
    mail_title = str(_("A Donation is revoked"))
    if siteSettings.admin_receive_revoked_emails:
        sendEmailNotificationsToAdmins(request, siteSettings, mail_title, get_donation_revoked_admin_text(request, donation), render_to_string(
            'donations/email_templates/donation_revoked_admin.html', context={'donation': donation}, request=request))


def sendDonationRevokedToDonor(request, donation):
    mail_title = str(_("Your Donation is revoked."))
    sendEmailNotificationsToDonor(request, getDonationEmail(donation), mail_title, get_donation_revoked_donor_text(
        request, donation), render_to_string('donations/email_templates/donation_revoked_donor.html', context={'donation': donation}, request=request))


def sendDonationStatusChangeToDonor(request, donation):
    mail_title = str(_("Your Donation Payment Status has been updated."))
    sendEmailNotificationsToDonor(request, getDonationEmail(donation), mail_title, get_donation_status_change_text(
        request, donation), render_to_string('donations/email_templates/donation_status_change.html', context={'donation': donation}, request=request))


def sendSubscriptionStatusChangeToDonor(request, subscription):
    mail_title = str(_("Your Recurring Donation Status has been updated."))
    sendEmailNotificationsToDonor(request, subscription.user.email, mail_title, get_subscription_status_change_text(
        request, subscription), render_to_string('donations/email_templates/subscription_status_change.html', context={'subscription': subscription}, request=request))


def sendRenewalNotifToAdmins(request, donation):
    siteSettings = getSiteSettings(request)
    if siteSettings.admin_receive_renewal_emails:
        sendEmailNotificationsToAdmins(request, siteSettings, str(_("New Renewal Donation")), get_new_renewal_text(request, donation), render_to_string(
            'donations/email_templates/new_renewal.html', context={'donation': donation}, request=request))


def sendRenewalReceiptToDonor(request, donation):
    sendEmailNotificationsToDonor(request, donation.user.email, str(_("Thank You! This is your Renewal Donation Receipt.")), get_renewal_receipt_text(
        request, donation), render_to_string('donations/email_templates/renewal_receipt.html', context={'donation': donation}, request=request))


def sendRecurringAdjustedNotifToAdmins(request, subscription):
    siteSettings = getSiteSettings(request)
    if siteSettings.admin_receive_adjusted_recurring_emails:
        sendEmailNotificationsToAdmins(request, siteSettings, "A Recurring Donation Amount is Adjusted", get_recurring_adjusted_admin_text(request, subscription), render_to_string(
            'donations/email_templates/recurring_adjusted_admin.html', context={'subscription': subscription}, request=request))


def sendRecurringAdjustedNotifToDonor(request, subscription):
    sendEmailNotificationsToDonor(request, subscription.user.email, "Your Recurring Donation is Adjusted", get_recurring_adjusted_donor_text(
        request, subscription), render_to_string('donations/email_templates/recurring_adjusted_donor.html', context={'subscription': subscription}, request=request))


def sendNewRecurringNotifToAdmins(request, subscription):
    siteSettings = getSiteSettings(request)
    if siteSettings.admin_receive_new_recurring_emails:
        sendEmailNotificationsToAdmins(request, siteSettings, "New Recurring Donation", get_new_recurring_admin_text(request, subscription), render_to_string(
            'donations/email_templates/new_recurring_donation.html', context={'subscription': subscription}, request=request))


def sendNewRecurringNotifToDonor(request, subscription):
    sendEmailNotificationsToDonor(request, subscription.user.email, "Your New Recurring Donation is Activated", get_new_recurring_donor_text(
        request, subscription), render_to_string('donations/email_templates/recurring_activated.html', context={'subscription': subscription}, request=request))


def sendRecurringRescheduledNotifToAdmins(request, subscription):
    siteSettings = getSiteSettings(request)
    if siteSettings.admin_receive_rescheduled_recurring_emails:
        sendEmailNotificationsToAdmins(request, siteSettings, "A Recurring Donation is Rescheduled", get_recurring_rescheduled_admin_text(request, subscription), render_to_string(
            'donations/email_templates/recurring_rescheduled_admin.html', context={'subscription': subscription}, request=request))


def sendRecurringRescheduledNotifToDonor(request, subscription):
    sendEmailNotificationsToDonor(request, subscription.user.email, "Your Recurring Donation is Rescheduled", get_recurring_rescheduled_donor_text(
        request, subscription), render_to_string('donations/email_templates/recurring_rescheduled_donor.html', context={'subscription': subscription}, request=request))


def sendRecurringPausedNotifToAdmins(request, subscription):
    siteSettings = getSiteSettings(request)
    if siteSettings.admin_receive_pause_recurring_emails:
        sendEmailNotificationsToAdmins(request, siteSettings, str(_("A Recurring Donation is paused")), get_recurring_paused_admin_text(request, subscription), render_to_string(
            'donations/email_templates/recurring_paused_admin.html', context={'subscription': subscription}, request=request))


def sendRecurringPausedNotifToDonor(request, subscription):
    sendEmailNotificationsToDonor(request, subscription.user.email, str(_("Your Recurring Donation is paused")), get_recurring_paused_donor_text(
        request, subscription), render_to_string('donations/email_templates/recurring_paused_donor.html', context={'subscription': subscription}, request=request))


def sendRecurringResumedNotifToAdmins(request, subscription):
    siteSettings = getSiteSettings(request)
    if siteSettings.admin_receive_resume_recurring_emails:
        sendEmailNotificationsToAdmins(request, siteSettings, str(_("A Recurring Donation is resumed")), get_recurring_resumed_admin_text(request, subscription), render_to_string(
            'donations/email_templates/recurring_resumed_admin.html', context={'subscription': subscription}, request=request))


def sendRecurringResumedNotifToDonor(request, subscription):
    sendEmailNotificationsToDonor(request, subscription.user.email, str(_("Your Recurring Donation is resumed")), get_recurring_resumed_donor_text(
        request, subscription), render_to_string('donations/email_templates/recurring_resumed_donor.html', context={'subscription': subscription}, request=request))


def sendRecurringCancelledNotifToAdmins(request, subscription):
    siteSettings = getSiteSettings(request)
    if siteSettings.admin_receive_cancel_recurring_emails:
        sendEmailNotificationsToAdmins(request, siteSettings, str(_("A Recurring Donation is cancelled")), get_recurring_cancelled_admin_text(request, subscription), render_to_string(
            'donations/email_templates/recurring_cancelled_admin.html', context={'subscription': subscription}, request=request))


def sendRecurringCancelRequestNotifToAdmins(request, subscription):
    siteSettings = getSiteSettings(request)
    sendEmailNotificationsToAdmins(request, siteSettings, str(_("Cancellation to a Recurring Donation is requested")), get_recurring_cancel_request_admin_text(request, subscription), render_to_string(
        'donations/email_templates/recurring_cancel_request_admin.html', context={'subscription': subscription}, request=request))


def sendRecurringCancelledNotifToDonor(request, subscription):
    sendEmailNotificationsToDonor(request, subscription.user.email, str(_("Your Recurring Donation is cancelled")), get_recurring_cancelled_donor_text(
        request, subscription), render_to_string('donations/email_templates/recurring_cancelled_donor.html', context={'subscription': subscription}, request=request))


def sendAccountCreatedNotifToAdmins(request, user):
    siteSettings = getSiteSettings(request)
    if siteSettings.admin_receive_account_created_emails:
        sendEmailNotificationsToAdmins(request, siteSettings, str(_("A Donor Account is created")), get_account_created_admin_text(request, user), render_to_string(
            'donations/email_templates/account_created_admin.html', context={'user': user}, request=request))


def sendAccountDeletedNotifToAdmins(request, user):
    siteSettings = getSiteSettings(request)
    if siteSettings.admin_receive_account_deleted_emails:
        sendEmailNotificationsToAdmins(request, siteSettings, str(_("A Donor Account is deleted")), get_account_deleted_admin_text(request, user), render_to_string(
            'donations/email_templates/account_deleted_admin.html', context={'user': user}, request=request))


def sendAccountDeletedNotifToDonor(request, user):
    sendEmailNotificationsToDonor(request, user.email, str(_("Your Account is deleted")), get_account_deleted_donor_text(
        request, user), render_to_string('donations/email_templates/account_deleted_donor.html', context={'user': user}, request=request))


def sendVerificationEmail(request, user):
    setDefaultFromEmail(request)
    # allauth's email confirmation uses DEFAULT_FROM_EMAIL
    send_email_confirmation(request, user, True)
