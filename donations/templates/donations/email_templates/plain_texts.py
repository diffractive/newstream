from django.utils.translation import gettext as _

from newstream.functions import getSiteName, getFullReverseUrl
from donations.functions import displayDonationAmountWithCurrency, displayRecurringAmountWithCurrency


def get_new_donation_text(request, donation):
    return _("""
        New Donation\n
        \n
        Hi Admins,\n
        This email is to inform you that a new donation has been made on your website:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Order Number: %(order_number)s\n
        Donation Frequency: %(frequency)s\n
        Currency: %(currency)s\n
        Donation Amount: %(amount)s\n
        Payment Status: %(status)s\n
        %(recurring_status)s
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': request.build_absolute_uri('/')[:-1],
        'name': donation.user.fullname,
        'order_number': donation.order_number,
        'frequency': donation.donation_frequency,
        'currency': donation.currency,
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring and donation.subscription else '',
        'sitename': getSiteName(request)
    }


def get_donation_receipt_text(request, donation):
    return _("""
        Donation Receipt\n
        \n
        Dear %(name)s,\n
        Thank you for your generosity! Your support means a lot to us. Go to %(url)s to view your donation on the website.\n
        Here are the details of your donation:\n
        \n
        Order Number: %(order_number)s\n
        Donation Frequency: %(frequency)s\n
        Currency: %(currency)s\n
        Donation Amount: %(amount)s\n
        Payment Status: %(status)s\n
        %(recurring_status)s
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': donation.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-recurring-donations') if donation.is_recurring else getFullReverseUrl(request, 'donations:my-onetime-donations'),
        'order_number': donation.order_number,
        'frequency': donation.donation_frequency,
        'currency': donation.currency,
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring and donation.subscription else '',
        'sitename': getSiteName(request)
    }


def get_new_renewal_text(request, donation):
    return _("""
        New Renewal Donation\n
        \n
        Hi Admins,\n
        This email is to inform you that a new renewal donation has been made on your website:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Order Number: %(order_number)s\n
        Donation Frequency: %(frequency)s\n
        Currency: %(currency)s\n
        Donation Amount: %(amount)s\n
        Payment Status: %(status)s\n
        %(recurring_status)s
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': request.build_absolute_uri('/')[:-1],
        'name': donation.user.fullname,
        'order_number': donation.order_number,
        'frequency': donation.donation_frequency,
        'currency': donation.currency,
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring else '',
        'sitename': getSiteName(request)
    }


def get_renewal_receipt_text(request, donation):
    return _("""
        Renewal Donation Receipt\n
        \n
        Dear %(name)s,\n
        Thank you for your generosity! Your support means a lot to us. Go to %(url)s to view your renewal donation on the website.\n
        Here are the details of your renewal donation:\n
        \n
        Order Number: %(order_number)s\n
        Donation Frequency: %(frequency)s\n
        Currency: %(currency)s\n
        Donation Amount: %(amount)s\n
        Payment Status: %(status)s\n
        %(recurring_status)s
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': donation.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-renewals', kwargs={'id': donation.subscription.id}),
        'order_number': donation.order_number,
        'frequency': donation.donation_frequency,
        'currency': donation.currency,
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring else '',
        'sitename': getSiteName(request)
    }


