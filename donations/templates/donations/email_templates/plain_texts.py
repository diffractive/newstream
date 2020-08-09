from django.utils.translation import gettext as _

from newstream.functions import getSiteName


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
        Opt in Mailing List? %(opt_in)s\n
        Payment Status: %(status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'url': request.build_absolute_uri('/')[:-1],
        'name': donation.user.fullname,
        'order_number': donation.order_number,
        'frequency': donation.donation_frequency,
        'currency': donation.currency,
        'amount': donation.donation_amount,
        'opt_in': donation.user.optInMailing(),
        'status': donation.payment_status,
        'sitename': getSiteName(request)
    }


def get_donation_receipt_text(request, donation):
    return _("""
        Donation Receipt\n
        \n
        Dear %(name)s,\n
        Thank you for your generosity! Your support means a lot to us. Here are the details of your donation:\n
        \n
        Order Number: %(order_number)s\n
        Donation Frequency: %(frequency)s\n
        Currency: %(currency)s\n
        Donation Amount: %(amount)s\n
        Opt in Mailing List? %(opt_in)s\n
        Payment Status: %(status)s\n
        \n
        Thank you,\n
        %(sitename)s
    """) % {
        'name': donation.user.fullname,
        'order_number': donation.order_number,
        'frequency': donation.donation_frequency,
        'currency': donation.currency,
        'amount': donation.donation_amount,
        'opt_in': donation.user.optInMailing(),
        'status': donation.payment_status,
        'sitename': getSiteName(request)
    }
