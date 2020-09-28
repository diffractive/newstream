import hmac
import hashlib
import re
from decimal import *
from urllib.parse import urlencode
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from newstream.functions import raiseObjectNone, getFullReverseUrl, getSiteName, getSiteSettings
from donations.functions import getNextDateFromRecurringInterval, getRecurringDateNextMonth, gen_order_prefix_2c2p, getCurrencyDictAt, getCurrencyFromCode
from donations.email_functions import sendDonationNotifToAdmins, sendDonationReceiptToDonor, sendRenewalNotifToAdmins, sendRenewalReceiptToDonor
from donations.models import Donation, Subscription, DonationPaymentMeta, STATUS_COMPLETE, STATUS_FAILED, STATUS_ACTIVE, STATUS_PENDING, STATUS_REVOKED, STATUS_CANCELLED
from donations.payment_gateways.gateway_manager import PaymentGatewayManager
from donations.payment_gateways.setting_classes import get2C2PSettings
from .functions import format_payment_amount, extract_payment_amount, map2C2PPaymentStatus, getRequestParamOrder, getResponseParamOrder

REDIRECT_API_VERSION = '8.5'
RPP_API_VERSION = '2.3'


class Gateway_2C2P(PaymentGatewayManager):

    def __init__(self, request, donation=None, subscription=None, **kwargs):
        '''
        Either donation or subscription newstream model is passed to this init.
        If subscription is passed, this indicates the request is a renewal donation.
        For kwargs:
         - data: the request.POST data with only the keys from getResponseParamOrder
         - first_time_subscription: indicates the need to create the subscription newstream object
        '''
        super().__init__(request, donation, subscription)
        # set 2c2p settings object
        self.settings = get2C2PSettings(request)
        # saves all remaining kwargs into the manager
        self.__dict__.update(kwargs)

    def base_live_redirect_url(self):
        # todo: 2c2p live redirect api url to be confirmed
        return 'https://t.2c2p.com/RedirectV3/payment'

    def base_testmode_redirect_url(self):
        return 'https://demo2.2c2p.com/2C2PFrontEnd/RedirectV3/payment'

    def base_gateway_redirect_url(self):
        if not self.testing_mode:
            return self.base_live_redirect_url()
        return self.base_testmode_redirect_url()

    def redirect_to_gateway_url(self):
        """ 
        Overriding parent implementation as 2C2P has to receive a form post from client browser.
        See docs https://developer.2c2p.com/docs/payment-requestresponse-parameters on recurring parameters behavior
        """
        data = {}
        data['version'] = REDIRECT_API_VERSION
        data['merchant_id'] = self.settings.merchant_id
        data['order_id'] = self.donation.order_number
        data['currency'] = getCurrencyDictAt(
            self.donation.currency)['code']
        # Beware: self.donation.donation_amount param is str in type
        data['amount'] = format_payment_amount(
            self.donation.donation_amount, self.donation.currency)
        # Apr 20 Tested result_url_1/2 working (such that merchant portal no need manual setting) after follow up with 2C2P Sum (an internal 2C2P settings needs to be turned on by them)
        # todo: Apr 21 2C2P server is not firing back the request from the new recurring payments (need follow up with Sum again)
        data['result_url_1'] = getFullReverseUrl(
            self.request, 'donations:return-from-2c2p')
        data['result_url_2'] = getFullReverseUrl(
            self.request, 'donations:verify-2c2p-response')
        data['user_defined_1'] = str(self.donation.id)

        if self.donation.is_recurring:
            data['payment_description'] = _('Recurring Donation for %(site)s') % {
                'site': getSiteName(self.request)}
            data['request_3ds'] = 'Y'
            data['recurring'] = 'Y'
            data['order_prefix'] = gen_order_prefix_2c2p()
            data['recurring_amount'] = format_payment_amount(
                self.donation.donation_amount, self.donation.currency)
            data['allow_accumulate'] = 'N'
            # todo: to be changed to 0 for endless loop until cancel
            data['recurring_count'] = 3
            data['payment_option'] = 'A'
            # - daily recurring for testing
            data['recurring_interval'] = 1
            data['charge_next_date'] = getNextDateFromRecurringInterval(
                data['recurring_interval'], '%d%m%Y')
            # - monthly recurring(normal behavior)
            # getRecurringDateNextMonth requires the superuser to set the timezone first
            # data['charge_on_date'] = getRecurringDateNextMonth('%d%m')

            # append order_prefix to donation metas for distinguishment
            # dpmeta = DonationPaymentMeta(
            #     donation=self.donation, field_key='order_prefix', field_value=data['order_prefix'])
            # dpmeta.save()
        else:
            data['payment_description'] = _('Onetime Donation for %(site)s') % {
                'site': getSiteName(self.request)}

        params = ''
        for key in getRequestParamOrder():
            if key in data:
                params += str(data[key])

        # python 3.6 code
        data['hash_value'] = hmac.new(
            bytes(self.settings.secret_key, 'utf-8'),
            bytes(params, 'utf-8'), hashlib.sha256).hexdigest()
            
        return render(self.request, 'donations/redirection_2c2p_form.html', {'action': self.base_gateway_redirect_url(), 'data': data})

    def process_webhook_response(self):
        # case one: donation is passed + not first_time_subscription = onetime donation
        if self.donation and not hasattr(self, 'first_time_subscription'):
            # change donation payment_status to 2c2p's payment_status, update recurring_status
            self.donation.payment_status = map2C2PPaymentStatus(self.data['payment_status'])
            self.donation.save()

            # email notifications
            sendDonationReceiptToDonor(self.request, self.donation)
            sendDonationNotifToAdmins(self.request, self.donation)

            return HttpResponse(status=200)
        # case two: donation is passed + first_time_subscription: true
        if self.donation and self.first_time_subscription:
            # change donation payment_status to 2c2p's payment_status, update recurring_status
            self.donation.payment_status = map2C2PPaymentStatus(self.data['payment_status'])
            self.donation.save()

            if self.donation.payment_status == STATUS_COMPLETE:
                # create new Subscription object
                subscription = Subscription(
                    object_id=data['recurring_unique_id'],
                    user=self.donation.user,
                    gateway=self.donation.gateway,
                    recurring_amount=extract_payment_amount(self.data['amount'], self.data['currency']),
                    currency=self.data['currency'],
                    recurring_status=STATUS_ACTIVE,
                )
                try:
                    subscription.save()
                    # link subscription to the donation
                    self.donation.subscription = subscription
                    self.donation.save()
                except Exception as e:
                    return HttpResponse(500)

                # send the donation receipt to donor and notification to admins if subscription is just created
                sendDonationReceiptToDonor(self.request, self.donation)
                sendDonationNotifToAdmins(self.request, self.donation)

                return HttpResponse(200)
            else:
                print("Cannot create subscription object due to donation payment_status: "+self.donation.payment_status, flush=True)
                return HttpResponse(500)
        # case 3: renewals
        if self.subscription:
            # find the first donation made for this subscription
            try:
                fDonation = Donation.objects.filter(subscription=self.subscription).order_by('id').first()
            except Exception as e:
                print(e, flush=True)
                return HttpResponse(500)
            # Create new donation record from fDonation
            donation = Donation(
                subscription=self.subscription,
                order_number=self.data['order_id'],
                user=fDonation.user,
                form=fDonation.form,
                gateway=fDonation.gateway,
                is_recurring=True,
                donation_amount=extract_payment_amount(self.data['amount'], self.data['currency']),
                currency=self.data['currency'],
                payment_status=map2C2PPaymentStatus(self.data['payment_status']),
            )
            try:
                donation.save()
            except Exception as e:
                # Should rarely happen, but in case some bugs or order id repeats itself
                print(e, flush=True)
                return HttpResponse(500)
            
            # email notifications
            sendRenewalReceiptToDonor(self.request, donation)
            sendRenewalNotifToAdmins(self.request, donation)

            return HttpResponse(200)
        print("Unable to process_webhook_response after verifying 2C2P request", flush=True)
        return HttpResponse(500)

    def update_recurring_payment(self):
        pass

    def cancel_recurring_payment(self):
        pass
