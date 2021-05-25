from decimal import Decimal
from datetime import datetime, timezone
from django.conf import settings
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from wagtail.core.models import Site

from donations.models import Donation, STATUS_CANCELLED, STATUS_FAILED, STATUS_PAUSED, STATUS_PROCESSING, STATUS_REVOKED, Subscription, STATUS_COMPLETE, STATUS_ACTIVE
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
        currentSite = Site.objects.get(pk=1)
        self.request.META['HTTP_HOST'] = currentSite.hostname
        self.request.META['SERVER_PORT'] = 443
        self.request.site = currentSite

        # todo: find a way to let the tester input a different recipient email before running these tests
        self.recipient_email = 'franky+testemail@diffractive.io'

        # create test user
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
        

    def testDonationReceiptToDonor(self):
        result_code = sendDonationReceiptToDonor(self.request, self.donation, override_email=self.recipient_email)
        self.assertEqual(result_code, 1)

    def testDonationRevokedToDonor(self):
        self.donation.payment_status = STATUS_REVOKED
        result_code = sendDonationRevokedToDonor(self.request, self.donation, override_email=self.recipient_email)
        self.assertEqual(result_code, 1)

    def testDonationStatusChangeToDonor(self):
        result_code = sendDonationStatusChangeToDonor(self.request, self.donation, override_email=self.recipient_email)
        self.assertEqual(result_code, 1)

    def testSubscriptionStatusChangeToDonor(self):
        result_code = sendSubscriptionStatusChangeToDonor(self.request, self.subscription, override_email=self.recipient_email)
        self.assertEqual(result_code, 1)

    def testRenewalReceiptToDonor(self):
        result_code = sendRenewalReceiptToDonor(self.request, self.renewal_donation, override_email=self.recipient_email)
        self.assertEqual(result_code, 1)

    def testNewRecurringNotifToDonor(self):
        result_code = sendNewRecurringNotifToDonor(self.request, self.subscription, override_email=self.recipient_email)
        self.assertEqual(result_code, 1)

    def testRecurringAdjustedNotifToDonor(self):
        result_code = sendRecurringAdjustedNotifToDonor(self.request, self.subscription, override_email=self.recipient_email)
        self.assertEqual(result_code, 1)

    def testRecurringRescheduledNotifToDonor(self):
        result_code = sendRecurringRescheduledNotifToDonor(self.request, self.subscription, override_email=self.recipient_email)
        self.assertEqual(result_code, 1)

    def testRecurringPausedNotifToDonor(self):
        self.subscription.recurring_status = STATUS_PAUSED
        result_code = sendRecurringPausedNotifToDonor(self.request, self.subscription, override_email=self.recipient_email)
        self.assertEqual(result_code, 1)

    def testRecurringResumedNotifToDonor(self):
        result_code = sendRecurringResumedNotifToDonor(self.request, self.subscription, override_email=self.recipient_email)
        self.assertEqual(result_code, 1)

    def testRecurringCancelledNotifToDonor(self):
        self.subscription.recurring_status = STATUS_CANCELLED
        result_code = sendRecurringCancelledNotifToDonor(self.request, self.subscription, override_email=self.recipient_email)
        self.assertEqual(result_code, 1)

    def testAccountDeletedNotifToDonor(self):
        result_code = sendAccountDeletedNotifToDonor(self.request, self.user, override_email=self.recipient_email)
        self.assertEqual(result_code, 1)

    def testDonationErrorNotifToAdmins(self):
        self.donation.payment_status = STATUS_FAILED
        result_code = sendDonationErrorNotifToAdmins(self.request, self.donation, 'ERROR TITLE', 'ERROR DESCRIPTION', override_flag=True, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    def testDonationNotifToAdmins(self):
        result_code = sendDonationNotifToAdmins(self.request, self.donation, override_flag=True, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    def testDonationRevokedNotifToAdmins(self):
        self.donation.payment_status = STATUS_REVOKED
        result_code = sendDonationRevokedToAdmins(self.request, self.donation, override_flag=True, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    def testRenewalNotifToAdmins(self):
        result_code = sendRenewalNotifToAdmins(self.request, self.renewal_donation, override_flag=True, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    def testNewRecurringNotifToAdmins(self):
        result_code = sendNewRecurringNotifToAdmins(self.request, self.subscription, override_flag=True, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    def testRecurringAdjustedNotifToAdmins(self):
        result_code = sendRecurringAdjustedNotifToAdmins(self.request, self.subscription, override_flag=True, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    def testRecurringRescheduledNotifToAdmins(self):
        result_code = sendRecurringRescheduledNotifToAdmins(self.request, self.subscription, override_flag=True, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    def testRecurringPausedNotifToAdmins(self):
        self.subscription.recurring_status = STATUS_PAUSED
        result_code = sendRecurringPausedNotifToAdmins(self.request, self.subscription, override_flag=True, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    def testRecurringResumedNotifToAdmins(self):
        result_code = sendRecurringResumedNotifToAdmins(self.request, self.subscription, override_flag=True, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    def testRecurringCancelledNotifToAdmins(self):
        self.subscription.recurring_status = STATUS_CANCELLED
        result_code = sendRecurringCancelledNotifToAdmins(self.request, self.subscription, override_flag=True, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    def testRecurringCancelRequestNotifToAdmins(self):
        self.subscription.recurring_status = STATUS_PROCESSING
        result_code = sendRecurringCancelRequestNotifToAdmins(self.request, self.subscription, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    def testAccountCreatedNotifToAdmins(self):
        result_code = sendAccountCreatedNotifToAdmins(self.request, self.user, override_flag=True, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    def testAccountDeletedNotifToAdmins(self):
        result_code = sendAccountDeletedNotifToAdmins(self.request, self.user, override_flag=True, override_emails=[self.recipient_email])
        self.assertEqual(result_code, 1)

    # Skipped for the moment due to this error during testing:
    # django.contrib.messages.api.MessageFailure: You cannot add messages without installing django.contrib.messages.middleware.MessageMiddleware
    # def testVerificationEmail(self):
    #     result_code = sendVerificationEmail(self.request, self.user)
    #     self.assertEqual(result_code, 1)