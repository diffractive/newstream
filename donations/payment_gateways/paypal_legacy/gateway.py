import re
import pytz
import json
from decimal import *
from datetime import datetime, timezone
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from newstream.functions import _debug, round_half_up
from newstream_user.models import SUBS_ACTION_CANCEL
from donations.models import STATUS_PROCESSING, STATUS_COMPLETE, Donation, Subscription, DonationPaymentMeta
from donations.email_functions import sendRenewalReceiptToDonor, sendRenewalNotifToAdmins, sendRecurringCancelRequestNotifToAdmins
from donations.functions import gen_transaction_id, addUpdateSubsActionLog
from donations.payment_gateways.gateway_manager import PaymentGatewayManager
from donations.payment_gateways.setting_classes import getPayPalLegacySettings
from donations.payment_gateways.paypal_legacy.constants import *


class Gateway_Paypal_Legacy(PaymentGatewayManager):
    def __init__(self, request, donation=None, subscription=None, **kwargs):
        super().__init__(request, donation, subscription)
        # set paypal legacy settings object
        self.settings = getPayPalLegacySettings(request)
        # saves all remaining kwargs into the manager
        self.__dict__.update(kwargs)

    def redirect_to_gateway_url(self):
        pass

    def process_webhook_response(self):
        # copy what process_paypal_subscr_payment does in givewp to here
        # at this stage, Donation(parent) object is already populated from the custom param
        # Subscription object should exist also, since it is linked to Donation either via parent_payment_id
        # update profile_id if it's empty
        if not self.subscription.profile_id:
            self.subscription.profile_id = self.request.POST.get('subscr_id', None)
            self.subscription.save()

        transaction_id_dpm = ''
        try:
            # either it returns a record with empty field_value or not found(which raises the DoesNotExist exception)
            transaction_id_dpm = DonationPaymentMeta.objects.get(donation=self.donation, field_key='_give_payment_transaction_id')
        except DonationPaymentMeta.DoesNotExist as e:
            # will re-add transaction_id_dpm down below
            pass
        # parse 'payment_date' from ipn_data into python date object for comparison
        ipn_payment_date = self.request.POST.get('payment_date', None)
        pac_tz = pytz.timezone('US/Pacific')
        naive_date = re.sub(r'\s(PST|PDT)$', '', ipn_payment_date)
        ipn_payment_datetime = pac_tz.localize(datetime.strptime(naive_date, '%H:%M:%S %b %d, %Y'))
        ipn_payment_datetime_utc = ipn_payment_datetime.astimezone(pytz.utc)
        is_today = self.subscription.created_at.date() == ipn_payment_datetime_utc.date()

        # Look to see if payment is same day as sign up and we haven't set the transaction ID on the parent payment yet.
        if is_today and (not transaction_id_dpm or transaction_id_dpm and not transaction_id_dpm.field_value):
            _debug("[paypal legacy recurring] is_today clause")
            # Verify the amount paid.
            initial_amount = round_half_up(self.subscription.recurring_amount, 2)
            paid_amount = round_half_up(self.request.POST.get('mc_gross', None), 2)

            if paid_amount < initial_amount:
                # save DonationPaymentMeta as note of failure, but no need to save parent payment's status to failed
                dpmeta = DonationPaymentMeta(donation=self.donation, field_key='IPN FAILURE', field_value=str(_('Payment failed due to invalid amount in PayPal Recurring IPN.')))
                dpmeta.save()

                raise Exception(str(_('Invalid payment amount in IPN subscr_payment response. IPN data: %(data)s') % {'data': json.dumps(self.request.POST.dict())}))

            # This is the very first payment so set the transaction ID.
            if transaction_id_dpm:
                transaction_id_dpm.field_value = self.request.POST.get('txn_id', '')
            else:
                transaction_id_dpm = DonationPaymentMeta(donation=self.donation, field_key='_give_payment_transaction_id', field_value=self.request.POST.get('txn_id', ''))
            transaction_id_dpm.save()

            return HttpResponse(status=200)

        # Is this payment already recorded?
        try:
            transaction_id_dpm = DonationPaymentMeta.objects.get(field_key='_give_payment_transaction_id', field_value=self.request.POST.get('txn_id', ''))
            # Payment already recorded
            _debug("[paypal legacy recurring] payment already recorded")
            return HttpResponse(status=200)
        except DonationPaymentMeta.DoesNotExist as e:
            # continue code execution
            pass

        # commented here as there is no logical need for this
        # verify if mc_currency match with the system defined currency_code
        # if self.request.POST.get('mc_currency', '').lower() != self.global_settings.currency.lower():
            # the currency code is invalid
            # raise Exception(str(_('Invalid currency in IPN response. IPN data: %(data)s') % {'data': json.dumps(self.request.POST.dict())}))

        # add renewal payment to subscription
        # transaction_id uses the txn_id from paypal directly, just for convenience, value is the same as _give_payment_transaction_id in donationPaymentMeta
        renewal = Donation(
            is_test=self.testing_mode,
            subscription=self.donation.subscription,
            transaction_id=self.request.POST.get('txn_id') if self.request.POST.get('txn_id', '') else gen_transaction_id(self.donation.gateway),
            user=self.donation.user,
            form=self.donation.form,
            gateway=self.donation.gateway,
            is_recurring=True,
            donation_amount=round_half_up(self.request.POST.get('mc_gross', None), 2),
            currency=self.donation.currency,
            payment_status=STATUS_COMPLETE,
            donation_date=datetime.now(timezone.utc),
        )
        # save new donation as a record of renewal donation
        renewal.save()

        # email notifications
        sendRenewalReceiptToDonor(self.request, renewal)
        sendRenewalNotifToAdmins(self.request, renewal)

        # also save required DonationPaymentMetas, purchase key is skipped here as it should be saved at the parent payment/subscription
        transaction_id_dpm = DonationPaymentMeta(donation=renewal, field_key='_give_payment_transaction_id', field_value=self.request.POST.get('txn_id', ''))
        transaction_id_dpm.save()
        # skip out the renew method from givewp as we don't do that here
            
        return HttpResponse(status=200)


    def update_recurring_payment(self, form_data):
        pass
        
    def cancel_recurring_payment(self):
        if not self.subscription:
            raise ValueError(_('Subscription object is None. Cannot cancel recurring payment.'))
        # update newstream model
        self.subscription.recurring_status = STATUS_PROCESSING
        self.subscription.save()

        # add to the update actions log
        addUpdateSubsActionLog(self.subscription, SUBS_ACTION_CANCEL, action_notes='Cancellation Request')

        # email notifications
        sendRecurringCancelRequestNotifToAdmins(
            self.request, self.subscription)

        # raise error so that main code goes to failure path
        raise Exception(_('Direct cancellation of subscription is not supported for this gateway. Email has been sent to site admin to take further action. Site admin will manually cancel this subscription.'))