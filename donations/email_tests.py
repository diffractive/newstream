from decimal import Decimal
from datetime import datetime, timezone
from django.conf import settings
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from wagtail.core.models import Site

from donations.models import Donation, Subscription, STATUS_COMPLETE, STATUS_ACTIVE
from donations.email_functions import *
from site_settings.models import PaymentGateway, GATEWAY_STRIPE
User = get_user_model()


@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
class EmailTests(TestCase):
    '''
    test send all the emails
    '''

    def setUp(self):
        self.request = HttpRequest()
        self.request.method = 'POST'

        # add the absolute url to be be included in email
        if settings.DEBUG:
            self.request.META['HTTP_HOST'] = 'newstream-staging.diffractive.io'
        else:
            self.request.META['HTTP_HOST'] = 'support.hongkongfp.com'
        self.request.META['SERVER_PORT'] = 443
        self.request.site = Site.objects.get(pk=1)

        self.user = User.objects.create_user(email="franky+testemail@diffractive.io", password="12345678")
        self.user.first_name = 'Franky'
        self.user.last_name = 'Hung'
        self.donation = Donation(
            is_test=True,
            transaction_id="TEST-ABCDE12345",
            user=self.user,
            gateway=PaymentGateway.objects.get(title=GATEWAY_STRIPE),
            is_recurring=False,
            donation_amount=Decimal("10.00"),
            currency="HKD",
            guest_email='',
            payment_status=STATUS_COMPLETE,
            donation_date=datetime.now(timezone.utc),
        )
        self.subscription = Subscription(
            is_test=True,
            profile_id='TEST-FGHIJ67890',
            user=self.user,
            gateway=PaymentGateway.objects.get(title=GATEWAY_STRIPE),
            recurring_amount=Decimal("10.00"),
            currency="HKD",
            recurring_status=STATUS_ACTIVE,
            subscribe_date=datetime.now(timezone.utc)
        )

    def testDonationErrorNotifToAdmins(self):
        sendDonationErrorNotifToAdmins(self.request, self.donation, 'ERROR TITLE', 'ERROR DESCRIPTION')

    def testDonationNotifToAdmins(self):
        sendDonationNotifToAdmins(self.request, self.donation)

    def testDonationReceiptToDonor(self):
        sendDonationReceiptToDonor(self.request, self.donation)

    def testDonationRevokedNotifToAdmins(self):
        sendDonationRevokedToAdmins(self.request, self.donation)

    def testDonationRevokedToDonor(self):
        sendDonationRevokedToDonor(self.request, self.donation)

    def testDonationStatusChangeToDonor(self):
        sendDonationStatusChangeToDonor(self.request, self.donation)

    def testSubscriptionStatusChangeToDonor(self):
        sendSubscriptionStatusChangeToDonor(self.request, self.subscription)

    def testRenewalNotifToAdmins(self):
        sendRenewalNotifToAdmins(self.request, self.donation)

    def testRenewalReceiptToDonor(self):
        sendRenewalReceiptToDonor(self.request, self.donation)

    def testNewRecurringNotifToAdmins(self):
        sendNewRecurringNotifToAdmins(self.request, self.subscription)

    def testNewRecurringNotifToDonor(self):
        sendNewRecurringNotifToDonor(self.request, self.subscription)

    def testRecurringAdjustedNotifToAdmins(self):
        sendRecurringAdjustedNotifToAdmins(self.request, self.subscription)

    def testRecurringAdjustedNotifToDonor(self):
        sendRecurringAdjustedNotifToDonor(self.request, self.subscription)

    def testRecurringRescheduledNotifToAdmins(self):
        sendRecurringRescheduledNotifToAdmins(self.request, self.subscription)

    def testRecurringRescheduledNotifToDonor(self):
        sendRecurringRescheduledNotifToDonor(self.request, self.subscription)

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