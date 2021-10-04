from django.utils.translation import gettext as _

from newstream.functions import get_site_name, get_site_url, reverse_with_site_url
from donations.functions import displayDonationAmountWithCurrency, displayRecurringAmountWithCurrency, displayGateway


def get_new_donation_admin_text(donation):
    return _("""
Hi Admins,\n
This email is to inform you that a new donation has been made on your website:\n
%(url)s\n
\n
Donor name: %(name)s\n
Donor email: %(email)s\n
Transaction ID: %(transaction_id)s\n
Donation frequency: %(frequency)s\n
Payment method: %(gateway)s\n
Donation amount: %(amount)s\n
Payment status: %(status)s\n
%(recurring_status)s
\n
Thank you,\n
%(sitename)s""") % {
        'url': reverse_with_site_url('donations_donation_modeladmin_inspect', kwargs={'instance_pk': donation.id}),
        'name': donation.display_donor_name(),
        'email': donation.display_donor_email(),
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': donation.gateway,
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring and donation.subscription else '',
        'sitename': get_site_name()
    }


def get_donation_receipt_text(donation):
    donation_url = reverse_with_site_url('donations:my-recurring-donations') if donation.is_recurring else reverse_with_site_url('donations:my-onetime-donations')
    if donation.user:
        url_text = str(_('Sign into our support page (click "forgot password?" if you have trouble logging in) to view your donation(%(url)s). Please email donations@hongkongfp.com if you have any further enquiries.') % {'url': donation_url})
    else:
        url_text = ''
    return _("""
Dear %(name)s,\n
A big "thank you" for your kind %(amount)s donation - it is very much appreciated and it will go a long way in supporting our operations.\n
Your contribution will be well-spent, allowing us to invest more in original reporting and safeguard press freedom. Please check out HKFP's latest Annual Report(https://hongkongfp.com/hong-kong-free-press-annual-report-2020/) - it includes our yearly, audited Transparency Report(https://hongkongfp.com/hong-kong-free-press-transparency-report-2019/), so you can see how carefully we spend our income.\n
%(url_text)s\n
From all of us, thank you for helping us keep independent media alive in Hong Kong!\n
Details of your donation:\n
\n
Transaction ID: %(transaction_id)s\n
Donation frequency: %(frequency)s\n
Payment method: %(gateway)s\n
Donation amount: %(amount)s\n
Payment status: %(status)s\n
%(recurring_status)s
\n
Thank you,\n
%(sitename)s""") % {
        'name': donation.display_donor(),
        'url_text': url_text,
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': displayGateway(donation),
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring and donation.subscription else '',
        'sitename': get_site_name()
    }


def get_donation_revoked_admin_text(donation):
    return _("""
Hi Admins,\n
This email is to inform you that a donation has been revoked on your website:\n
%(url)s\n
\n
Donor name: %(name)s\n
Donor email: %(email)s\n
Transaction ID: %(transaction_id)s\n
Donation frequency: %(frequency)s\n
Payment method: %(gateway)s\n
Donation amount: %(amount)s\n
Payment status: %(status)s\n
%(recurring_status)s
\n
Thank you,\n
%(sitename)s""") % {
        'url': reverse_with_site_url('donations_donation_modeladmin_inspect', kwargs={'instance_pk': donation.id}),
        'name': donation.display_donor_name(),
        'email': donation.display_donor_email(),
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': donation.gateway,
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring and donation.subscription else '',
        'sitename': get_site_name()
    }


def get_donation_revoked_donor_text(donation):
    donation_url = reverse_with_site_url('donations:my-recurring-donations') if donation.is_recurring else reverse_with_site_url('donations:my-onetime-donations')
    if donation.user:
        url_text = str(_('Go to %(url)s to view your donation on the website.') % {'url': donation_url})
    else:
        url_text = ''
    return _("""
Dear %(name)s,\n
Your donation is unfortunately revoked by the payment gateway. %(url_text)s\n
Here are the details of your donation:\n
\n
Transaction ID: %(transaction_id)s\n
Donation frequency: %(frequency)s\n
Payment method: %(gateway)s\n
Donation amount: %(amount)s\n
Payment status: %(status)s\n
%(recurring_status)s
\n
Thank you,\n
%(sitename)s""") % {
        'name': donation.display_donor(),
        'url_text': url_text,
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': displayGateway(donation),
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring and donation.subscription else '',
        'sitename': get_site_name()
    }


