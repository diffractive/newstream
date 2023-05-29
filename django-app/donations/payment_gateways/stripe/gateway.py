import stripe
from datetime import datetime, timezone
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from donations.models import (Donation, DonationPaymentMeta, SubscriptionPaymentMeta, STATUS_COMPLETE,
    STATUS_ACTIVE, STATUS_PROCESSING, STATUS_PAUSED, STATUS_CANCELLED, STATUS_PAYMENT_FAILED)
from donations.payment_gateways.gateway_manager import PaymentGatewayManager
from donations.payment_gateways.setting_classes import getStripeSettings
from donations.payment_gateways.stripe.constants import *
from donations.email_functions import (sendDonationReceiptToDonor, sendDonationNotifToAdmins,
    sendNewRecurringNotifToAdmins, sendNewRecurringNotifToDonor, sendRecurringAdjustedNotifToAdmins,
    sendRecurringAdjustedNotifToDonor, sendRecurringRescheduledNotifToAdmins, sendRecurringRescheduledNotifToDonor,
    sendRenewalReceiptToDonor, sendRenewalNotifToAdmins, sendRecurringPausedNotifToDonor,
    sendRecurringPausedNotifToAdmins, sendRecurringResumedNotifToDonor, sendRecurringResumedNotifToAdmins,
    sendRecurringCancelledNotifToDonor, sendRecurringCancelledNotifToAdmins, sendFailedPaymentNotifToAdmins,
    sendFailedPaymentNotifToDonor, sendReactivatedPaymentNotifToAdmins, sendReactivatedPaymentNotifToDonor)
from newstream.functions import _debug
from donations.payment_gateways.stripe.functions import initStripeApiKey, formatDonationAmount, formatDonationAmountFromGateway


