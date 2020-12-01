import stripe
from decimal import *
from django.conf import settings
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from donations.models import Donation, DonationPaymentMeta, Subscription, SubscriptionPaymentMeta, STATUS_COMPLETE, STATUS_ACTIVE, STATUS_PAUSED, STATUS_CANCELLED, STATUS_PROCESSING
from donations.payment_gateways.gateway_manager import PaymentGatewayManager
from donations.payment_gateways.setting_classes import getStripeSettings
from donations.payment_gateways.stripe.constants import *
from donations.functions import gen_order_id
from donations.email_functions import sendDonationReceiptToDonor, sendDonationNotifToAdmins, sendRenewalReceiptToDonor, sendRenewalNotifToAdmins, sendRecurringUpdatedNotifToDonor, sendRecurringUpdatedNotifToAdmins, sendRecurringPausedNotifToDonor, sendRecurringPausedNotifToAdmins, sendRecurringResumedNotifToDonor, sendRecurringResumedNotifToAdmins, sendRecurringCancelledNotifToDonor, sendRecurringCancelledNotifToAdmins
from newstream.functions import uuid4_str, getSiteName, getSiteSettings, getFullReverseUrl, printvars, raiseObjectNone, _debug
from .functions import initStripeApiKey, formatDonationAmount, formatDonationAmountFromGateway


