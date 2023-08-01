from decimal import Decimal
from datetime import datetime, timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from paypalcheckoutsdk.core import PayPalHttpClient

from newstream.functions import _debug, round_half_up
from donations.models import STATUS_PROCESSING, STATUS_FAILED, STATUS_ACTIVE, STATUS_CANCELLED, STATUS_COMPLETE, STATUS_PAUSED, STATUS_PAYMENT_FAILED, Donation, SubscriptionInstance, SubscriptionPaymentMeta, DonationPaymentMeta
from donations.email_functions import (sendDonationReceiptToDonor, sendDonationNotifToAdmins, sendNewRecurringNotifToAdmins,
    sendNewRecurringNotifToDonor, sendRecurringAdjustedNotifToAdmins, sendRecurringAdjustedNotifToDonor, sendRenewalReceiptToDonor,
    sendRenewalNotifToAdmins, sendRecurringPausedNotifToDonor, sendRecurringPausedNotifToAdmins, sendRecurringResumedNotifToDonor,
    sendRecurringResumedNotifToAdmins, sendRecurringCancelledNotifToDonor, sendRecurringCancelledNotifToAdmins,
    sendFailedPaymentNotifToAdmins, sendFailedPaymentNotifToDonor, sendReactivatedPaymentNotifToAdmins, sendReactivatedPaymentNotifToDonor)
from donations.functions import gen_transaction_id
from donations.payment_gateways.gateway_manager import PaymentGatewayManager
from donations.payment_gateways.setting_classes import getPayPalSettings
from donations.payment_gateways.paypal.constants import *
from donations.payment_gateways.paypal.functions import activateSubscription, suspendSubscription, updateSubscription, cancelSubscription, getSubscriptionDetails, getPlanDetails


