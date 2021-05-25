from django.utils.translation import gettext as _

from newstream.functions import getSiteName, getFullReverseUrl
from donations.functions import displayDonationAmountWithCurrency, displayRecurringAmountWithCurrency, displayGateway


def default_new_donation_text():
    return """New Donation\n
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
%(sitename)s"""


def get_new_donation_text(request, donation, text=None):
    if text is None:
        text = default_new_donation_text()
    return _(text) % {
        'url': getFullReverseUrl(request, 'donations_donation_modeladmin_inspect', kwargs={'instance_pk': donation.id}),
        'name': donation.donor_name(),
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': donation.gateway,
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring and donation.subscription else '',
        'sitename': getSiteName(request)
    }


def default_donation_receipt_text():
    return """Donation Receipt\n
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
%(sitename)s"""


def get_donation_receipt_text(request, donation, text=None):
    if text is None:
        text = default_donation_receipt_text()
    donation_url = getFullReverseUrl(request, 'donations:my-recurring-donations') if donation.is_recurring else getFullReverseUrl(request, 'donations:my-onetime-donations')
    if donation.user:
        url_text = str(_('Go to %(url)s to view your donation on the website.') % {'url': donation_url})
    else:
        url_text = ''
    return _(text) % {
        'name': donation.donor_name(),
        'url_text': url_text,
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': displayGateway(donation),
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring and donation.subscription else '',
        'sitename': getSiteName(request)
    }


def default_donation_revoked_admin_text():
    return """A Donation is revoked\n
\n
Hi Admins,\n
This email is to inform you that a donation has been revoked on your website:\n
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
%(sitename)s"""


def get_donation_revoked_admin_text(request, donation, text=None):
    if text is None:
        text = default_donation_revoked_admin_text()
    return _(text) % {
        'url': getFullReverseUrl(request, 'donations_donation_modeladmin_inspect', kwargs={'instance_pk': donation.id}),
        'name': donation.donor_name(),
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': donation.gateway,
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring and donation.subscription else '',
        'sitename': getSiteName(request)
    }


def default_donation_revoked_donor_text():
    return """Donation Revoked\n
\n
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
%(sitename)s"""


def get_donation_revoked_donor_text(request, donation, text=None):
    if text is None:
        text = default_donation_revoked_donor_text()
    donation_url = getFullReverseUrl(request, 'donations:my-recurring-donations') if donation.is_recurring else getFullReverseUrl(request, 'donations:my-onetime-donations')
    if donation.user:
        url_text = str(_('Go to %(url)s to view your donation on the website.') % {'url': donation_url})
    else:
        url_text = ''
    return _(text) % {
        'name': donation.donor_name(),
        'url_text': url_text,
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': displayGateway(donation),
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring and donation.subscription else '',
        'sitename': getSiteName(request)
    }


def default_donation_status_change_text():
    return """Your Donation Payment Status has been updated\n
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
%(sitename)s"""


def get_donation_status_change_text(request, donation, text=None):
    if text is None:
        text = default_donation_status_change_text()
    donation_url = getFullReverseUrl(request, 'donations:my-renewals', kwargs={'id': donation.subscription.id}) if donation.is_recurring else getFullReverseUrl(request, 'donations:my-onetime-donations')
    if donation.user:
        url_text = str(_('Go to %(url)s to see more.') % {'url': donation_url})
    else:
        url_text = ''
    return _(text) % {
        'name': donation.donor_name(),
        'url_text': url_text,
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': displayGateway(donation),
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'sitename': getSiteName(request)
    }


def default_subscription_status_change_text():
    return """Your Recurring Donation Status has been updated\n
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
%(sitename)s"""


