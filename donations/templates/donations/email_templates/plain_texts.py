def get_new_donation_text(request, donation):
    return """
        New Donation\n
        \n
        Hi Admins,\n
        This email is to inform you that a new donation has been made on your website:\n
        %s\n
        \n
        Donor: %s\n
        Order Number: %s\n
        Is Monthly Donation? %s\n
        Currency: %s\n
        Donation Amount: %s\n
        Creates Account? %s\n
        Opt in Mailing List? %s\n
        Payment Status: %s\n
        \n
        Thank you,\n
        %s
    """ % (request.build_absolute_uri('/')[:-1],
           donation.donor.fullname,
           donation.order_number,
           donation.isRecurring(),
           donation.currency,
           donation.donation_amount,
           donation.isCreateAccount(),
           donation.donor.optInMailing(),
           donation.payment_status,
           request.site.site_name
           )


def get_donation_receipt_text(request, donation):
    return """
        Donation Receipt\n
        \n
        Dear %s,\n
        Thank you for your generosity! Your support means a lot to us. Here are the details of your donation:\n
        \n
        Order Number: %s\n
        Is Monthly Donation? %s\n
        Currency: %s\n
        Donation Amount: %s\n
        Creates Account? %s\n
        Opt in Mailing List? %s\n
        Payment Status: %s\n
        \n
        Thank you,\n
        %s
    """ % (donation.donor.fullname,
           donation.order_number,
           donation.isRecurring(),
           donation.currency,
           donation.donation_amount,
           donation.isCreateAccount(),
           donation.donor.optInMailing(),
           donation.payment_status,
           request.site.site_name
           )