class Gateway_Stripe(PaymentGatewayManager):

    def __init__(self, request, donation=None, subscription=None, **kwargs):
        '''
        Note that the subscription parameter passed here can be either a newstream model or a stripe subscription object.

        Other stripe objects are to be passed in kwargs, including session, event and invoice
        session: this is the stripe checkout session object, stores also the donation_id in the metadata
        event: this is the stripe event object when stripe webhooks are triggered and emitted to our server
        invoice: this is the stripe invoice object sent to our server when a payment has succeeded or failed
        '''
        super().__init__(request, donation, subscription)
        # set stripe settings object
        self.settings = getStripeSettings(request)
        # saves all remaining kwargs into the manager, e.g. session, event, invoice
        self.__dict__.update(kwargs)

    def redirect_to_gateway_url(self):
        """ Overriding parent implementation as Stripe redirects with js on client browser """

        # save donation id in session for use in later checkout session creation
        self.request.session['donation_id'] = self.donation.id

        return render(self.request, 'donations/redirection_stripe.html', {'publishable_key': self.settings.publishable_key})

    def process_webhook_response(self):
        initStripeApiKey(self.request)
        # Decide what actions to perform on Newstream's side according to the results/events from the Stripe notifications
        # Event: checkout.session.completed
        if self.event['type'] == EVENT_CHECKOUT_SESSION_COMPLETED:
            # Update payment status
            self.donation.payment_status = STATUS_COMPLETE
            self.donation.save()

            # Since for recurring payment, subscription.updated event might lag behind checkout.session.completed
            if not self.donation.is_recurring:
                sendDonationReceiptToDonor(self.request, self.donation)
                sendDonationNotifToAdmins(self.request, self.donation)

            return HttpResponse(status=200)

        # Event: invoice.created (for subscriptions, just return 200 here and do nothing - to signify to Stripe that it can proceed and finalize the invoice)
        # https://stripe.com/docs/billing/subscriptions/webhooks#understand
        if self.event['type'] == EVENT_INVOICE_CREATED and hasattr(self, 'subscription') and hasattr(self, 'invoice'):
            return HttpResponse(status=200)

        # Event: invoice.paid (for subscriptions)
        if self.event['type'] == EVENT_INVOICE_PAID and hasattr(self, 'subscription') and hasattr(self, 'invoice'):
            if self.invoice.status == 'paid':
                # check if subscription has one or more invoices to determine it's a first time or renewal payment
                # self.subscription here is the stripe subscription object
                invoices = stripe.Invoice.list(subscription=self.subscription.id)
                _debug("Stripe: Subscription {} has {} invoices.".format(self.subscription.id, len(invoices['data'])))
                if len(invoices['data']) == 1:
                    dpmeta = DonationPaymentMeta(
                        donation=self.donation, field_key='stripe_invoice_number', field_value=self.invoice.number)
                    dpmeta.save()
                elif len(invoices['data']) > 1:
                    # create a new donation record + then send donation receipt to user
                    # self.donation is the first donation made for a subscription
                    donation = Donation(
                        subscription=self.donation.subscription,
                        order_number=gen_order_id(self.donation.gateway),
                        user=self.donation.user,
                        form=self.donation.form,
                        gateway=self.donation.gateway,
                        is_recurring=True,
                        donation_amount=formatDonationAmountFromGateway(str(self.invoice.amount_paid), self.donation.currency),
                        currency=self.donation.currency,
                        payment_status=STATUS_COMPLETE,
                    )
                    donation.save()

                    dpmeta = DonationPaymentMeta(
                        donation=donation, field_key='stripe_invoice_number', field_value=self.invoice.number)
                    dpmeta.save()

                    # email notifications
                    sendRenewalReceiptToDonor(self.request, donation)
                    sendRenewalNotifToAdmins(self.request, donation)

                return HttpResponse(status=200)

        # Event: customer.subscription.updated
        if self.event['type'] == EVENT_CUSTOMER_SUBSCRIPTION_UPDATED and hasattr(self, 'subscription'):
            # Subscription active after invoice paid
            if self.subscription['status'] == 'active':
                if self.donation.subscription == None:
                    # create new Subscription object
                    subscription = Subscription(
                        object_id=self.subscription.id,
                        user=self.donation.user,
                        gateway=self.donation.gateway,
                        recurring_amount=formatDonationAmountFromGateway(self.subscription['items']['data'][0]['price']['unit_amount_decimal'], self.donation.currency),
                        currency=self.donation.currency,
                        recurring_status=STATUS_ACTIVE,
                    )
                    subscription.save()
                    # link subscription to the donation
                    self.donation.subscription = subscription
                    # set donation payment_status to complete(as this event may be faster than checkout.session.completed)
                    self.donation.payment_status = STATUS_COMPLETE
                    self.donation.save()

                    # send the donation receipt to donor and notification to admins if subscription is just created
                    sendDonationReceiptToDonor(self.request, self.donation)
                    sendDonationNotifToAdmins(self.request, self.donation)
                else:
                    # check if pause_collection is marked_uncollectible
                    if self.subscription['pause_collection'] and self.subscription['pause_collection']['behavior'] == 'mark_uncollectible':
                        self.donation.subscription.recurring_status = STATUS_PAUSED
                    else:
                        self.donation.subscription.recurring_status = STATUS_ACTIVE
                    self.donation.subscription.save()

                # todo: check logic consistency: does it make sense to log down subscription_period even when recurring is paused?
                spmeta = SubscriptionPaymentMeta(
                    subscription=self.donation.subscription, field_key='stripe_subscription_period', field_value=str(self.subscription.current_period_start)+'-'+str(self.subscription.current_period_end))
                spmeta.save()

                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)

        # Event: customer.subscription.deleted
        if self.event['type'] == EVENT_CUSTOMER_SUBSCRIPTION_DELETED and hasattr(self, 'subscription'):
            # update donation recurring_status
            self.donation.subscription.recurring_status = STATUS_CANCELLED
            self.donation.subscription.save()

            return HttpResponse(status=200)
        
        # for other events:
        return HttpResponse(status=400)

    def update_recurring_payment(self, form_data):
        if not self.subscription:
            raise ValueError(_('Subscription object is None. Cannot update recurring payment.'))
        initStripeApiKey(self.request)
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
            stripeRes = stripe.SubscriptionItem.list(
                subscription=self.subscription.object_id,
            )
            if len(stripeRes['data']) == 1:
                subItemId = stripeRes['data'][0].id
                # call stripe api to update SubscriptionItem
                updateRes = stripe.SubscriptionItem.modify(
                    subItemId,
                    proration_behavior='none',
                    price_data=adhoc_price,
                    quantity=1
                )
                # update newstream model
                if updateRes:
                    self.subscription.recurring_amount = formatDonationAmountFromGateway(updateRes['price']['unit_amount_decimal'], self.subscription.currency)
                    self.subscription.save()

                    # email notifications
                    sendRecurringUpdatedNotifToAdmins(self.request, self.subscription, str(
                        _("A Recurring Donation's amount has been updated on your website:")))
                    sendRecurringUpdatedNotifToDonor(self.request, self.subscription, str(
                        _("You have just updated your recurring donation amount.")))

                    messages.add_message(self.request, messages.SUCCESS, _(
                        'Your recurring donation amount at Stripe is updated successfully.'))
                else:
                    raise RuntimeError(_('Cannot update stripe subscription. Stripe API returned none.'))
            else:
                raise RuntimeError(_('Cannot update stripe subscription. SubscriptionItem more or less than 1.'))

        # update billing_cycle_anchor if user checked yes
        if form_data['billing_cycle_now']:
            updateRes = stripe.Subscription.modify(
                self.subscription.object_id,
                proration_behavior='none',
                billing_cycle_anchor='now',
            )
            if updateRes:
                # email notifications
                sendRecurringUpdatedNotifToAdmins(self.request, self.subscription, str(
                    _("A Recurring Donation's billing cycle has been reset to today's date on your website:")))
                sendRecurringUpdatedNotifToDonor(self.request, self.subscription, str(
                    _("You have just reset your recurring donation's billing cycle to today's date.")))

                messages.add_message(self.request, messages.SUCCESS, _(
                    'Your recurring donation at Stripe is set to bill on today\'s date every month.'))
            else:
                raise RuntimeError(_('Cannot update stripe subscription. Stripe API returned none.'))

    def cancel_recurring_payment(self):
        if not self.subscription:
            raise ValueError(_('Subscription object is None. Cannot cancel recurring payment.'))
        initStripeApiKey(self.request)
        # cancel subscription via stripe API
        cancelled_subscription = stripe.Subscription.delete(
            self.subscription.object_id)
        if cancelled_subscription and cancelled_subscription.status == 'canceled':
            # update newstream model
            self.subscription.recurring_status = STATUS_CANCELLED
            self.subscription.save()
            # email notifications
            sendRecurringCancelledNotifToAdmins(
                self.request, self.subscription)
            sendRecurringCancelledNotifToDonor(
                self.request, self.subscription)
        else:
            raise RuntimeError(_('Subscription object returned from stripe having status %(status)s instead of canceled') % {'status': cancelled_subscription.status})

    def toggle_recurring_payment(self):
        initStripeApiKey(self.request)
        # pause or resume subscription via stripe API
        toggle_obj = None
        if self.subscription.recurring_status == STATUS_PAUSED:
            toggle_obj = ''
        elif self.subscription.recurring_status == STATUS_ACTIVE:
            toggle_obj = {"behavior": "mark_uncollectible"}
        else:
            raise ValueError(_('Subscription object is neither Active or Paused'))
        try:
            updated_subscription = stripe.Subscription.modify(
                self.subscription.object_id, pause_collection=toggle_obj)
        except Exception as e:
            raise RuntimeError(_('Cannot update stripe subscription: %(errmsg)s') % {'errmsg': str(e)})
        if updated_subscription:
            if toggle_obj and updated_subscription['pause_collection']['behavior'] == 'mark_uncollectible':
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
            if toggle_obj == '' and updated_subscription['pause_collection'] == None:
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
        else:
            raise ValueError(_('Subscription object returned from stripe does not have valid pause_collection value'))
