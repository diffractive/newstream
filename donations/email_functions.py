import html
from pprint import pprint
from django.conf import settings
from django.core.mail import send_mail
from django.template import Template, RequestContext
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from allauth.account.utils import send_email_confirmation

from donations.email_template_ids import ET_ADN_ACCOUNT_CREATED, ET_ADN_ACCOUNT_DELETED, ET_ADN_DONATION_ERROR, ET_ADN_DONATION_REVOKED, ET_ADN_NEW_DONATION, ET_ADN_NEW_SUBSCRIPTION, ET_ADN_RENEWAL_DONATION, ET_ADN_SUBSCRIPTION_ADJUSTED, ET_ADN_SUBSCRIPTION_CANCELLED, ET_ADN_SUBSCRIPTION_CANCEL_REQUEST, ET_ADN_SUBSCRIPTION_PAUSED, ET_ADN_SUBSCRIPTION_RESCHEDULED, ET_ADN_SUBSCRIPTION_RESUMED, ET_DNR_ACCOUNT_DELETED, ET_DNR_DONATION_RECEIPT, ET_DNR_DONATION_REVOKED, ET_DNR_DONATION_STATUS_UPDATED, ET_DNR_NEW_SUBSCRIPTION, ET_DNR_RENEWAL_RECEIPT, ET_DNR_SUBSCRIPTION_ADJUSTED, ET_DNR_SUBSCRIPTION_CANCELLED, ET_DNR_SUBSCRIPTION_PAUSED, ET_DNR_SUBSCRIPTION_RESCHEDULED, ET_DNR_SUBSCRIPTION_RESUMED, ET_DNR_SUBSCRIPTION_STATUS_UPDATED
from newstream.functions import getSiteSettings, getDefaultFromEmail, setDefaultFromEmail, _exception
from donations.functions import getDonationEmail
from donations.templates.donations.email_templates.plain_texts import get_donation_revoked_admin_text, get_donation_revoked_donor_text, get_new_donation_text, get_donation_receipt_text, get_donation_status_change_text, get_new_recurring_admin_text, get_new_recurring_donor_text, get_recurring_rescheduled_admin_text, get_recurring_rescheduled_donor_text, get_subscription_status_change_text, get_new_renewal_text, get_renewal_receipt_text, get_recurring_adjusted_admin_text, get_recurring_adjusted_donor_text, get_recurring_paused_admin_text, get_recurring_paused_donor_text, get_recurring_resumed_admin_text, get_recurring_resumed_donor_text, get_recurring_cancelled_admin_text, get_recurring_cancel_request_admin_text, get_recurring_cancelled_donor_text, get_account_created_admin_text, get_account_deleted_admin_text, get_account_deleted_donor_text, get_donation_error_admin_text
from donations.models import EmailTemplate


def setDonorLanguagePreference(user):
    if user.language_preference:
        translation.activate(user.language_preference)


def sendEmailNotificationsToDonor(request, user_email, subject, textStr, htmlStr):
    # setDonorLanguagePreference(user)
    siteSettings = getSiteSettings(request)
    try:
        # The return value will be the number of successfully delivered messages (which can be 0 or 1 since it can only send one message).
        return send_mail(
            subject,
            textStr,
            '%s <%s>' % (siteSettings.default_from_name, getDefaultFromEmail(request)),
            [user_email],
            html_message=htmlStr
        )
    except Exception as e:
        _exception("Cannot send '"+subject+"' to '" +
              user_email+"': "+str(e))
        return -1


def sendEmailNotificationsToAdmins(request, siteSettings, subject, textStr, htmlStr, admin_list=None):
    # set default language for admins' emails
    # translation.activate(settings.LANGUAGE_CODE)

    if admin_list is None:
        admin_list = [
            admin_email.email for admin_email in siteSettings.admin_emails.all()]
    try:
        # The return value will be the number of successfully delivered messages (which can be 0 or 1 since it can only send one message).
        return send_mail(
            subject,
            textStr,
            '%s <%s>' % (siteSettings.default_from_name, getDefaultFromEmail(request)),
            admin_list,  # requires admin list to be set in siteSettings
            html_message=htmlStr
        )
    except Exception as e:
        _exception("Cannot send '"+subject +
              "' emails to admins: "+str(e))
        return -1


