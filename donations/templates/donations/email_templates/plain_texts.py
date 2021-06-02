from django.utils.translation import gettext as _

from newstream.functions import get_site_name, get_site_url, reverse_with_site_url
from donations.functions import displayDonationAmountWithCurrency, displayRecurringAmountWithCurrency, displayGateway


def get_new_donation_text(donation):
    return _("""
        New Donation\n
        \n
        Hi Admins,\n
        This email is to inform you that a new donation has been made on your website:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Transaction ID: %(transaction_id)s\n
        Donation frequency: %(frequency)s\n
        Payment method: %(gateway)s\n
        Donation amount: %(amount)s\n
        Payment status: %(status)s\n
        %(recurring_status)s
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': reverse_with_site_url('donations_donation_modeladmin_inspect', kwargs={'instance_pk': donation.id}),
        'name': donation.donor_name(),
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
        url_text = str(_('Go to %(url)s to view your donation on the website.') % {'url': donation_url})
    else:
        url_text = ''
    return _("""
        Donation Receipt\n
        \n
        Dear %(name)s,\n
        Thank you for your generosity! Your support means a lot to us. %(url_text)s\n
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
        %(sitename)s
    """) % {
        'name': donation.donor_name(),
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
        url_text = str(_('Go to %(url)s to see more.') % {'url': donation_url})
    else:
        url_text = ''
    return _("""
        Your Donation Payment Status has been updated\n
        \n
        Dear %(name)s,\n
        Listed below are the updated details of your donation. %(url_text)s:\n
        \n
        Transaction ID: %(transaction_id)s\n
        Donation frequency: %(frequency)s\n
        Payment method: %(gateway)s\n
        Donation amount: %(amount)s\n
        Payment status: %(status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': donation.donor_name(),
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
        Your Recurring Donation Status has been updated\n
        \n
        Dear %(name)s,\n
        Listed below are the updated details of your recurring donation. Go to %(url)s to see more.\n
        \n
        Profile ID: %(profile_id)s\n
        Payment method: %(gateway)s\n
        Recurring Amount: %(amount)s\n
        Status: %(status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': subscription.user.fullname,
        'url': reverse_with_site_url('donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_new_renewal_text(donation):
    return _("""
        New Renewal Donation\n
        \n
        Hi Admins,\n
        This email is to inform you that a new renewal donation has been made on your website:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Transaction ID: %(transaction_id)s\n
        Donation frequency: %(frequency)s\n
        Payment method: %(gateway)s\n
        Donation amount: %(amount)s\n
        Payment status: %(status)s\n
        %(recurring_status)s
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': reverse_with_site_url('donations_donation_modeladmin_inspect', kwargs={'instance_pk': donation.id}),
        'name': donation.user.fullname,
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
        Renewal Donation Receipt\n
        \n
        Dear %(name)s,\n
        Thank you for your generosity! Your support means a lot to us. Go to %(url)s to view your renewal donation on the website.\n
        Here are the details of your renewal donation:\n
        \n
        Transaction ID: %(transaction_id)s\n
        Donation frequency: %(frequency)s\n
        Payment method: %(gateway)s\n
        Donation amount: %(amount)s\n
        Payment status: %(status)s\n
        %(recurring_status)s
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': donation.user.fullname,
        'url': reverse_with_site_url('donations:my-renewals', kwargs={'id': donation.subscription.id}),
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': displayGateway(donation),
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring else '',
        'sitename': get_site_name()
    }


def get_recurring_updated_admin_text(subscription, message):
    return _("""
        A Recurring Donation is updated\n
        \n
        Hi Admins,\n
        %(message)s\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Recurring donation identifier: %(profile_id)s\n
        Payment method: %(gateway)s\n
        Recurring donation amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'message': message,
        'url': reverse_with_site_url('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.fullname,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_updated_donor_text(subscription, message):
    return _("""
        Your Recurring Donation is updated\n
        \n
        Dear %(name)s,\n
        %(message)s Go to %(url)s to view your recurring donations on the website.\n
        Here are the details of your recurring donation:\n
        \n
        Donor: %(name)s\n
        Recurring donation identifier: %(profile_id)s\n
        Payment method: %(gateway)s\n
        Recurring donation amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': subscription.user.fullname,
        'message': message,
        'url': reverse_with_site_url('donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_paused_admin_text(subscription):
    return _("""
        A Recurring Donation is paused\n
        \n
        Hi Admins,\n
        This email is to inform you that a recurring donation has been paused on your website:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Recurring donation identifier: %(profile_id)s\n
        Payment method: %(gateway)s\n
        Recurring donation amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': reverse_with_site_url('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.fullname,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_paused_donor_text(subscription):
    return _("""
        Your Recurring Donation is paused\n
        \n
        Dear %(name)s,\n
        You have just paused your recurring donation. You can resume it anytime in your account. Go to %(url)s to view your recurring donations on the website.\n
        Here are the details of your recurring donation:\n
        \n
        Donor: %(name)s\n
        Recurring donation identifier: %(profile_id)s\n
        Payment method: %(gateway)s\n
        Recurring donation amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': subscription.user.fullname,
        'url': reverse_with_site_url('donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_resumed_admin_text(subscription):
    return _("""
        A Recurring Donation is resumed\n
        \n
        Hi Admins,\n
        This email is to inform you that a recurring donation has been resumed on your website:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Recurring donation identifier: %(profile_id)s\n
        Payment method: %(gateway)s\n
        Recurring donation amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': reverse_with_site_url('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.fullname,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_resumed_donor_text(subscription):
    return _("""
        Your Recurring Donation is resumed\n
        \n
        Dear %(name)s,\n
        You have just resumed your recurring donation. Go to %(url)s to view your recurring donations on the website.\n
        Here are the details of your recurring donation:\n
        \n
        Donor: %(name)s\n
        Recurring donation identifier: %(profile_id)s\n
        Payment method: %(gateway)s\n
        Recurring donation amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': subscription.user.fullname,
        'url': reverse_with_site_url('donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_cancelled_admin_text(subscription):
    return _("""
        A Recurring Donation is cancelled\n
        \n
        Hi Admins,\n
        This email is to inform you that a recurring donation has been cancelled on your website:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Recurring donation identifier: %(profile_id)s\n
        Payment method: %(gateway)s\n
        Recurring donation amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': reverse_with_site_url('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.fullname,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_cancel_request_admin_text(subscription):
    return _("""
        Cancellation to a Recurring Donation is requested\n
        \n
        Hi Admins,\n
        This email is to inform you that a cancellation to a recurring donation has been requested on your website. Please complete the request and manually change the subscription status to Cancelled at the link below:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Recurring donation identifier: %(profile_id)s\n
        Payment method: %(gateway)s\n
        Recurring donation amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': reverse_with_site_url('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.fullname,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_recurring_cancelled_donor_text(subscription):
    return _("""
        Your Recurring Donation is cancelled\n
        \n
        Dear %(name)s,\n
        You have just cancelled your recurring donation. Go to %(url)s to view your recurring donations on the website.\n
        Here are the details of your recurring donation:\n
        \n
        Donor: %(name)s\n
        Recurring donation identifier: %(profile_id)s\n
        Payment method: %(gateway)s\n
        Recurring donation amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': subscription.user.fullname,
        'url': reverse_with_site_url('donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': get_site_name()
    }


def get_account_deleted_admin_text(user):
    return _("""
        A Donor Account is deleted\n
        \n
        Hi Admins,\n
        This email is to inform you that a donor account has been deleted on your website:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': get_site_url()+'/admin/users/',
        'name': user.fullname,
        'sitename': get_site_name()
    }


def get_account_deleted_donor_text(user):
    return _("""
        Your Account is deleted\n
        \n
        Dear %(name)s,\n
        You have just deleted your account. Thank you for your support all the way!\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': user.fullname,
        'sitename': get_site_name()
    }


def get_account_created_admin_text(user):
    return _("""
        A Donor Account is created\n
        \n
        Hi Admins,\n
        This email is to inform you that a donor account has been created on your website:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': get_site_url()+'/admin/users/%d/' % user.id,
        'name': user.fullname,
        'sitename': get_site_name()
    }


def get_donation_error_admin_text(donation, error_title, error_description):
    return _("""
        A Donation Error has occurred.\n
        \n
        Hi Admins,\n
        This email is to inform you that a donation error has occurred on your website:\n
        %(url)s\n
        \n
        Donation transaction ID: %(order)s\n
        Donor: %(name)s\n
        Error title: %(error_title)s\n
        Error description: %(error_description)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': reverse_with_site_url('donations_donation_modeladmin_inspect', kwargs={'instance_pk': donation.id}),
        'order': donation.transaction_id,
        'name': donation.donor_name(),
        'error_title': error_title,
        'error_description': error_description,
        'sitename': get_site_name()
    }