def get_recurring_updated_admin_text(request, subscription, message):
    return _("""
        A Recurring Donation is updated\n
        \n
        Hi Admins,\n
        %(message)s\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Recurring Donation Identifier: %(object_id)s\n
        Currency: %(currency)s\n
        Recurring Donation Amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'message': message,
        'url': request.build_absolute_uri('/')[:-1],
        'name': subscription.user.fullname,
        'object_id': subscription.object_id,
        'currency': subscription.currency,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def get_recurring_updated_donor_text(request, subscription, message):
    return _("""
        Your Recurring Donation is updated\n
        \n
        Dear %(name)s,\n
        %(message)s Go to %(url)s to view your recurring donations on the website.\n
        Here are the details of your recurring donation:\n
        \n
        Donor: %(name)s\n
        Recurring Donation Identifier: %(object_id)s\n
        Currency: %(currency)s\n
        Recurring Donation Amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': subscription.user.fullname,
        'message': message,
        'url': getFullReverseUrl(request, 'donations:my-recurring-donations'),
        'object_id': subscription.object_id,
        'currency': subscription.currency,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def get_recurring_paused_admin_text(request, subscription):
    return _("""
        A Recurring Donation is paused\n
        \n
        Hi Admins,\n
        This email is to inform you that a recurring donation has been paused on your website:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Recurring Donation Identifier: %(object_id)s\n
        Currency: %(currency)s\n
        Recurring Donation Amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': request.build_absolute_uri('/')[:-1],
        'name': subscription.user.fullname,
        'object_id': subscription.object_id,
        'currency': subscription.currency,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def get_recurring_paused_donor_text(request, subscription):
    return _("""
        Your Recurring Donation is paused\n
        \n
        Dear %(name)s,\n
        You have just paused your recurring donation. You can resume it anytime in your account. Go to %(url)s to view your recurring donations on the website.\n
        Here are the details of your recurring donation:\n
        \n
        Donor: %(name)s\n
        Recurring Donation Identifier: %(object_id)s\n
        Currency: %(currency)s\n
        Recurring Donation Amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': subscription.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-recurring-donations'),
        'object_id': subscription.object_id,
        'currency': subscription.currency,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def get_recurring_resumed_admin_text(request, subscription):
    return _("""
        A Recurring Donation is resumed\n
        \n
        Hi Admins,\n
        This email is to inform you that a recurring donation has been resumed on your website:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Recurring Donation Identifier: %(object_id)s\n
        Currency: %(currency)s\n
        Recurring Donation Amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': request.build_absolute_uri('/')[:-1],
        'name': subscription.user.fullname,
        'object_id': subscription.object_id,
        'currency': subscription.currency,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def get_recurring_resumed_donor_text(request, subscription):
    return _("""
        Your Recurring Donation is resumed\n
        \n
        Dear %(name)s,\n
        You have just resumed your recurring donation. Go to %(url)s to view your recurring donations on the website.\n
        Here are the details of your recurring donation:\n
        \n
        Donor: %(name)s\n
        Recurring Donation Identifier: %(object_id)s\n
        Currency: %(currency)s\n
        Recurring Donation Amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': subscription.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-recurring-donations'),
        'object_id': subscription.object_id,
        'currency': subscription.currency,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def get_recurring_cancelled_admin_text(request, subscription):
    return _("""
        A Recurring Donation is cancelled\n
        \n
        Hi Admins,\n
        This email is to inform you that a recurring donation has been cancelled on your website:\n
        %(url)s\n
        \n
        Donor: %(name)s\n
        Recurring Donation Identifier: %(object_id)s\n
        Currency: %(currency)s\n
        Recurring Donation Amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': request.build_absolute_uri('/')[:-1],
        'name': subscription.user.fullname,
        'object_id': subscription.object_id,
        'currency': subscription.currency,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def get_recurring_cancelled_donor_text(request, subscription):
    return _("""
        Your Recurring Donation is cancelled\n
        \n
        Dear %(name)s,\n
        You have just cancelled your recurring donation. Go to %(url)s to view your recurring donations on the website.\n
        Here are the details of your recurring donation:\n
        \n
        Donor: %(name)s\n
        Recurring Donation Identifier: %(object_id)s\n
        Currency: %(currency)s\n
        Recurring Donation Amount: %(amount)s\n
        Recurring Status: %(recurring_status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': subscription.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-recurring-donations'),
        'object_id': subscription.object_id,
        'currency': subscription.currency,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def get_account_deleted_admin_text(request, user):
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
        'url': request.build_absolute_uri('/')[:-1],
        'name': user.fullname,
        'sitename': getSiteName(request)
    }


def get_account_deleted_donor_text(request, user):
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
        'sitename': getSiteName(request)
    }


def get_account_created_admin_text(request, user):
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
        'url': request.build_absolute_uri('/')[:-1],
        'name': user.fullname,
        'sitename': getSiteName(request)
    }

def get_donation_error_admin_text(request, donation, error_title, error_description):
    return _("""
        A Donation Error has occurred.\n
        \n
        Hi Admins,\n
        This email is to inform you that a donation error has occurred on your website:\n
        %(url)s\n
        \n
        Donation order number: %(order)s\n
        Donor: %(name)s\n
        Error Title: %(error_title)s\n
        Error Description: %(error_description)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': request.build_absolute_uri('/')[:-1],
        'order': donation.order_number,
        'name': donation.user.fullname,
        'error_title': error_title,
        'error_description': error_description,
        'sitename': getSiteName(request)
    }