def getEmailTemplateByID(template_id):
    try:
        et = EmailTemplate.objects.get(template_id=template_id)
        return et
    except EmailTemplate.DoesNotExist as e:
        _exception(str(e))
        return None


def sendDonationReceiptToDonor(request, donation, override_email=None):
    emailTemplate = getEmailTemplateByID(ET_DNR_DONATION_RECEIPT)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Thank You! This is your Donation Receipt."))
    mail_text = get_donation_receipt_text(request, donation, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_donation_receipt_text(request, donation)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'donation': donation})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/donation_receipt.html', context={'donation': donation}, request=request)
    return sendEmailNotificationsToDonor(request, getDonationEmail(donation) if not override_email else override_email if not override_email else override_email, mail_subject, mail_text, mail_html)


def sendDonationRevokedToDonor(request, donation, override_email=None):
    emailTemplate = getEmailTemplateByID(ET_DNR_DONATION_REVOKED)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Your Donation is revoked."))
    mail_text = get_donation_revoked_donor_text(request, donation, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_donation_revoked_donor_text(request, donation)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'donation': donation})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/donation_revoked_donor.html', context={'donation': donation}, request=request)
    return sendEmailNotificationsToDonor(request, getDonationEmail(donation) if not override_email else override_email, mail_subject, mail_text, mail_html)


def sendDonationStatusChangeToDonor(request, donation, override_email=None):
    emailTemplate = getEmailTemplateByID(ET_DNR_DONATION_STATUS_UPDATED)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Your Donation Payment Status has been updated."))
    mail_text = get_donation_status_change_text(request, donation, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_donation_status_change_text(request, donation)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'donation': donation})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/donation_status_change.html', context={'donation': donation}, request=request)
    return sendEmailNotificationsToDonor(request, getDonationEmail(donation) if not override_email else override_email, mail_subject, mail_text, mail_html)


def sendSubscriptionStatusChangeToDonor(request, subscription, override_email=None):
    emailTemplate = getEmailTemplateByID(ET_DNR_SUBSCRIPTION_STATUS_UPDATED)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Your Recurring Donation Status has been updated."))
    mail_text = get_subscription_status_change_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_subscription_status_change_text(request, subscription)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/subscription_status_change.html', context={'subscription': subscription}, request=request)
    return sendEmailNotificationsToDonor(request, subscription.user.email if not override_email else override_email, mail_subject, mail_text, mail_html)


def sendRenewalReceiptToDonor(request, donation, override_email=None):
    emailTemplate = getEmailTemplateByID(ET_DNR_RENEWAL_RECEIPT)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Thank You! This is your Renewal Donation Receipt."))
    mail_text = get_renewal_receipt_text(request, donation, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_renewal_receipt_text(request, donation)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'donation': donation})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/renewal_receipt.html', context={'donation': donation}, request=request)
    return sendEmailNotificationsToDonor(request, donation.user.email if not override_email else override_email, mail_subject, mail_text, mail_html)


def sendRecurringAdjustedNotifToDonor(request, subscription, override_email=None):
    emailTemplate = getEmailTemplateByID(ET_DNR_SUBSCRIPTION_ADJUSTED)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Your Recurring Donation is Adjusted"))
    mail_text = get_recurring_adjusted_donor_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_recurring_adjusted_donor_text(request, subscription)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/recurring_adjusted_donor.html', context={'subscription': subscription}, request=request)
    return sendEmailNotificationsToDonor(request, subscription.user.email if not override_email else override_email, mail_subject, mail_text, mail_html)