class Gateway_Stripe(PaymentGatewayManager):
    def __init__(self, request, donation=None, subscription=None, **kwargs):
        '''
        Note that the subscription parameter passed here should always be a newstream model.

        Other stripe objects are to be passed in kwargs, including session, event and invoice
        session: this is the stripe checkout session object, stores also the donation_id in the metadata
        event: this is the stripe event object when stripe webhooks are triggered and emitted to our server
        subscription_obj: this is the stripe subscription object fetched directly or retrieved indirectly from the webhook payload
        invoice: this is the stripe invoice object sent to our server when a payment has succeeded or failed
        '''
        super().__init__(request, donation, subscription)
        # set stripe settings object
        self.settings = getStripeSettings()
        # saves all remaining kwargs into the manager, e.g. session, event, invoice
        self.__dict__.update(kwargs)

    def redirect_to_gateway_url(self):
        """ Overriding parent implementation as Stripe redirects with js on client browser """

        # save donation id in session for use in later checkout session creation
        self.request.session['donation_id'] = self.donation.id

        return render(self.request, 'donations/redirection_stripe.html', {'publishable_key': self.settings.publishable_key})

    def process_webhook_response(self):
        initStripeApiKey()
        # Decide what actions to perform on Newstream's side according to the results/events from the Stripe notifications
        # Event: checkout.session.completed
        if self.event['type'] == EVENT_CHECKOUT_SESSION_COMPLETED:
            # Update payment status
            self.donation.payment_status = STATUS_COMPLETE
            # update donation_date
            self.donation.donation_date = datetime.now(timezone.utc)
            self.donation.save()

            # Since for recurring payment, subscription.updated event might lag behind checkout.session.completed
            if not self.donation.is_recurring:
                sendDonationReceiptToDonor(self.donation)
                sendDonationNotifToAdmins(self.donation)

            return HttpResponse(status=200)

        # Event: payment_intent.succeeded
        # Should be handled for onetime donations
        if self.event['type'] == EVENT_PAYMENT_INTENT_SUCCEEDED:
            # Update payment transaction_id as the charge id
            self.donation.transaction_id = self.payment_intent['charges']['data'][0]['id']
            self.donation.save()

            return HttpResponse(status=200)

        # Event: invoice.created (for subscriptions, just return 200 here and do nothing - to signify to Stripe that it can proceed and finalize the invoice)
        # https://stripe.com/docs/billing/subscriptions/webhooks#understand
        if self.event['type'] == EVENT_INVOICE_CREATED and hasattr(self, 'subscription_obj') and hasattr(self, 'invoice'):
            return HttpResponse(status=200)

        # Event: invoice.paid (for subscriptions)
        if self.event['type'] == EVENT_INVOICE_PAID and hasattr(self, 'subscription_obj') and hasattr(self, 'invoice'):
            if self.invoice.status == 'paid':
                _debug("[stripe recurring] Invoice confirmed paid")
                # check if subscription has one or more invoices to determine it's a first time or renewal payment
                # self.subscription_obj here is the stripe subscription object
                try:
                    invoices = stripe.Invoice.list(subscription=self.subscription_obj.id)
                except (stripe.error.RateLimitError, stripe.error.InvalidRequestError, stripe.error.AuthenticationError, stripe.error.APIConnectionError, stripe.error.StripeError) as e:
                    raise RuntimeError("Stripe API Error({}): Status({}), Code({}), Param({}), Message({})".format(type(e).__name__, e.http_status, e.code, e.param, e.user_message))
                # _debug("Stripe: Subscription {} has {} invoices.".format(self.subscription_obj.id, len(invoices['data'])))
                if len(invoices['data']) == 1:
                    _debug("[stripe recurring] First time subscription")
                    # save charge id as donation.transaction_id
                    self.donation.transaction_id = self.invoice.charge
                    self.donation.payment_status = STATUS_COMPLETE
                    self.donation.save()

                    # also save the invoice number as a DonationPaymentMeta
                    dpmeta = DonationPaymentMeta(
                        donation=self.donation, field_key='stripe_invoice_number', field_value=self.invoice.number)
                    dpmeta.save()
                elif len(invoices['data']) > 1:
                    _debug("[stripe recurring] About to add renewal donation")
                    # create a new donation record + then send donation receipt to user
                    # self.donation is the first donation made for a subscription
                    donation = Donation(
                        is_test=self.donation.is_test,
                        subscription=self.donation.subscription,
                        transaction_id=self.invoice.charge,
                        user=self.donation.user,
                        form=self.donation.form,
                        gateway=self.donation.gateway,
                        is_recurring=True,
                        donation_amount=formatDonationAmountFromGateway(str(self.invoice.amount_paid), self.donation.currency),
                        currency=self.donation.currency,
                        payment_status=STATUS_COMPLETE,
                        donation_date=datetime.now(timezone.utc),
                    )
                    donation.save()

                    dpmeta = DonationPaymentMeta(
                        donation=donation, field_key='stripe_invoice_number', field_value=self.invoice.number)
                    dpmeta.save()

                    # email notifications
                    # disabling renewal emails for the moment
                    # sendRenewalReceiptToDonor(donation)
                    # sendRenewalNotifToAdmins(donation)

                # log down the current subscription period span
                spmeta = SubscriptionPaymentMeta(
                    subscription=self.donation.subscription, field_key='stripe_subscription_period', field_value=str(self.subscription_obj.current_period_start)+'-'+str(self.subscription_obj.current_period_end))
                spmeta.save()

                return HttpResponse(status=200)

        # Event: invoice.payment_failed
        if self.event['type'] == EVENT_INVOICE_PAYMENT_FAILED and hasattr(self, 'subscription_obj') and hasattr(self, 'invoice'):
            # We don't want to update processing failures or cancelled subscriptions
            if self.donation.subscription.recurring_status in [STATUS_ACTIVE, STATUS_PAYMENT_FAILED]:

                # Update subscription to payment_failed status
                self.donation.subscription.recurring_status = STATUS_PAYMENT_FAILED
                self.donation.subscription.save()

                # Semd email notifying user and admin of issue
                sendFailedPaymentNotifToAdmins(self.donation.subscription)
                sendFailedPaymentNotifToDonor(self.donation.subscription)

        # Event: customer.subscription.updated
        if self.event['type'] == EVENT_CUSTOMER_SUBSCRIPTION_UPDATED and hasattr(self, 'subscription_obj'):
            # Subscription active after invoice paid
            if self.subscription_obj['status'] == 'active':
                if self.donation.subscription.recurring_status == STATUS_PROCESSING:
                    # save the new subscription, marked by profile_id
                    self.donation.subscription.profile_id = self.subscription_obj.id
                    self.donation.subscription.recurring_amount = formatDonationAmountFromGateway(self.subscription_obj['items']['data'][0]['price']['unit_amount_decimal'], self.donation.currency)
                    self.donation.subscription.currency = self.donation.currency
                    self.donation.subscription.recurring_status = STATUS_ACTIVE
                    self.donation.subscription.save()

                    # set donation payment_status to complete(as this event may be faster than checkout.session.completed, for the email is sent next line)
                    self.donation.payment_status = STATUS_COMPLETE
                    self.donation.save()

                    # send the new recurring notifs to admins and donor as subscription is just active
                    sendNewRecurringNotifToAdmins(self.donation.subscription)
                    sendNewRecurringNotifToDonor(self.donation.subscription)

                elif self.donation.subscription.recurring_status == STATUS_PAYMENT_FAILED:
                    self.donation.subscription.recurring_status = STATUS_ACTIVE
                    self.donation.subscription.save()

                    # send notif emails to admins and donor as a previously failed payment has now succeeded
                    sendReactivatedPaymentNotifToAdmins(self.donation.subscription)
                    sendReactivatedPaymentNotifToDonor(self.donation.subscription)

                else:
                    # check if pause_collection is marked_uncollectible
                    if self.subscription_obj['pause_collection'] and self.subscription_obj['pause_collection']['behavior'] == 'mark_uncollectible':
                        self.donation.subscription.recurring_status = STATUS_PAUSED
                    else:
                        self.donation.subscription.recurring_status = STATUS_ACTIVE
                    self.donation.subscription.save()

                # price changes events should goes through the if-else block and returns 200 right here
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)

        # Event: customer.subscription.deleted
        # self.donation is not initialized here, reason refer to Factory_Stripe.initGatewayByVerification
        if self.event['type'] == EVENT_CUSTOMER_SUBSCRIPTION_DELETED and hasattr(self, 'subscription_obj'):
            # only check for the all retries failed scenario if subscription status isn't cancelled (can't simply match status with payment_failed because the live site hasn't been handling invoice.payment_failed events, which sets newstream subscription status to payment_failed)
            # if subscription is cancelled by donor/admin, status has been set to cancelled already
            if self.donation.subscription.recurring_status != STATUS_CANCELLED:
                try:
                    invoice = stripe.Invoice.retrieve(self.subscription_obj["latest_invoice"])
                    # on Stripe dashboard, admins can configure the number of retries for failed invoices (0-3 times) (doc link: https://stripe.com/docs/billing/subscriptions/overview#settings)
                    # so we shouldn't use invoice.attempt_count = {fixed number} as a criteria for checking if cancelled reason is due to failed payments
                    # since we know that when the invoice is still retrying, invoice.next_payment_attempt should be a timestamp
                    # and if invoice is out of retries, invoice.next_payment_attempt should be null
                    # so the criteria should consist of:
                    if invoice.amount_paid == 0 and invoice.next_payment_attempt == None and invoice.auto_advance == False:
                        self.donation.subscription.cancel_reason = SubscriptionInstance.CancelReason.PAYMENTS_FAILED
                    # else case not handled here since this event could be triggered by donor/admin as well
                    # we already saved the reason on Newstream's side if it was cancelled by donor/admin
                except (stripe.error.RateLimitError, stripe.error.InvalidRequestError, stripe.error.AuthenticationError, stripe.error.APIConnectionError, stripe.error.StripeError) as e:
                    raise RuntimeError("Stripe API Error({}): Status({}), Code({}), Param({}), Message({})".format(type(e).__name__, e.http_status, e.code, e.param, e.user_message))
            
            # note that admins can also cancel subscriptions manually at the stripe dashboard
            # set subscription recurring_status to cancelled
            self.donation.subscription.recurring_status = STATUS_CANCELLED
            self.donation.subscription.save()

            # send email notifications here for all cancellation scenarios
            sendRecurringCancelledNotifToAdmins(self.donation.subscription)
            sendRecurringCancelledNotifToDonor(self.donation.subscription)

            return HttpResponse(status=200)

        # for other events:
        return HttpResponse(status=400)

    def update_recurring_payment(self, form_data):
        if not self.subscription:
            raise ValueError(_('SubscriptionInstance object is None. Cannot update recurring payment.'))
        initStripeApiKey()
        # update donation amount if it is different from database
        if form_data['recurring_amount'] != self.subscription.recurring_amount:
            # ad-hoc price is used
            amount_str = formatDonationAmount(
                form_data['recurring_amount'], self.subscription.currency)
            adhoc_price = {
                'unit_amount_decimal': amount_str,
                'currency': self.subscription.currency.lower(),
                'product': self.settings.product_id,
                'recurring': {
                    'interval': 'month',
                    'interval_count': 1
                }
            }
            # call stripe api to get the SubscriptionItem
            try:
                stripeRes = stripe.SubscriptionItem.list(
                    subscription=self.subscription.profile_id,
                )
            except (stripe.error.RateLimitError, stripe.error.InvalidRequestError, stripe.error.AuthenticationError, stripe.error.APIConnectionError, stripe.error.StripeError) as e:
                raise RuntimeError("Stripe API Error({}): Status({}), Code({}), Param({}), Message({})".format(type(e).__name__, e.http_status, e.code, e.param, e.user_message))
            if len(stripeRes['data']) == 1:
                subItemId = stripeRes['data'][0].id
                # call stripe api to update SubscriptionItem
                try:
                    updateRes = stripe.SubscriptionItem.modify(
                        subItemId,
                        proration_behavior='none',
                        price_data=adhoc_price,
                        quantity=1
                    )
                except (stripe.error.RateLimitError, stripe.error.InvalidRequestError, stripe.error.AuthenticationError, stripe.error.APIConnectionError, stripe.error.StripeError) as e:
                    raise RuntimeError("Stripe API Error({}): Status({}), Code({}), Param({}), Message({})".format(type(e).__name__, e.http_status, e.code, e.param, e.user_message))
                # update newstream model
                if updateRes:
                    self.subscription.recurring_amount = formatDonationAmountFromGateway(updateRes['price']['unit_amount_decimal'], self.subscription.currency)
                    self.subscription.save()

                    # email notifications
                    sendRecurringAdjustedNotifToAdmins(self.subscription)
                    sendRecurringAdjustedNotifToDonor(self.subscription)

                    messages.add_message(self.request, messages.SUCCESS, _(
                        'Your recurring donation amount at Stripe is updated successfully.'))
                else:
                    raise RuntimeError(_('Cannot update stripe subscription. Stripe API returned none.'))
            else:
                raise RuntimeError(_('Cannot update stripe subscription. SubscriptionItem more or less than 1.'))

        # update billing_cycle_anchor if user checked yes
        if form_data['billing_cycle_now']:
            try:
                updateRes = stripe.Subscription.modify(
                    self.subscription.profile_id,
                    proration_behavior='none',
                    billing_cycle_anchor='now',
                )
            except (stripe.error.RateLimitError, stripe.error.InvalidRequestError, stripe.error.AuthenticationError, stripe.error.APIConnectionError, stripe.error.StripeError) as e:
                raise RuntimeError("Stripe API Error({}): Status({}), Code({}), Param({}), Message({})".format(type(e).__name__, e.http_status, e.code, e.param, e.user_message))
            if updateRes:
                # email notifications
                sendRecurringRescheduledNotifToAdmins(self.subscription)
                sendRecurringRescheduledNotifToDonor(self.subscription)

                messages.add_message(self.request, messages.SUCCESS, _(
                    'Your recurring donation via Stripe is set to bill on today\'s date every month.'))
            else:
                raise RuntimeError(_('Cannot update stripe subscription. Stripe API returned none.'))

    def cancel_recurring_payment(self, reason=None):
        if not self.subscription:
            raise ValueError(_('SubscriptionInstance object is None. Cannot cancel recurring payment.'))
        initStripeApiKey()
        # cancel subscription via stripe API
        try:
            cancelled_subscription = stripe.Subscription.delete(
                self.subscription.profile_id)
        except (stripe.error.RateLimitError, stripe.error.InvalidRequestError, stripe.error.AuthenticationError, stripe.error.APIConnectionError, stripe.error.StripeError) as e:
            raise RuntimeError("Stripe API Error({}): Status({}), Code({}), Param({}), Message({})".format(type(e).__name__, e.http_status, e.code, e.param, e.user_message))
        if cancelled_subscription and cancelled_subscription.status == 'canceled':
            # update newstream model
            self.subscription.recurring_status = STATUS_CANCELLED
            self.subscription.cancel_reason = reason
            self.subscription.save()
        else:
            raise RuntimeError(_('SubscriptionInstance object returned from stripe having status %(status)s instead of canceled') % {'status': cancelled_subscription.status})

    def toggle_recurring_payment(self):
        initStripeApiKey()
        # pause or resume subscription via stripe API
        toggle_obj = None
        if self.subscription.recurring_status == STATUS_PAUSED:
            toggle_obj = ''
        elif self.subscription.recurring_status == STATUS_ACTIVE:
            toggle_obj = {"behavior": "mark_uncollectible"}
        else:
            raise ValueError(_('SubscriptionInstance object is neither Active or Paused'))
        try:
            updated_subscription = stripe.Subscription.modify(
                self.subscription.profile_id, pause_collection=toggle_obj)
        except (stripe.error.RateLimitError, stripe.error.InvalidRequestError, stripe.error.AuthenticationError, stripe.error.APIConnectionError, stripe.error.StripeError) as e:
            raise RuntimeError("Stripe API Error({}): Status({}), Code({}), Param({}), Message({})".format(type(e).__name__, e.http_status, e.code, e.param, e.user_message))
        if updated_subscription:
            if toggle_obj and updated_subscription['pause_collection']['behavior'] == 'mark_uncollectible':
                # update newstream model
                self.subscription.recurring_status = STATUS_PAUSED
                self.subscription.save()
                # email notifications
                sendRecurringPausedNotifToAdmins(self.subscription)
                sendRecurringPausedNotifToDonor(self.subscription)
                return {
                    'button-text': str(_('Resume Recurring Donation')),
                    'recurring-status': STATUS_PAUSED,
                    'success-message': str(_('Your recurring donation via Stripe is paused.'))
                }
            if toggle_obj == '' and updated_subscription['pause_collection'] == None:
                # update newstream model
                self.subscription.recurring_status = STATUS_ACTIVE
                self.subscription.save()
                # email notifications
                sendRecurringResumedNotifToAdmins(self.subscription)
                sendRecurringResumedNotifToDonor(self.subscription)
                return {
                    'button-text': str(_('Pause Recurring Donation')),
                    'recurring-status': STATUS_ACTIVE,
                    'success-message': str(_('Your recurring donation via Stripe is resumed.'))
                }
        else:
            raise ValueError(_('SubscriptionInstance object returned from stripe does not have valid pause_collection value'))