def get_subscription_status_change_text(request, subscription, text=None):
    if text is None:
        text = default_subscription_status_change_text()
    return _(text) % {
        'name': subscription.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_new_renewal_text():
    return """New Renewal Donation\n
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
%(sitename)s"""


def get_new_renewal_text(request, donation, text=None):
    if text is None:
        text = default_new_renewal_text()
    return _(text) % {
        'url': getFullReverseUrl(request, 'donations_donation_modeladmin_inspect', kwargs={'instance_pk': donation.id}),
        'name': donation.user.fullname,
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': donation.gateway,
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring else '',
        'sitename': getSiteName(request)
    }


def default_renewal_receipt_text():
    return """Renewal Donation Receipt\n
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
%(sitename)s"""


def get_renewal_receipt_text(request, donation, text=None):
    if text is None:
        text = default_renewal_receipt_text()
    return _(text) % {
        'name': donation.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-renewals', kwargs={'id': donation.subscription.id}),
        'transaction_id': donation.transaction_id,
        'frequency': donation.donation_frequency,
        'gateway': displayGateway(donation),
        'amount': displayDonationAmountWithCurrency(donation),
        'status': donation.payment_status,
        'recurring_status': 'Recurring Status: '+donation.subscription.recurring_status + "\n" if donation.is_recurring else '',
        'sitename': getSiteName(request)
    }


def default_recurring_adjusted_admin_text():
    return """A Recurring Donation Amount is Adjusted\n
\n
Hi Admins,\n
A Recurring Donation's amount has been adjusted on your website:\n
%(url)s\n
\n
Donor: %(name)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s"""


def get_recurring_adjusted_admin_text(request, subscription, text=None):
    if text is None:
        text = default_recurring_adjusted_admin_text()
    return _(text) % {
        'url': getFullReverseUrl(request, 'donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.fullname,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_recurring_adjusted_donor_text():
    return """Your Recurring Donation Amount is Adjusted\n
\n
Dear %(name)s,\n
You have just adjusted your recurring donation amount. Go to %(url)s to view your recurring donations on the website.\n
Here are the details of your recurring donation:\n
\n
Donor: %(name)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s"""


def get_recurring_adjusted_donor_text(request, subscription, text=None):
    if text is None:
        text = default_recurring_adjusted_donor_text()
    return _(text) % {
        'name': subscription.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_new_recurring_admin_text():
    return """New Recurring Donation\n
\n
Hi Admins,\n
A new recurring donation has been activated on your website:\n
%(url)s\n
\n
Donor: %(name)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s"""


def get_new_recurring_admin_text(request, subscription, text=None):
    if text is None:
        text = default_new_recurring_admin_text()
    return _(text) % {
        'url': getFullReverseUrl(request, 'donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.fullname,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_new_recurring_donor_text():
    return """Your New Recurring Donation is Activated\n
\n
Dear %(name)s,\n
Your new recurring donation has just been activated. Go to %(url)s to view your recurring donations on the website.\n
Here are the details of your recurring donation:\n
\n
Donor: %(name)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s"""


def get_new_recurring_donor_text(request, subscription, text=None):
    if text is None:
        text = default_new_recurring_donor_text()
    return _(text) % {
        'name': subscription.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_recurring_rescheduled_admin_text():
    return """A Recurring Donation is Rescheduled\n
\n
Hi Admins,\n
A Recurring Donation's billing date has been rescheduled to today:\n
%(url)s\n
\n
Donor: %(name)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s"""


def get_recurring_rescheduled_admin_text(request, subscription, text=None):
    if text is None:
        text = default_recurring_rescheduled_admin_text()
    return _(text) % {
        'url': getFullReverseUrl(request, 'donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.fullname,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_recurring_rescheduled_donor_text():
    return """Your Recurring Donation is Rescheduled\n
\n
Dear %(name)s,\n
You have just rescheduled your recurring donation's billing date to today. Go to %(url)s to view your recurring donations on the website.\n
Here are the details of your recurring donation:\n
\n
Donor: %(name)s\n
Recurring donation identifier: %(profile_id)s\n
Payment method: %(gateway)s\n
Recurring donation amount: %(amount)s\n
Recurring Status: %(recurring_status)s\n
\n
Thank you,\n
%(sitename)s"""


def get_recurring_rescheduled_donor_text(request, subscription, text=None):
    if text is None:
        text = default_recurring_rescheduled_donor_text()
    return _(text) % {
        'name': subscription.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_recurring_paused_admin_text():
    return """A Recurring Donation is paused\n
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
%(sitename)s"""


def get_recurring_paused_admin_text(request, subscription, text=None):
    if text is None:
        text = default_recurring_paused_admin_text()
    return _(text) % {
        'url': getFullReverseUrl(request, 'donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.fullname,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_recurring_paused_donor_text():
    return """Your Recurring Donation is paused\n
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
%(sitename)s"""


def get_recurring_paused_donor_text(request, subscription, text=None):
    if text is None:
        text = default_recurring_paused_donor_text()
    return _(text) % {
        'name': subscription.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_recurring_resumed_admin_text():
    return """A Recurring Donation is resumed\n
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
%(sitename)s"""


def get_recurring_resumed_admin_text(request, subscription, text=None):
    if text is None:
        text = default_recurring_resumed_admin_text()
    return _(text) % {
        'url': getFullReverseUrl(request, 'donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.fullname,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_recurring_resumed_donor_text():
    return """Your Recurring Donation is resumed\n
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
%(sitename)s"""


def get_recurring_resumed_donor_text(request, subscription, text=None):
    if text is None:
        text = default_recurring_resumed_donor_text()
    return _(text) % {
        'name': subscription.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_recurring_cancelled_admin_text():
    return """A Recurring Donation is cancelled\n
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
%(sitename)s"""


def get_recurring_cancelled_admin_text(request, subscription, text=None):
    if text is None:
        text = default_recurring_cancelled_admin_text()
    return _(text) % {
        'url': getFullReverseUrl(request, 'donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.fullname,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_recurring_cancel_request_admin_text():
    return """Cancellation to a Recurring Donation is requested\n
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
%(sitename)s"""


def get_recurring_cancel_request_admin_text(request, subscription, text=None):
    if text is None:
        text = default_recurring_cancel_request_admin_text()
    return _(text) % {
        'url': getFullReverseUrl(request, 'donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription.id}),
        'name': subscription.user.fullname,
        'profile_id': subscription.profile_id,
        'gateway': subscription.gateway,
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_recurring_cancelled_donor_text():
    return """Your Recurring Donation is cancelled\n
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
%(sitename)s"""


def get_recurring_cancelled_donor_text(request, subscription, text=None):
    if text is None:
        text = default_recurring_cancelled_donor_text()
    return _(text) % {
        'name': subscription.user.fullname,
        'url': getFullReverseUrl(request, 'donations:my-recurring-donations'),
        'profile_id': subscription.profile_id,
        'gateway': displayGateway(subscription),
        'amount': displayRecurringAmountWithCurrency(subscription),
        'recurring_status': subscription.recurring_status,
        'sitename': getSiteName(request)
    }


def default_account_deleted_admin_text():
    return """A Donor Account is deleted\n
\n
Hi Admins,\n
This email is to inform you that a donor account has been deleted on your website:\n
%(url)s\n
\n
Donor: %(name)s\n
\n
Thank you,\n
%(sitename)s"""


def get_account_deleted_admin_text(request, user, text=None):
    if text is None:
        text = default_account_deleted_admin_text()
    return _(text) % {
        'url': request.build_absolute_uri('/')+'admin/users/',
        'name': user.fullname,
        'sitename': getSiteName(request)
    }


def default_account_deleted_donor_text():
    return """Your Account is deleted\n
\n
Dear %(name)s,\n
You have just deleted your account. Thank you for your support all the way!\n
\n
Thank you,\n
%(sitename)s"""


def get_account_deleted_donor_text(request, user, text=None):
    if text is None:
        text = default_account_deleted_donor_text()
    return _(text) % {
        'name': user.fullname,
        'sitename': getSiteName(request)
    }


def default_account_created_admin_text():
    return """A Donor Account is created\n
\n
Hi Admins,\n
This email is to inform you that a donor account has been created on your website:\n
%(url)s\n
\n
Donor: %(name)s\n
\n
Thank you,\n
%(sitename)s"""


def get_account_created_admin_text(request, user, text=None):
    if text is None:
        text = default_account_created_admin_text()
    return _(text) % {
        'url': request.build_absolute_uri('/')+'admin/users/%d/' % user.id,
        'name': user.fullname,
        'sitename': getSiteName(request)
    }


def default_donation_error_admin_text():
    return """A Donation Error has occurred.\n
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
%(sitename)s"""


def get_donation_error_admin_text(request, donation, error_title, error_description, text=None):
    if text is None:
        text = default_donation_error_admin_text()
    return _(text) % {
        'url': getFullReverseUrl(request, 'donations_donation_modeladmin_inspect', kwargs={'instance_pk': donation.id}),
        'order': donation.transaction_id,
        'name': donation.donor_name(),
        'error_title': error_title,
        'error_description': error_description,
        'sitename': getSiteName(request)
    }