def sendNewRecurringNotifToDonor(request, subscription, override_email=None):
    emailTemplate = getEmailTemplateByID(ET_DNR_NEW_SUBSCRIPTION)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Your New Recurring Donation is Activated"))
    mail_text = get_new_recurring_donor_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_new_recurring_donor_text(request, subscription)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/recurring_activated.html', context={'subscription': subscription}, request=request)
    return sendEmailNotificationsToDonor(request, subscription.user.email if not override_email else override_email, mail_subject, mail_text, mail_html)


def sendRecurringRescheduledNotifToDonor(request, subscription, override_email=None):
    emailTemplate = getEmailTemplateByID(ET_DNR_SUBSCRIPTION_RESCHEDULED)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Your Recurring Donation is Rescheduled"))
    mail_text = get_recurring_rescheduled_donor_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_recurring_rescheduled_donor_text(request, subscription)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/recurring_rescheduled_donor.html', context={'subscription': subscription}, request=request)
    return sendEmailNotificationsToDonor(request, subscription.user.email if not override_email else override_email, mail_subject, mail_text, mail_html)


def sendRecurringPausedNotifToDonor(request, subscription, override_email=None):
    emailTemplate = getEmailTemplateByID(ET_DNR_SUBSCRIPTION_PAUSED)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Your Recurring Donation is paused"))
    mail_text = get_recurring_paused_donor_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_recurring_paused_donor_text(request, subscription)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/recurring_paused_donor.html', context={'subscription': subscription}, request=request)
    return sendEmailNotificationsToDonor(request, subscription.user.email if not override_email else override_email, mail_subject, mail_text, mail_html)


def sendRecurringResumedNotifToDonor(request, subscription, override_email=None):
    emailTemplate = getEmailTemplateByID(ET_DNR_SUBSCRIPTION_RESUMED)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Your Recurring Donation is resumed"))
    mail_text = get_recurring_resumed_donor_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_recurring_resumed_donor_text(request, subscription)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/recurring_resumed_donor.html', context={'subscription': subscription}, request=request)
    return sendEmailNotificationsToDonor(request, subscription.user.email if not override_email else override_email, mail_subject, mail_text, mail_html)


def sendRecurringCancelledNotifToDonor(request, subscription, override_email=None):
    emailTemplate = getEmailTemplateByID(ET_DNR_SUBSCRIPTION_CANCELLED)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Your Recurring Donation is cancelled"))
    mail_text = get_recurring_cancelled_donor_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_recurring_cancelled_donor_text(request, subscription)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/recurring_cancelled_donor.html', context={'subscription': subscription}, request=request)
    return sendEmailNotificationsToDonor(request, subscription.user.email if not override_email else override_email, mail_subject, mail_text, mail_html)


def sendAccountDeletedNotifToDonor(request, user, override_email=None):
    emailTemplate = getEmailTemplateByID(ET_DNR_ACCOUNT_DELETED)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Your Account is deleted"))
    mail_text = get_account_deleted_donor_text(request, user, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_account_deleted_donor_text(request, user)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'user': user})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/account_deleted_donor.html', context={'user': user}, request=request)
    return sendEmailNotificationsToDonor(request, user.email if not override_email else override_email, mail_subject, mail_text, mail_html)


