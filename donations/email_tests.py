from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from wagtail.core.models import Site

from donations.models import Donation, Subscription
from donations.email_functions import *
User = get_user_model()

# tweak these settings for your tests
TEST_DOMAIN_NAME = "newstream.hongkongfp.com"
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
        self.request.META['HTTP_HOST'] = 'newstream.hongkongfp.com'
        self.request.META['SERVER_PORT'] = 443
        self.request.site = Site.objects.get(pk=1)

        self.donation = Donation.objects.get(pk=DONATION_ID)
        self.subscription = Subscription.objects.get(pk=SUBSCRIPTION_ID)
        self.user = User.objects.get(pk=USER_ID)

    def testDonationErrorNotifToAdmins(self):
        sendDonationErrorNotifToAdmins(self.request, self.donation, 'ERROR TITLE', 'ERROR DESCRIPTION')

    def testDonationNotifToAdmins(self):
        sendDonationNotifToAdmins(self.request, self.donation)

    def testDonationReceiptToDonor(self):
        sendDonationReceiptToDonor(self.request, self.donation)

    def testDonationStatusChangeToDonor(self):
        sendDonationStatusChangeToDonor(self.request, self.donation)

    def testSubscriptionStatusChangeToDonor(self):
        sendSubscriptionStatusChangeToDonor(self.request, self.subscription)

    def testRenewalNotifToAdmins(self):
        sendRenewalNotifToAdmins(self.request, self.donation)

    def testRenewalReceiptToDonor(self):
        sendRenewalReceiptToDonor(self.request, self.donation)

    def testRecurringUpdatedNotifToAdmins(self):
        sendRecurringUpdatedNotifToAdmins(self.request, self.subscription, 'TEXT MESSAGE')

    def testRecurringUpdatedNotifToDonor(self):
        sendRecurringUpdatedNotifToDonor(self.request, self.subscription, 'TEXT MESSAGE')

    def testRecurringPausedNotifToAdmins(self):
        sendRecurringPausedNotifToAdmins(self.request, self.subscription)

    def testRecurringPausedNotifToDonor(self):
        sendRecurringPausedNotifToDonor(self.request, self.subscription)

    def testRecurringResumedNotifToAdmins(self):
        sendRecurringResumedNotifToAdmins(self.request, self.subscription)

    def testRecurringResumedNotifToDonor(self):
        sendRecurringResumedNotifToDonor(self.request, self.subscription)

    def testRecurringCancelledNotifToAdmins(self):
        sendRecurringCancelledNotifToAdmins(self.request, self.subscription)

    def testRecurringCancelledNotifToDonor(self):
        sendRecurringCancelledNotifToDonor(self.request, self.subscription)

    def testAccountCreatedNotifToAdmins(self):
        sendAccountCreatedNotifToAdmins(self.request, self.user)

    def testAccountDeletedNotifToAdmins(self):
        sendAccountDeletedNotifToAdmins(self.request, self.user)

    def testAccountDeletedNotifToDonor(self):
        sendAccountDeletedNotifToDonor(self.request, self.user)

    def testVerificationEmail(self):
        sendVerificationEmail(self.request, self.user)