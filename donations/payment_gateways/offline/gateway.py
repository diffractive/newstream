from decimal import *
from datetime import datetime, timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from donations.models import Donation, DonationPaymentMeta, Subscription, SubscriptionPaymentMeta, STATUS_COMPLETE, STATUS_ACTIVE, STATUS_PROCESSING, STATUS_PAUSED, STATUS_CANCELLED
from donations.payment_gateways.gateway_manager import PaymentGatewayManager
from donations.payment_gateways.setting_classes import getOfflineSettings
from donations.functions import gen_transaction_id
from donations.email_functions import sendDonationReceiptToDonor, sendDonationNotifToAdmins, sendRenewalReceiptToDonor, sendRenewalNotifToAdmins, sendRecurringUpdatedNotifToDonor, sendRecurringUpdatedNotifToAdmins, sendRecurringPausedNotifToDonor, sendRecurringPausedNotifToAdmins, sendRecurringResumedNotifToDonor, sendRecurringResumedNotifToAdmins, sendRecurringCancelledNotifToDonor, sendRecurringCancelledNotifToAdmins
from newstream.functions import uuid4_str, getSiteName, getSiteSettings, getFullReverseUrl, printvars, _debug


class Gateway_Offline(PaymentGatewayManager):

    def __init__(self, request, donation=None, subscription=None, **kwargs):
        super().__init__(request, donation, subscription)
        # set offline settings object
        self.settings = getOfflineSettings(request)
        # saves all remaining kwargs into the manager
        self.__dict__.update(kwargs)

    def redirect_to_gateway_url(self):
        """ Overriding parent implementation, just redirecting to thank you page. """

        # save donation id in session for use in later checkout session creation
        self.request.session['return-donation-id'] = self.donation.id

        # send email notifs
        sendDonationReceiptToDonor(self.request, self.donation)
        sendDonationNotifToAdmins(self.request, self.donation)

        return redirect('donations:thank-you')

    def process_webhook_response(self):
        pass

    def update_recurring_payment(self, form_data):
        if not self.subscription:
            raise ValueError(_('Subscription object is None. Cannot update recurring payment.'))
        # update donation amount if it is different from database
        if form_data['recurring_amount'] != self.subscription.recurring_amount:
            self.subscription.recurring_amount = form_data['recurring_amount']
            self.subscription.recurring_status = STATUS_PROCESSING
            self.subscription.save()

            # email notifications
            sendRecurringUpdatedNotifToAdmins(self.request, self.subscription, str(
                _("A Recurring Donation's amount has been updated on your website:")))
            sendRecurringUpdatedNotifToDonor(self.request, self.subscription, str(
                _("You have just updated your recurring donation amount.")))

            messages.add_message(self.request, messages.SUCCESS, _(
                "Your offline recurring donation amount is updated successfully. Please wait for the administrator to complete the checking."))

    def cancel_recurring_payment(self):
        if not self.subscription:
            raise ValueError(_('Subscription object is None. Cannot cancel recurring payment.'))
        # update newstream model
        self.subscription.recurring_status = STATUS_CANCELLED
        self.subscription.save()
        # email notifications
        sendRecurringCancelledNotifToAdmins(
            self.request, self.subscription)
        sendRecurringCancelledNotifToDonor(
            self.request, self.subscription)

    def toggle_recurring_payment(self):
        if self.subscription.recurring_status == STATUS_PAUSED:
            # update newstream model
            self.subscription.recurring_status = STATUS_ACTIVE
            self.subscription.save()
            # email notifications
            sendRecurringResumedNotifToAdmins(
                self.request, self.subscription)
            sendRecurringResumedNotifToDonor(
                self.request, self.subscription)
            return {
                'button-html': '<span class="btn-text">'+str(_('Pause Recurring Donation'))+'</span><span class="icon"></span>',
                'recurring-status': STATUS_ACTIVE,
                'success-message': str(_('Your recurring donation is resumed.'))
            }
        elif self.subscription.recurring_status == STATUS_ACTIVE:
            # update newstream model
            self.subscription.recurring_status = STATUS_PAUSED
            self.subscription.save()
            # email notifications
            sendRecurringPausedNotifToAdmins(
                self.request, self.subscription)
            sendRecurringPausedNotifToDonor(
                self.request, self.subscription)
            return {
                'button-html': '<span class="btn-text">'+str(_('Resume Recurring Donation'))+'</span><span class="icon"></span>',
                'recurring-status': STATUS_PAUSED,
                'success-message': str(_('Your recurring donation is paused.'))
            }
        else:
            raise ValueError(_('Subscription object is neither Active or Paused'))