def sendDonationErrorNotifToAdmins(request, donation, error_title, error_description, override_flag=False, override_emails=None):
    siteSettings = getSiteSettings(request)
    if override_flag or siteSettings.admin_receive_donation_error_emails:
        emailTemplate = getEmailTemplateByID(ET_ADN_DONATION_ERROR)
        mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Donation Error"))
        mail_text = get_donation_error_admin_text(request, donation, error_title, error_description, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_donation_error_admin_text(request, donation, error_title, error_description)
        mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'donation': donation, 'error_title': error_title, 'error_description': error_description})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
            'donations/email_templates/donation_error_admin.html', context={'donation': donation, 'error_title': error_title, 'error_description': error_description}, request=request)
        return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendDonationNotifToAdmins(request, donation, override_flag=False, override_emails=None):
    siteSettings = getSiteSettings(request)
    if override_flag or siteSettings.admin_receive_checkout_emails:
        emailTemplate = getEmailTemplateByID(ET_ADN_NEW_DONATION)
        mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("New Donation"))
        mail_text = get_new_donation_text(request, donation, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_new_donation_text(request, donation)
        mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'donation': donation})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
            'donations/email_templates/new_donation.html', context={'donation': donation}, request=request)
        return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendDonationRevokedToAdmins(request, donation, override_flag=False, override_emails=None):
    siteSettings = getSiteSettings(request)
    if override_flag or siteSettings.admin_receive_revoked_emails:
        emailTemplate = getEmailTemplateByID(ET_ADN_DONATION_REVOKED)
        mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("A Donation is revoked"))
        mail_text = get_donation_revoked_admin_text(request, donation, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_donation_revoked_admin_text(request, donation)
        mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'donation': donation})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
            'donations/email_templates/donation_revoked_admin.html', context={'donation': donation}, request=request)
        return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendRenewalNotifToAdmins(request, donation, override_flag=False, override_emails=None):
    siteSettings = getSiteSettings(request)
    if override_flag or siteSettings.admin_receive_renewal_emails:
        emailTemplate = getEmailTemplateByID(ET_ADN_RENEWAL_DONATION)
        mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("New Renewal Donation"))
        mail_text = get_new_renewal_text(request, donation, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_new_renewal_text(request, donation)
        mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'donation': donation})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
            'donations/email_templates/new_renewal.html', context={'donation': donation}, request=request)
        return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendRecurringAdjustedNotifToAdmins(request, subscription, override_flag=False, override_emails=None):
    siteSettings = getSiteSettings(request)
    if override_flag or siteSettings.admin_receive_adjusted_recurring_emails:
        emailTemplate = getEmailTemplateByID(ET_ADN_SUBSCRIPTION_ADJUSTED)
        mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("A Recurring Donation Amount is Adjusted"))
        mail_text = get_recurring_adjusted_admin_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_recurring_adjusted_admin_text(request, subscription)
        mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
            'donations/email_templates/recurring_adjusted_admin.html', context={'subscription': subscription}, request=request)
        return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendNewRecurringNotifToAdmins(request, subscription, override_flag=False, override_emails=None):
    siteSettings = getSiteSettings(request)
    if override_flag or siteSettings.admin_receive_new_recurring_emails:
        emailTemplate = getEmailTemplateByID(ET_ADN_NEW_SUBSCRIPTION)
        mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("New Recurring Donation"))
        mail_text = get_new_recurring_admin_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_new_recurring_admin_text(request, subscription)
        mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
            'donations/email_templates/new_recurring_donation.html', context={'subscription': subscription}, request=request)
        return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendRecurringRescheduledNotifToAdmins(request, subscription, override_flag=False, override_emails=None):
    siteSettings = getSiteSettings(request)
    if override_flag or siteSettings.admin_receive_rescheduled_recurring_emails:
        emailTemplate = getEmailTemplateByID(ET_ADN_SUBSCRIPTION_RESCHEDULED)
        mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("A Recurring Donation is Rescheduled"))
        mail_text = get_recurring_rescheduled_admin_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_recurring_rescheduled_admin_text(request, subscription)
        mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
            'donations/email_templates/recurring_rescheduled_admin.html', context={'subscription': subscription}, request=request)
        return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendRecurringPausedNotifToAdmins(request, subscription, override_flag=False, override_emails=None):
    siteSettings = getSiteSettings(request)
    if override_flag or siteSettings.admin_receive_pause_recurring_emails:
        emailTemplate = getEmailTemplateByID(ET_ADN_SUBSCRIPTION_PAUSED)
        mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("A Recurring Donation is paused"))
        mail_text = get_recurring_paused_admin_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_recurring_paused_admin_text(request, subscription)
        mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
            'donations/email_templates/recurring_paused_admin.html', context={'subscription': subscription}, request=request)
        return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendRecurringResumedNotifToAdmins(request, subscription, override_flag=False, override_emails=None):
    siteSettings = getSiteSettings(request)
    if override_flag or siteSettings.admin_receive_resume_recurring_emails:
        emailTemplate = getEmailTemplateByID(ET_ADN_SUBSCRIPTION_RESUMED)
        mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("A Recurring Donation is resumed"))
        mail_text = get_recurring_resumed_admin_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_recurring_resumed_admin_text(request, subscription)
        mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
            'donations/email_templates/recurring_resumed_admin.html', context={'subscription': subscription}, request=request)
        return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendRecurringCancelledNotifToAdmins(request, subscription, override_flag=False, override_emails=None):
    siteSettings = getSiteSettings(request)
    if override_flag or siteSettings.admin_receive_cancel_recurring_emails:
        emailTemplate = getEmailTemplateByID(ET_ADN_SUBSCRIPTION_CANCELLED)
        mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("A Recurring Donation is cancelled"))
        mail_text = get_recurring_cancelled_admin_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_recurring_cancelled_admin_text(request, subscription)
        mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
            'donations/email_templates/recurring_cancelled_admin.html', context={'subscription': subscription}, request=request)
        return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendRecurringCancelRequestNotifToAdmins(request, subscription, override_emails=None):
    siteSettings = getSiteSettings(request)
    emailTemplate = getEmailTemplateByID(ET_ADN_SUBSCRIPTION_CANCEL_REQUEST)
    mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("Cancellation to a Recurring Donation is requested"))
    mail_text = get_recurring_cancel_request_admin_text(request, subscription, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_recurring_cancel_request_admin_text(request, subscription)
    mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'subscription': subscription})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
        'donations/email_templates/recurring_cancel_request_admin.html', context={'subscription': subscription}, request=request)
    return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendAccountCreatedNotifToAdmins(request, user, override_flag=False, override_emails=None):
    siteSettings = getSiteSettings(request)
    if override_flag or siteSettings.admin_receive_account_created_emails:
        emailTemplate = getEmailTemplateByID(ET_ADN_ACCOUNT_CREATED)
        mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("A Donor Account is created"))
        mail_text = get_account_created_admin_text(request, user, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_account_created_admin_text(request, user)
        mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'user': user})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
            'donations/email_templates/account_created_admin.html', context={'user': user}, request=request)
        return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendAccountDeletedNotifToAdmins(request, user, override_flag=False, override_emails=None):
    siteSettings = getSiteSettings(request)
    if override_flag or siteSettings.admin_receive_account_deleted_emails:
        emailTemplate = getEmailTemplateByID(ET_ADN_ACCOUNT_DELETED)
        mail_subject = emailTemplate.email_subject if emailTemplate and emailTemplate.email_subject else str(_("A Donor Account is deleted"))
        mail_text = get_account_deleted_admin_text(request, user, text=emailTemplate.email_text_body) if emailTemplate and emailTemplate.email_text_body else get_account_deleted_admin_text(request, user)
        mail_html = Template(emailTemplate.email_html_body).render(RequestContext(request, {'user': user})) if emailTemplate and emailTemplate.email_html_body else render_to_string(
            'donations/email_templates/account_deleted_admin.html', context={'user': user}, request=request)
        return sendEmailNotificationsToAdmins(request, siteSettings, mail_subject, mail_text, mail_html, admin_list=override_emails)


def sendVerificationEmail(request, user):
    setDefaultFromEmail(request)
    # allauth's email confirmation uses DEFAULT_FROM_EMAIL
    send_email_confirmation(request, user, True)
