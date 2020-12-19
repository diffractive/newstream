from decimal import *
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from paypalcheckoutsdk.core import PayPalHttpClient

from newstream.functions import _debug
from donations.models import STATUS_PROCESSING, STATUS_ACTIVE, STATUS_CANCELLED, STATUS_COMPLETE, STATUS_PAUSED, Donation, Subscription, SubscriptionPaymentMeta, DonationPaymentMeta
from donations.email_functions import sendDonationReceiptToDonor, sendDonationNotifToAdmins, sendRenewalReceiptToDonor, sendRenewalNotifToAdmins, sendRecurringUpdatedNotifToDonor, sendRecurringUpdatedNotifToAdmins, sendRecurringPausedNotifToDonor, sendRecurringPausedNotifToAdmins, sendRecurringResumedNotifToDonor, sendRecurringResumedNotifToAdmins, sendRecurringCancelledNotifToDonor, sendRecurringCancelledNotifToAdmins
from donations.functions import gen_order_id
from donations.payment_gateways.gateway_manager import PaymentGatewayManager
from donations.payment_gateways.setting_classes import getPayPalSettings
from donations.payment_gateways.paypal.constants import *
from donations.payment_gateways.paypal.functions import activateSubscription, suspendSubscription, updateSubscription, cancelSubscription, getSubscriptionDetails


