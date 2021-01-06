from django.utils import translation
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.defaultfilters import pluralize
from django.utils.translation import gettext_lazy as _

from wagtailstreamforms.hooks import register

from newstream.functions import getSiteSettings_from_default_site

@register('process_form_submission')
def email_submission_to_admins(instance, form):
    """ Send an email with the submission to admins. """
    # set default language for admins' emails
    translation.activate(settings.LANGUAGE_CODE)

    siteSettings = getSiteSettings_from_default_site()

    admin_list = [admin_email.email for admin_email in siteSettings.admin_emails.all()]

    txt_content = ['Please see below submission\n', ]
    html_content = ['<table cellpadding="10" cellspacing="0" style="width: 100%;"> <tr> <th style="width: 100%;text-align: left;"> <h2 style="font-weight: bold;">', str(_('Please see below submission:')), '</h2> </th> </tr><tr> <td style="width: 100%;"> <table cellpadding="10">']
    from_address = settings.DEFAULT_FROM_EMAIL
    subject = 'New Form Submission : %s' % instance.title

    # build up the email content
    for field, value in form.cleaned_data.items():
        if field in form.files:
            count = len(form.files.getlist(field))
            value = '{} file{}'.format(count, pluralize(count))
        elif isinstance(value, list):
            value = ', '.join(value)
        txt_content.append('{}: {}'.format(field, value))
        html_content.append('<tr> <td style="font-weight: bold;">')
        html_content.append(field)
        html_content.append('</td> <td>')
        html_content.append(value)
        html_content.append('</td> </tr>')
    txt_content = '\n'.join(txt_content)
    html_content = ''.join(html_content)
    html_content += '</table></td></tr></table>'

    # create the email message
    email = EmailMultiAlternatives(
        subject=subject,
        body=txt_content,
        from_email=from_address,
        to=admin_list
    )
    email.attach_alternative(html_content, "text/html")

    # attach any files submitted
    for field in form.files:
        for file in form.files.getlist(field):
            file.seek(0)
            email.attach(file.name, file.read(), file.content_type)

    # finally send the email
    email.send(fail_silently=False)