def get_donation_status_change_text(donation):
    donation_url = reverse_with_site_url('donations:my-renewals', kwargs={'id': donation.subscription.id}) if donation.is_recurring else reverse_with_site_url('donations:my-onetime-donations')
    if donation.user:
        url_text = str(_('Sign into our support page to view your updated donation(%(url)s).') % {'url': donation_url}) + "\n"
    else:
        url_text = ''
    return _("""
Dear %(name)s,\n
%(url_text)s
Details of your donation:\n
\n
Transaction ID: %(transaction_id)s\n
Donation frequency: %(frequency)s\n
Payment method: %(gateway)s\n
Donation amount: %(amount)s\n
Payment status: %(status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'name': donation.display_donor(),
        'url_text': url_text,
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': displayGateway(donation),
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'sitename': get_site_name()
    }


def get_subscription_status_change_text(subscription):
    return _("""
Dear %(name)s,\n
Sign into our support page to view your updated recurring donation(%(url)s).\n
Details of your recurring donation:\n
\n
Profile ID: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring Amount: %(amount)s\n
Status: %(status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'name': subscription.user.display_fullname(),
        'url': reverse_with_site_url('donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_new_renewal_text(donation):
    return _("""
Hi Admins,\n
This email is to inform you that a new renewal donation has been made on your website:\n
%(url)s\n
\n
Donor name: %(name)s\n
Donor email: %(email)s\n
Transaction ID: %(transaction_id)s\n
Donation frequency: %(frequency)s\n
Payment method: %(gateway)s\n
Donation amount: %(amount)s\n
Payment status: %(status)s\n
%(recurring_status)s
\n
Thank you,\n
%(sitename)s""") % {
        'url': reverse_with_site_url('donations_donation_modeladmin_inspect', kwargs={'instance_pk': donation.id}),
        'name': donation.user.display_fullname(),
        'email': donation.user.email,
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': donation.gateway,
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring else '',
        'sitename': get_site_name()
    }


def get_renewal_receipt_text(donation):
    return _("""
Dear %(name)s,\n
A big "thank you" for your kind %(amount)s recurring donation - it is very much appreciated and it will go a long way in supporting our operations.\n
Your contribution will be well-spent, allowing us to invest more in original reporting and safeguard press freedom. Please check out HKFP's latest Annual Report(https://hongkongfp.com/hong-kong-free-press-annual-report-2020/) - it includes our yearly, audited Transparency Report(https://hongkongfp.com/hong-kong-free-press-transparency-report-2019/), so you can see how carefully we spend our income.\n
Sign into our support page to view your renewal donations(%(renewals_url)s). You can also adjust, pause or cancel your recurring donation(%(donation_url)s). Please email donations@hongkongfp.com if you have any further enquiries.\n
From all of us, thank you for helping us keep independent media alive in Hong Kong!\n
Details of your renewal donation:\n
\n
Transaction ID: %(transaction_id)s\n
Donation frequency: %(frequency)s\n
Payment method: %(gateway)s\n
Donation amount: %(amount)s\n
Payment status: %(status)s\n
%(recurring_status)s
\n
Thank you,\n
%(sitename)s""") % {
        'name': donation.user.display_fullname(),
        'renewals_url': reverse_with_site_url('donations:my-renewals', kwargs={'id': donation.subscription.id}),
        'donation_url': reverse_with_site_url('donations:my-recurring-donations'),
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': displayGateway(donation),
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring else '',
        'sitename': get_site_name()
    }


def get_recurring_adjusted_admin_text(subscription):
    return _("""
Hi Admins,\n
A Recurring Donation's amount has been adjusted on your website:\n
%(url)s\n
\n
Donor name: %(name)s\n
Donor email: %(email)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'url': reverse_with_site_url('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.display_fullname(),
        'email': subscription.user.email,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_adjusted_donor_text(subscription):
    return _("""
Dear %(name)s,\n
Your monthly donation has been adjusted to %(amount)s per month. Thank you for your continued support.\n
Your contribution will be well-spent, allowing us to invest more in original reporting and safeguard press freedom. Please check out HKFP's latest Annual Report(https://hongkongfp.com/hong-kong-free-press-annual-report-2020/) - it includes our yearly, audited Transparency Report(https://hongkongfp.com/hong-kong-free-press-transparency-report-2019/), so you can see how carefully we spend our income.\n
Sign into our support page to adjust, pause or cancel your donation(%(url)s). Please email donations@hongkongfp.com if you have any further enquiries.\n
From all of us, thank you for helping us keep independent media alive in Hong Kong!\n
Details of your recurring donation:\n
\n
Donor name: %(name)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'name': subscription.user.display_fullname(),
        'url': reverse_with_site_url('donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_new_recurring_admin_text(subscription):
    return _("""
Hi Admins,\n
A new recurring donation has been activated on your website:\n
%(url)s\n
\n
Donor name: %(name)s\n
Donor email: %(email)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'url': reverse_with_site_url('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.display_fullname(),
        'email': subscription.user.email,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_new_recurring_donor_text(subscription):
    return _("""
Dear %(name)s,\n
A big "thank you" for your kind %(amount)s recurring donation - it is very much appreciated and it will go a long way in supporting our operations. Recurring donations, in particular, are vital to our sustainability.
As an HKFP Patron, your contribution will be well-spent, allowing us to invest more in original reporting and safeguard press freedom. Please check out HKFP's latest Annual Report(https://hongkongfp.com/hong-kong-free-press-annual-report-2020/) - it includes our yearly, audited Transparency Report(https://hongkongfp.com/hong-kong-free-press-transparency-report-2019/), so you can see how carefully we spend our income.\n
Sign into our support page (click "forgot password?" if you have trouble logging in) to adjust, pause or cancel your donation(%(url)s). Please email donations@hongkongfp.com if you have any further enquiries.\n
From all of us, thank you for helping us keep independent media alive in Hong Kong!\n
Details of your recurring donation:\n
\n
Donor name: %(name)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'name': subscription.user.display_fullname(),
        'url': reverse_with_site_url('donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_rescheduled_admin_text(subscription):
    return _("""
Hi Admins,\n
A Recurring Donation's billing date has been rescheduled to today:\n
%(url)s\n
\n
Donor name: %(name)s\n
Donor email: %(email)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'url': reverse_with_site_url('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.display_fullname(),
        'email': subscription.user.email,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_rescheduled_donor_text(subscription):
    return _("""
Dear %(name)s,\n
Your monthly donation's billing date has been rescheduled to today. Thank you for your continued support.\n
Your contribution will be well-spent, allowing us to invest more in original reporting and safeguard press freedom. Please check out HKFP's latest Annual Report(https://hongkongfp.com/hong-kong-free-press-annual-report-2020/) - it includes our yearly, audited Transparency Report(https://hongkongfp.com/hong-kong-free-press-transparency-report-2019/), so you can see how carefully we spend our income.\n
Sign into our support page to adjust, pause or cancel your donation(%(url)s). Please email donations@hongkongfp.com if you have any further enquiries.\n
From all of us, thank you for helping us keep independent media alive in Hong Kong!\n
Details of your recurring donation:\n
\n
Donor name: %(name)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'name': subscription.user.display_fullname(),
        'url': reverse_with_site_url('donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_paused_admin_text(subscription):
    return _("""
Hi Admins,\n
This email is to inform you that a recurring donation has been paused on your website:\n
%(url)s\n
\n
Donor name: %(name)s\n
Donor email: %(email)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'url': reverse_with_site_url('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.display_fullname(),
        'email': subscription.user.email,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_paused_donor_text(subscription):
    return _("""
Dear %(name)s,\n
Thanks very much for your recent support.\n
Your recurring donation to HKFP has been paused at your request - no further payments will be processed, unless you reactivate your contribution.\n
Sign into our support page if you wish to support us again in the future(%(url)s). Please email donations@hongkongfp.com if you have any further enquiries.\n
From all of us, thank you for backing our team and helping us keep independent media alive in Hong Kong!\n
Details of your recurring donation:\n
\n
Donor name: %(name)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'name': subscription.user.display_fullname(),
        'url': reverse_with_site_url('donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_resumed_admin_text(subscription):
    return _("""
Hi Admins,\n
This email is to inform you that a recurring donation has been resumed on your website:\n
%(url)s\n
\n
Donor name: %(name)s\n
Donor email: %(email)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'url': reverse_with_site_url('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.display_fullname(),
        'email': subscription.user.email,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_resumed_donor_text(subscription):
    return _("""
Dear %(name)s,\n
A big "thank you" for resuming your %(amount)s contribution - it is very much appreciated and it will go a long way in supporting our operations. Recurring donations, in particular, are vital to our sustainability.
As an HKFP Patron, your contribution will be well-spent, allowing us to invest more in original reporting and safeguard press freedom. Please check out HKFP's latest Annual Report(https://hongkongfp.com/hong-kong-free-press-annual-report-2020/) - it includes our yearly, audited Transparency Report(https://hongkongfp.com/hong-kong-free-press-transparency-report-2019/), so you can see how carefully we spend our income.\n
Sign into our support page to adjust, pause or cancel your donation(%(url)s). Please email donations@hongkongfp.com if you have any further enquiries.\n
From all of us, thank you for helping us keep independent media alive in Hong Kong!\n
Details of your recurring donation:\n
\n
Donor name: %(name)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'name': subscription.user.display_fullname(),
        'url': reverse_with_site_url('donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_cancelled_admin_text(subscription):
    return _("""
Hi Admins,\n
This email is to inform you that a recurring donation has been cancelled on your website:\n
%(url)s\n
\n
Donor name: %(name)s\n
Donor email: %(email)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'url': reverse_with_site_url('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.display_fullname(),
        'email': subscription.user.email,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_cancel_request_admin_text(subscription):
    return _("""
Hi Admins,\n
This email is to inform you that a cancellation to a recurring donation has been requested on your website. Please complete the request and manually change the subscription status to Cancelled at the link below:\n
%(url)s\n
\n
Donor name: %(name)s\n
Donor email: %(email)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'url': reverse_with_site_url('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.display_fullname(),
        'email': subscription.user.email,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_cancelled_donor_text(subscription):
    return _("""
Dear %(name)s,\n
Thanks very much for your recent support.\n
Your recurring donation to HKFP has been cancelled at your request - no further payments will be processed.\n
Sign into our support page(%(siteurl)s) if you wish to support us again in the future. Please email donations@hongkongfp.com if you have any further enquiries.\n
From all of us, thank you for backing our team and helping us keep independent media alive in Hong Kong!\n
Details of your recurring donation:\n
\n
Donor name: %(name)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'name': subscription.user.display_fullname(),
        'siteurl': get_site_url(),
        'url': reverse_with_site_url('donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_account_deleted_admin_text(user):
    return _("""
Hi Admins,\n
This email is to inform you that a donor account has been deleted on your website:\n
%(url)s\n
\n
Donor name: %(name)s\n
Donor email: %(email)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'url': get_site_url()+'/admin/users/',
        'name': user.display_fullname(),
        'email': user.email,
        'sitename': get_site_name()
    }


def get_account_deleted_donor_text(user):
    return _("""
Dear %(name)s,\n
Thanks very much for your recent support.\n
Your account at %(sitename)s has been deleted at your request.\n
From all of us, thank you for backing our team and helping us keep independent media alive in Hong Kong!\n
\n
Thank you,\n
%(sitename)s""") % {
        'name': user.display_fullname(),
        'sitename': get_site_name()
    }


def get_account_created_admin_text(user):
    return _("""
Hi Admins,\n
This email is to inform you that a donor account has been created on your website:\n
%(url)s\n
\n
Donor name: %(name)s\n
Donor email: %(email)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'url': get_site_url()+'/admin/users/%d/' % user.id,
        'name': user.display_fullname(),
        'email': user.email,
        'sitename': get_site_name()
    }


def get_donation_error_admin_text(donation, error_title, error_description):
    return _("""
Hi Admins,\n
This email is to inform you that a donation error has occurred on your website:\n
%(url)s\n
\n
Donation transaction ID: %(order)s\n
Donor name: %(name)s\n
Donor email: %(email)s\n
Error title: %(error_title)s\n
Error description: %(error_description)s\n
\n
Thank you,\n
%(sitename)s""") % {
        'url': reverse_with_site_url('donations_donation_modeladmin_inspect', kwargs={'instance_pk': donation.id}),
        'order': donation.transaction_id,
        'name': donation.display_donor_name(),
        'email': donation.display_donor_email(),
        'error_title': error_title,
        'error_description': error_description,
        'sitename': get_site_name()
    }
