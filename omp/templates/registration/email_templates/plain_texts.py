def get_verify_your_email_text(request, fullname, verify_link):
    return """
        Verify Your Email Now\n
        \n
        Dear %s,\n
        Your account has been created. Please verify your email by visiting %s in order to fully manage your donations and account. \n
        Thank you,\n
        %s
    """ % (fullname,
           verify_link,
           request.site.site_name
           )