class Gateway_Paypal(PaymentGatewayManager):
    def __init__(self, request, donation=None, subscription=None, **kwargs):
        super().__init__(request, donation, subscription)
        # set paypal settings object
        self.settings = getPayPalSettings(request)
        # init paypal http client
        self.client = PayPalHttpClient(self.settings.environment)
        # saves all remaining kwargs into the manager, e.g. order_id, order_status
        self.__dict__.update(kwargs)

    def redirect_to_gateway_url(self):
        """ Overriding parent implementation as PayPal redirects with js on client browser """

        # save donation id in session for use in later checkout session creation
        self.request.session['donation_id'] = self.donation.id

        return render(self.request, 'donations/redirection_paypal.html', {'client_id': self.settings.client_id, 'currency': self.donation.currency})

    def process_webhook_response(self):
        # Event: EVENT_PAYMENT_CAPTURE_COMPLETED (This alone comes after the onetime donation is captured)
        if self.event_type == EVENT_PAYMENT_CAPTURE_COMPLETED:
            # payment should have been completed after successful capture at the moment of returning to this site
            # only run below code if somehow payment_status is still not complete(e.g. donor did not return to site)
            if self.donation.payment_status != STATUS_COMPLETE:
                self.donation.payment_status = STATUS_COMPLETE
                self.donation.save()
                # send email notifs
                sendDonationReceiptToDonor(self.request, self.donation)
                sendDonationNotifToAdmins(self.request, self.donation)

            return HttpResponse(status=200)

        # Event: EVENT_BILLING_SUBSCRIPTION_ACTIVATED
        if self.event_type == EVENT_BILLING_SUBSCRIPTION_ACTIVATED and hasattr(self, 'subscription'):
            if self.subscription['status'] == 'ACTIVE':
                if self.donation.subscription.recurring_status == STATUS_PROCESSING:
                    # save the new subscription, marked by object_id
                    self.donation.subscription.object_id = self.subscription['id']
                    self.donation.subscription.recurring_amount = Decimal(self.subscription['billing_info']['last_payment']['amount']['value'])
                    self.donation.subscription.currency = self.subscription['billing_info']['last_payment']['amount']['currency_code']
                    self.donation.subscription.recurring_status = STATUS_ACTIVE
                    self.donation.subscription.save()

                    # might be also set by payment-sale-completed, but in case this event is faster(for the email is sent next line)
                    self.donation.payment_status = STATUS_COMPLETE
                    self.donation.save()

                    # send the donation receipt to donor and notification to admins as subscription is just created
                    sendDonationReceiptToDonor(self.request, self.donation)
                    sendDonationNotifToAdmins(self.request, self.donation)

                return HttpResponse(status=200)
            else:
                raise ValueError(_("EVENT_BILLING_SUBSCRIPTION_ACTIVATED but subscription status is %(status)s") % {'status': self.subscription['status']})
        
        # Event: EVENT_BILLING_SUBSCRIPTION_UPDATED
        if self.event_type == EVENT_BILLING_SUBSCRIPTION_UPDATED and hasattr(self, 'subscription'):
            if self.subscription['status'] == 'SUSPENDED' or self.subscription['status'] == 'ACTIVE':
                subscription = Subscription.objects.filter(object_id=self.subscription['id']).first()
                if not subscription:
                    raise ValueError(_("Cannot find subscription object in database with object_id %(id)s") % {'id': self.subscription['id']})
                subscription.recurring_amount = Decimal(self.subscription['plan']['billing_cycles'][0]['pricing_scheme']['fixed_price']['value'])
                subscription.save()

                return HttpResponse(status=200)
            else:
                raise ValueError(_("EVENT_BILLING_SUBSCRIPTION_UPDATED but subscription status is %(status)s") % {'status': self.subscription['status']})

        # Event: EVENT_PAYMENT_SALE_COMPLETED
        if self.event_type == EVENT_PAYMENT_SALE_COMPLETED and hasattr(self, 'subscription'):
            if self.payload['state'] == 'completed':
                # check if this is first time subscription payment or a renewal payment
                donationPMs = DonationPaymentMeta.objects.filter(donation=self.donation, field_key='paypal_first_cycle')
                renewals = Donation.objects.filter(subscription__object_id=self.subscription['id'])
                _debug("Number of donation PMs: "+str(len(donationPMs)))
                _debug("Number of renewals for subscription_id({}): ".format(self.subscription['id'])+str(len(renewals)))
                if len(donationPMs) == 1 or len(renewals) >= 2:
                    # this is already a renewal payment
                    # self.donation is the first donation associated with the subscription
                    if not self.donation.subscription:
                        raise ValueError(_("Missing subscription linkage/object for donation %(id)s") % {'id': self.donation.id})
                    donation = Donation(
                        is_test=self.testing_mode,
                        subscription=self.donation.subscription,
                        order_number=gen_order_id(self.donation.gateway),
                        user=self.donation.user,
                        form=self.donation.form,
                        gateway=self.donation.gateway,
                        is_recurring=True,
                        donation_amount=Decimal(self.payload['amount']['total']),
                        currency=self.payload['amount']['currency'],
                        payment_status=STATUS_COMPLETE,
                        donation_date=datetime.now(),
                    )
                    # save new donation as a record of renewal donation
                    donation.save()

                    # email notifications
                    sendRenewalReceiptToDonor(self.request, donation)
                    sendRenewalNotifToAdmins(self.request, donation)
                else:
                    # this is a first time subscription payment
                    self.donation.payment_status = STATUS_COMPLETE
                    self.donation.save()
                    
                    # save DonationPaymentMeta as proof of first time subscription payment
                    dpmeta = DonationPaymentMeta(donation=self.donation, field_key='paypal_first_cycle', field_value='completed')
                    dpmeta.save()

                return HttpResponse(status=200)
            else:
               raise ValueError(_("EVENT_PAYMENT_SALE_COMPLETED but payment state is %(state)s") % {'state': self.payload['state']})

        # return 400 for all other events
        return HttpResponse(status=400)

    def update_recurring_payment(self, form_data):
        if not self.subscription:
            raise ValueError(_('Subscription object is None. Cannot update recurring payment.'))
        # update donation amount if it is different from database
        if form_data['recurring_amount'] != self.subscription.recurring_amount:
            updateSubscription(self.request, self.subscription.object_id, str(form_data['recurring_amount']), self.subscription.currency)

            self.subscription.recurring_amount = form_data['recurring_amount']
            self.subscription.save()

            # email notifications
            sendRecurringUpdatedNotifToAdmins(self.request, self.subscription, str(
                _("A Recurring Donation's amount has been updated on your website:")))
            sendRecurringUpdatedNotifToDonor(self.request, self.subscription, str(
                _("You have just updated your recurring donation amount.")))

            messages.add_message(self.request, messages.SUCCESS, _(
                'Your recurring donation amount at Stripe is updated successfully.'))


    def cancel_recurring_payment(self):
        if not self.subscription:
            raise ValueError(_('Subscription object is None. Cannot cancel recurring payment.'))
        cancelSubscription(self.request, self.subscription.object_id)
        # update newstream model
        self.subscription.recurring_status = STATUS_CANCELLED
        self.subscription.save()
        # email notifications
        sendRecurringCancelledNotifToAdmins(
            self.request, self.subscription)
        sendRecurringCancelledNotifToDonor(
            self.request, self.subscription)

    def toggle_recurring_payment(self):
        # no need to handle webhook events for activate/suspend actions(as they are too slow, donor might have already toggled twice before the first webhook arrives)
        # get realtime subscription's status from paypal
        req_subscription = getSubscriptionDetails(self.request, self.subscription.object_id)
        # if self.subscription.recurring_status == STATUS_PAUSED:
        if req_subscription['status'] == "SUSPENDED":
            # activate subscription(returns 204 if success)
            activateSubscription(self.request, self.subscription.object_id)
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
        # elif self.subscription.recurring_status == STATUS_ACTIVE:
        elif req_subscription['status'] == "ACTIVE":
            # suspend subscription(returns 204 if success)
            suspendSubscription(self.request, self.subscription.object_id)
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
