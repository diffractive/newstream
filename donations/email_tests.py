from decimal import Decimal
from datetime import datetime, timezone
from django.conf import settings
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.test.utils import override_settings

from newstream.functions import get_default_site
from donations.models import Donation, Subscription, STATUS_COMPLETE, STATUS_ACTIVE, STATUS_FAILED, STATUS_REVOKED, STATUS_PAUSED, STATUS_CANCELLED
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
        default_site = get_default_site()
        self.request.site = default_site
        self.request.META['HTTP_HOST'] = default_site.hostname
        self.request.META['SERVER_PORT'] = 443

        self.user = User.objects.create_user(email="franky+testemail@diffractive.io", password="12345678")
        self.user.first_name = 'Franky'
        self.user.last_name = 'Hung'
        # create test Donation
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
        # create test Subscription
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
        # create test Renewal Donation
        self.renewal_donation = Donation(
            is_test=True,
            transaction_id="TEST-ABCDE12345",
            user=self.user,
            gateway=PaymentGateway.objects.get(title=GATEWAY_STRIPE),
            is_recurring=True,
            subscription=self.subscription,
            donation_amount=Decimal("10.00"),
            currency="HKD",
            guest_email='',
            payment_status=STATUS_COMPLETE,
            donation_date=datetime.now(timezone.utc),
        )
        # just set the subscription id to an arbitrary number
        # to prevent the django.urls.exceptions.NoReverseMatch error when using getFullReverseUrl in plain_texts.get_renewal_receipt_text
        self.renewal_donation.subscription.id = 1

    def testDonationErrorNotifToAdmins(self):
        self.donation.payment_status = STATUS_FAILED
        sendDonationErrorNotifToAdmins(self.donation, 'ERROR TITLE', 'ERROR DESCRIPTION')

    def testDonationNotifToAdmins(self):
        sendDonationNotifToAdmins(self.donation)

    def testDonationReceiptToDonor(self):
        sendDonationReceiptToDonor(self.donation)

    def testDonationRevokedNotifToAdmins(self):
        self.donation.payment_status = STATUS_REVOKED
        sendDonationRevokedToAdmins(self.donation)

    def testDonationRevokedToDonor(self):
        self.donation.payment_status = STATUS_REVOKED
        sendDonationRevokedToDonor(self.donation)

    def testDonationStatusChangeToDonor(self):
        sendDonationStatusChangeToDonor(self.donation)

    def testSubscriptionStatusChangeToDonor(self):
        sendSubscriptionStatusChangeToDonor(self.subscription)

    def testRenewalNotifToAdmins(self):
        sendRenewalNotifToAdmins(self.renewal_donation)

    def testRenewalReceiptToDonor(self):
        sendRenewalReceiptToDonor(self.renewal_donation)

    def testNewRecurringNotifToAdmins(self):
        sendNewRecurringNotifToAdmins(self.subscription)

    def testNewRecurringNotifToDonor(self):
        sendNewRecurringNotifToDonor(self.subscription)

    def testRecurringAdjustedNotifToAdmins(self):
        sendRecurringAdjustedNotifToAdmins(self.subscription)

    def testRecurringAdjustedNotifToDonor(self):
        sendRecurringAdjustedNotifToDonor(self.subscription)

    def testRecurringRescheduledNotifToAdmins(self):
        sendRecurringRescheduledNotifToAdmins(self.subscription)

    def testRecurringRescheduledNotifToDonor(self):
        sendRecurringRescheduledNotifToDonor(self.subscription)

    def testRecurringPausedNotifToAdmins(self):
        self.subscription.recurring_status = STATUS_PAUSED
        sendRecurringPausedNotifToAdmins(self.subscription)

    def testRecurringPausedNotifToDonor(self):
        self.subscription.recurring_status = STATUS_PAUSED
        sendRecurringPausedNotifToDonor(self.subscription)

    def testRecurringResumedNotifToAdmins(self):
        sendRecurringResumedNotifToAdmins(self.subscription)

    def testRecurringResumedNotifToDonor(self):
        sendRecurringResumedNotifToDonor(self.subscription)

    def testRecurringCancelledNotifToAdmins(self):
        self.subscription.recurring_status = STATUS_CANCELLED
        sendRecurringCancelledNotifToAdmins(self.subscription)

    def testRecurringCancelledNotifToDonor(self):
        self.subscription.recurring_status = STATUS_CANCELLED
        sendRecurringCancelledNotifToDonor(self.subscription)

    def testAccountCreatedNotifToAdmins(self):
        sendAccountCreatedNotifToAdmins(self.user)

    def testAccountDeletedNotifToAdmins(self):
        sendAccountDeletedNotifToAdmins(self.user)

    def testAccountDeletedNotifToDonor(self):
        sendAccountDeletedNotifToDonor(self.user)

    # def testVerificationEmail(self):
    #     sendVerificationEmail(self.user)