class Gateway_Paypal(PaymentGatewayManager):
    def __init__(self, request, donation=None, subscription=None, **kwargs):
        super().__init__(request, donation, subscription)
        # set paypal settings object
        self.settings = getPayPalSettings()
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
            # update transaction_id
            self.donation.transaction_id = self.payload['id']
            self.donation.save()
            # payment should have been completed after successful capture at the moment of returning to this site
            # only run below code if somehow payment_status is still not complete(e.g. donor did not return to site)
            if self.donation.payment_status != STATUS_COMPLETE:
                self.donation.payment_status = STATUS_COMPLETE
                self.donation.save()

            # send email notifs
            sendDonationReceiptToDonor(self.donation)
            sendDonationNotifToAdmins(self.donation)

            return HttpResponse(status=200)

        # Event: EVENT_BILLING_SUBSCRIPTION_ACTIVATED
        if self.event_type == EVENT_BILLING_SUBSCRIPTION_ACTIVATED and hasattr(self, 'subscription_obj'):
            if self.subscription_obj['status'] == 'ACTIVE':
                if self.donation.subscription.recurring_status == STATUS_PROCESSING:
                    # save the new subscription, marked by profile_id
                    self.donation.subscription.profile_id = self.subscription_obj['id']
                    self.donation.subscription.recurring_amount = Decimal(self.subscription_obj['billing_info']['last_payment']['amount']['value'])
                    self.donation.subscription.currency = self.subscription_obj['billing_info']['last_payment']['amount']['currency_code']
                    self.donation.subscription.recurring_status = STATUS_ACTIVE
                    self.donation.subscription.save()

                    # Update card flow, will include the old_instance_id metadata
                    try:
                        spmeta = SubscriptionPaymentMeta.objects.get(subscription=self.donation.subscription, field_key='old_instance_id')

                        # send notif emails to admins and donor as a previously failed payment has now succeeded
                        sendReactivatedPaymentNotifToAdmins(self.donation.subscription)
                        sendReactivatedPaymentNotifToDonor(self.donation.subscription)

                        # We want to remove the update card flow flag, so we delete the metadata
                        spmeta.delete()
                    # Not part of the card update flow so a normal new recurring payment
                    except SubscriptionPaymentMeta.DoesNotExist:

                        # send the new recurring notifs to admins and donor as subscription is just active
                        sendNewRecurringNotifToAdmins(self.donation.subscription)
                        sendNewRecurringNotifToDonor(self.donation.subscription)

                return HttpResponse(status=200)
            else:
                raise ValueError(_("EVENT_BILLING_SUBSCRIPTION_ACTIVATED but subscription status is %(status)s") % {'status': self.subscription_obj['status']})

        # Event: EVENT_BILLING_SUBSCRIPTION_UPDATED
        if self.event_type == EVENT_BILLING_SUBSCRIPTION_UPDATED and hasattr(self, 'subscription_obj'):
            if self.subscription_obj['status'] == 'SUSPENDED' or self.subscription_obj['status'] == 'ACTIVE':
                subscription = SubscriptionInstance.objects.filter(profile_id=self.subscription_obj['id']).first()
                if not subscription:
                    raise ValueError(_("Cannot find subscription object in database with profile_id %(id)s") % {'id': self.subscription_obj['id']})
                subscription.recurring_amount = Decimal(self.subscription_obj['plan']['billing_cycles'][0]['pricing_scheme']['fixed_price']['value'])
                subscription.save()

                return HttpResponse(status=200)
            else:
                raise ValueError(_("EVENT_BILLING_SUBSCRIPTION_UPDATED but subscription status is %(status)s") % {'status': self.subscription_obj['status']})

        # Event: EVENT_PAYMENT_SALE_COMPLETED
        if self.event_type == EVENT_PAYMENT_SALE_COMPLETED and hasattr(self, 'subscription_obj'):
            if self.payload['state'] == 'completed':
                # check if this is first time subscription payment or a renewal payment
                donationPMs = DonationPaymentMeta.objects.filter(donation=self.donation, field_key='paypal_first_cycle')
                renewals = Donation.objects.filter(subscription__profile_id=self.subscription_obj['id'])
                _debug("Number of donation PMs: "+str(len(donationPMs)))
                _debug("Number of renewals for subscription_id({}): ".format(self.subscription_obj['id'])+str(len(renewals)))
                if len(donationPMs) == 1 or len(renewals) >= 2:
                    # this is already a renewal payment
                    # self.donation is the first donation associated with the subscription
                    if not self.donation.subscription:
                        raise ValueError(_("Missing subscription linkage/object for donation %(id)s") % {'id': self.donation.id})
                    donation = Donation(
                        is_test=self.donation.is_test,
                        subscription=self.donation.subscription,
                        transaction_id=self.payload['id'],
                        user=self.donation.user,
                        form=self.donation.form,
                        gateway=self.donation.gateway,
                        is_recurring=True,
                        donation_amount=Decimal(self.payload['amount']['total']),
                        currency=self.payload['amount']['currency'],
                        payment_status=STATUS_COMPLETE,
                        donation_date=datetime.now(timezone.utc),
                    )
                    # save new donation as a record of renewal donation
                    donation.save()

                    # Update subscription status if it has previously failed
                    if self.donation.subscription.recurring_status == STATUS_PAYMENT_FAILED:
                        self.donation.subscription.recurring_status = STATUS_ACTIVE
                        self.donation.subscription.save()

                        # send notif emails to admins and donor as a previously failed payment has now succeeded
                        sendReactivatedPaymentNotifToAdmins(self.donation.subscription)
                        sendReactivatedPaymentNotifToDonor(self.donation.subscription)

                    # email notifications
                    # disabling renewal emails for the moment
                    # sendRenewalReceiptToDonor(donation)
                    # sendRenewalNotifToAdmins(donation)
                else:
                    # this is a first time subscription payment
                    self.donation.payment_status = STATUS_COMPLETE
                    self.donation.transaction_id = self.payload['id']
                    self.donation.save()

                    # save DonationPaymentMeta as proof of first time subscription payment
                    dpmeta = DonationPaymentMeta(donation=self.donation, field_key='paypal_first_cycle', field_value='completed')
                    dpmeta.save()

                return HttpResponse(status=200)
            else:
               raise ValueError(_("EVENT_PAYMENT_SALE_COMPLETED but payment state is %(state)s") % {'state': self.payload['state']})

        # Event: EVENT_BILLING_SUBSCRIPTION_PAYMENT_FAILED
        if self.event_type == EVENT_BILLING_SUBSCRIPTION_PAYMENT_FAILED and hasattr(self, 'subscription_obj'):
            # We don't want to update processing failures or cancelled subscriptions
            if self.subscription_obj['status'] == 'ACTIVE':

                subscription = SubscriptionInstance.objects.get(profile_id=self.subscription_obj['id'])
                subscription.recurring_status = STATUS_PAYMENT_FAILED
                subscription.save()

                # Semd email notifying user and admin of issue
                sendFailedPaymentNotifToAdmins(subscription)
                sendFailedPaymentNotifToDonor(subscription)

            return HttpResponse(status=200)

        # Event: EVENT_BILLING_SUBSCRIPTION_CANCELLED
        if self.event_type == EVENT_BILLING_SUBSCRIPTION_CANCELLED and hasattr(self, 'subscription_obj'):
            if self.subscription_obj['status'] == 'CANCELLED':
                self.donation.subscription.recurring_status = STATUS_CANCELLED
                self.donation.subscription.save()

                # Dont send an email in update card process
                try:
                    # This value only exists for subscriptions that are part of the update card process
                    spmeta = SubscriptionPaymentMeta.objects.get(subscription=self.donation.subscription, field_key='awaiting_cancelation')
                    spmeta.delete()
                except SubscriptionPaymentMeta.DoesNotExist:
                    print("No spmeta linked to %s is found" % self.donation.subscription.profile_id)
                    # send email notifications here for all other cancellation scenarios
                    sendRecurringCancelledNotifToAdmins(self.donation.subscription)
                    sendRecurringCancelledNotifToDonor(self.donation.subscription)
                return HttpResponse(status=200)
            else:
               raise ValueError(_("EVENT_BILLING_SUBSCRIPTION_CANCELLED but subscription status is %(status)s") % {'status': self.subscription_obj['status']})

        # Event: EVENT_BILLING_SUBSCRIPTION_SUSPENDED
        # note that this event is also triggered when user pause the recurring donation, but we don't further process this event for the pause scenario since it's already been handled in toggle_recurring_payment()
        if self.event_type == EVENT_BILLING_SUBSCRIPTION_SUSPENDED and hasattr(self, 'subscription_obj'):
            if self.subscription_obj['status'] == 'SUSPENDED':
                plan = getPlanDetails(self.request.session, self.subscription_obj['plan_id'])
                
                if int(self.subscription_obj["billing_info"]["failed_payments_count"]) >= int(plan['payment_preferences']['payment_failure_threshold']):
                    print("Marking PayPal Subscription {sub_id} as cancelled since failed_payments_count({failed_payments_count}) reached payment_failure_threshold of {payment_failure_threshold}".format(sub_id=self.subscription_obj["id"], failed_payments_count=self.subscription_obj["billing_info"]["failed_payments_count"], payment_failure_threshold=plan['payment_preferences']['payment_failure_threshold']))
                    self.donation.subscription.recurring_status = STATUS_CANCELLED
                    self.donation.subscription.cancel_reason = SubscriptionInstance.CancelReason.PAYMENTS_FAILED
                    self.donation.subscription.save()

                    sendRecurringCancelledNotifToAdmins(self.donation.subscription)
                    sendRecurringCancelledNotifToDonor(self.donation.subscription)
                
                return HttpResponse(status=200)
            else:
               raise ValueError(_("EVENT_BILLING_SUBSCRIPTION_SUSPENDED but subscription status is %(status)s") % {'status': self.subscription_obj['status']})

        # return 400 for all other events
        return HttpResponse(status=400)

    def update_recurring_payment(self, form_data):
        if not self.subscription:
            raise ValueError(_('SubscriptionInstance object is None. Cannot update recurring payment.'))
        # update donation amount if it is different from database
        if form_data['recurring_amount'] != self.subscription.recurring_amount:
            updateSubscription(self.request.session, self.subscription.profile_id, str(form_data['recurring_amount']), self.subscription.currency)

            self.subscription.recurring_amount = form_data['recurring_amount']
            self.subscription.save()

            # email notifications
            sendRecurringAdjustedNotifToAdmins(self.subscription)
            sendRecurringAdjustedNotifToDonor(self.subscription)

            messages.add_message(self.request, messages.SUCCESS, _(
                'Your recurring donation amount via PayPal is updated successfully.'))


    def cancel_recurring_payment(self, reason=None):
        if not self.subscription:
            raise ValueError(_('SubscriptionInstance object is None. Cannot cancel recurring payment.'))
        # update newstream model
        self.subscription.recurring_status = STATUS_CANCELLED
        self.subscription.cancel_reason = reason
        self.subscription.save()
        cancelSubscription(self.request.session, self.subscription.profile_id)


    def toggle_recurring_payment(self):
        # no need to handle webhook events for activate/suspend actions(as they are too slow, donor might have already toggled twice before the first webhook arrives)
        # get realtime subscription's status from paypal
        req_subscription = getSubscriptionDetails(self.request.session, self.subscription.profile_id)
        # if self.subscription.recurring_status == STATUS_PAUSED:
        if req_subscription['status'] == "SUSPENDED":
            # activate subscription(returns 204 if success)
            activateSubscription(self.request.session, self.subscription.profile_id)
            # update newstream model
            self.subscription.recurring_status = STATUS_ACTIVE
            self.subscription.save()
            # email notifications
            sendRecurringResumedNotifToAdmins(self.subscription)
            sendRecurringResumedNotifToDonor(self.subscription)
            return {
                'button-text': str(_('Pause Recurring Donation')),
                'recurring-status': STATUS_ACTIVE,
                'success-message': str(_('Your recurring donation via PayPal  is resumed.'))
            }
        # elif self.subscription.recurring_status == STATUS_ACTIVE:
        elif req_subscription['status'] == "ACTIVE":
            # suspend subscription(returns 204 if success)
            suspendSubscription(self.request.session, self.subscription.profile_id)
            # update newstream model
            self.subscription.recurring_status = STATUS_PAUSED
            self.subscription.save()
            # email notifications
            sendRecurringPausedNotifToAdmins(self.subscription)
            sendRecurringPausedNotifToDonor(self.subscription)
            return {
                'button-text': str(_('Resume Recurring Donation')),
                'recurring-status': STATUS_PAUSED,
                'success-message': str(_('Your recurring donation via PayPal  is paused.'))
            }
        else:
            raise ValueError(_('SubscriptionInstance object is neither Active or Paused'))
