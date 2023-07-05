import traceback

from django.conf import settings
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from allauth.account.views import PasswordResetView

from wagtail.models import Site

User = get_user_model()

class Command(BaseCommand):
    help = 'Batch send password reset emails to users.'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--donorids',
            action='append',
            nargs='+',
            type=int,
            help='Provide specific donor ids for this operation instead of all data',
        )

        parser.add_argument(
            '--site_host',
            action='store', 
            default='support.hongkongfp.com',
            help='Hostname for the wagtail site'
        )

    def print(self, msg):
        self.stdout.write(msg)

    def handle(self, *args, **options):
        try:
            if options['donorids']:
                # operate on specific users, beware it is a list of lists
                donorids_list = [item for sublist in options['donorids'] for item in sublist]
                donors = User.objects.filter(pk__in=donorids_list)
            else:
                # operate on all users
                donors = User.objects.all()

            # Create a post request to pass to the view
            request = HttpRequest()
            request.method = 'POST'

            # add the absolute url to be be included in email
            if options['site_host']:
                request.META['HTTP_HOST'] = options['site_host']
            else:
                newstreamSite = Site.objects.filter(is_default_site=True).get()
                request.META['HTTP_HOST'] = newstreamSite.hostname

            # loop donors to send email to each one
            for donor in donors:
                # pass the post form data
                request.POST = {
                    'email': donor.email,
                    'csrfmiddlewaretoken': get_token(HttpRequest())
                }
                PasswordResetView.as_view()(request)  # email will be sent!
                self.print("[√] PasswordReset Email sent to %s(%d)" % (donor.display_fullname(), donor.id))
        except Exception as e:
            self.print(str(e))
            traceback.print_exc()

        