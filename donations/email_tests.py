from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from requests.api import get
from wagtail.core.models import Site

from newstream.functions import get_default_site
from donations.models import Donation, Subscription
from donations.email_functions import *
User = get_user_model()

# can ignore these hardcodings for now, since these will be replaced by temporary objects in another branch later
DONATION_ID = 599
SUBSCRIPTION_ID = 80
USER_ID = 42

@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
class EmailTests(TestCase):
    '''
    test send all the emails
    '''

    def setUp(self):
        self.request = HttpRequest()
        self.request.method = 'POST'

        # add the absolute url to be be included in email
        default_site = get_default_site()
        self.request.site = default_site
        self.request.META['HTTP_HOST'] = default_site.hostname
        self.request.META['SERVER_PORT'] = 443

        self.donation = Donation.objects.get(pk=DONATION_ID)
        self.subscription = Subscription.objects.get(pk=SUBSCRIPTION_ID)
        self.user = User.objects.get(pk=USER_ID)

    def testDonationErrorNotifToAdmins(self):
        sendDonationErrorNotifToAdmins(self.donation, 'ERROR TITLE', 'ERROR DESCRIPTION')

    def testDonationNotifToAdmins(self):
        sendDonationNotifToAdmins(self.donation)

    def testDonationReceiptToDonor(self):
        sendDonationReceiptToDonor(self.donation)

    def testDonationStatusChangeToDonor(self):
        sendDonationStatusChangeToDonor(self.donation)

    def testSubscriptionStatusChangeToDonor(self):
        sendSubscriptionStatusChangeToDonor(self.subscription)

    def testRenewalNotifToAdmins(self):
        sendRenewalNotifToAdmins(self.donation)

    def testRenewalReceiptToDonor(self):
        sendRenewalReceiptToDonor(self.donation)

    def testRecurringUpdatedNotifToAdmins(self):
        sendRecurringUpdatedNotifToAdmins(self.subscription, 'TEXT MESSAGE')

    def testRecurringUpdatedNotifToDonor(self):
        sendRecurringUpdatedNotifToDonor(self.subscription, 'TEXT MESSAGE')

    def testRecurringPausedNotifToAdmins(self):
        sendRecurringPausedNotifToAdmins(self.subscription)

    def testRecurringPausedNotifToDonor(self):
        sendRecurringPausedNotifToDonor(self.subscription)

    def testRecurringResumedNotifToAdmins(self):
        sendRecurringResumedNotifToAdmins(self.subscription)

    def testRecurringResumedNotifToDonor(self):
        sendRecurringResumedNotifToDonor(self.subscription)

    def testRecurringCancelledNotifToAdmins(self):
        sendRecurringCancelledNotifToAdmins(self.subscription)

    def testRecurringCancelledNotifToDonor(self):
        sendRecurringCancelledNotifToDonor(self.subscription)

    def testAccountCreatedNotifToAdmins(self):
        sendAccountCreatedNotifToAdmins(self.user)

    def testAccountDeletedNotifToAdmins(self):
        sendAccountDeletedNotifToAdmins(self.user)

    def testAccountDeletedNotifToDonor(self):
        sendAccountDeletedNotifToDonor(self.user)

    def testVerificationEmail(self):
        sendVerificationEmail(self.request, self.user)