from django.shortcuts import render
from donations.payment_gateways.core import PaymentGatewayManager
from donations.functions import getGlobalSettings, get2C2PSettings, getNextDateFromRecurringInterval, getRecurringDateNextMonth, gen_order_prefix_2c2p, getCurrencyDictAt, getCurrencyFromCode
from donations.models import DonationMeta, STATUS_COMPLETE, STATUS_FAILED, STATUS_ONGOING, STATUS_NONRECURRING, STATUS_PENDING, STATUS_REVOKED, STATUS_CANCELLED
from omp.functions import raiseObjectNone, getFullReverseUrl
from urllib.parse import urlencode
import hmac
import hashlib
import re

REDIRECT_API_VERSION = '8.5'
RPP_API_VERSION = '2.3'


class Gateway_2C2P(PaymentGatewayManager):

    def __init__(self, request, donation):
        super().__init__(request, donation)
        # set 2c2p settings object
        self.settings = get2C2PSettings(request)

    def base_live_redirect_url(self):
        # todo: 2c2p live redirect api url to be confirmed
        return 'https://2c2p.com/2C2PFrontEnd/RedirectV3/payment'

    def base_testmode_redirect_url(self):
        return 'https://demo2.2c2p.com/2C2PFrontEnd/RedirectV3/payment'

    def build_redirect_url_params(self):
        pass

    def redirect_to_gateway_url(self):
        """ Overriding parent implementation as 2C2P has to receive a form post from client browser """
        data = {}
        data['version'] = REDIRECT_API_VERSION
        data['merchant_id'] = self.settings.merchant_id
        data['order_id'] = self.donation.order_number
        data['currency'] = getCurrencyDictAt(
            self.donation.currency)['code']
        data['amount'] = self.format_payment_amount(
            self.donation.donation_amount)
        # Apr 20 Tested result_url_1/2 working (such that merchant portal no need manual setting) after follow up with 2C2P Sum (an internal 2C2P settings needs to be turned on by them)
        data['result_url_1'] = getFullReverseUrl(
            self.request, 'donations:return-from-gateway')
        data['result_url_2'] = getFullReverseUrl(
            self.request, 'donations:verify-gateway-response')
        data['user_defined_1'] = str(self.donation.id)

        if self.donation.is_recurring:
            data['payment_description'] = 'Recurring Donation for {}'.format(
                self.request.site.site_name)
            data['request_3ds'] = 'Y'
            data['recurring'] = 'Y'
            data['order_prefix'] = gen_order_prefix_2c2p()
            data['recurring_amount'] = self.format_payment_amount(
                self.donation.donation_amount)
            data['allow_accumulate'] = 'N'
            # max accumulate_amount should also be unnecessary if we do not allow it
            # data['max_accumulate_amount'] = '000000020000'
            # recurring_interval should be unnecessary if we charge on specified date each month (charge_on_date)
            # data['recurring_interval'] = 1
            # todo: to be changed to 0 for endless loop until cancel
            data['recurring_count'] = 3
            # charge_next_date is optional if have charge_on_date set
            # data['charge_next_date'] = getNextDateFromRecurringInterval(
            #     data['recurring_interval'], '%d%m%Y')
            # getRecurringDateNextMonth requires the superuser to set the timezone first
            data['charge_on_date'] = getRecurringDateNextMonth('%d%m')
            # data['charge_on_date'] = getNextDateFromRecurringInterval(
            #     1, '%d%m')
            data['payment_option'] = 'A'

            # append order_prefix to donation metas for distinguishment
            dmeta = DonationMeta(
                donation=self.donation, field_key='order_prefix', field_value=data['order_prefix'])
            dmeta.save()
        else:
            data['payment_description'] = 'Onetime Donation for {}'.format(
                self.request.site.site_name)

        params = ''
        for key in Gateway_2C2P.getRequestParamOrder():
            if key in data:
                params += str(data[key])

        # python 3.6 code
        data['hash_value'] = hmac.new(
            bytes(self.settings.secret_key, 'utf-8'),
            bytes(params, 'utf-8'), hashlib.sha256).hexdigest()

        # append hash_value to donation metas for checking purposes
        dmeta = DonationMeta(
            donation=self.donation, field_key='hash_value', field_value=data['hash_value'])
        dmeta.save()

        return render(self.request, 'donations/redirection_2c2p_form.html', {'action': self.base_gateway_redirect_url, 'data': data})

    def verify_gateway_response(self):
        data = {}
        for key in Gateway_2C2P.getResponseParamOrder():
            if key in self.request.POST:
                data[key] = self.request.POST[key]
        hash_value = self.request.POST['hash_value']
        checkHashStr = ''
        for key in Gateway_2C2P.getResponseParamOrder():
            if key in data:
                checkHashStr += data[key]
        checkHash = hmac.new(
            bytes(self.settings.secret_key, 'utf-8'),
            bytes(checkHashStr, 'utf-8'), hashlib.sha256).hexdigest()
        if hash_value.lower() == checkHash.lower():
            hashCheckResult = True
            if self.request.path.find('verify-gateway-response') != -1:
                print("--Incoming from verify-gateway-response--", flush=True)
                # change donation payment_status to 2c2p's payment_status, update recurring_status
                if data['payment_status'] == '000':
                    self.donation.payment_status = STATUS_COMPLETE
                elif data['payment_status'] == '002':
                    self.donation.payment_status = STATUS_REVOKED
                elif data['payment_status'] == '003':
                    self.donation.payment_status = STATUS_CANCELLED
                elif data['payment_status'] == '999':
                    self.donation.payment_status = STATUS_FAILED
                else:
                    self.donation.payment_status = STATUS_PENDING

                if self.donation.is_recurring:
                    self.donation.recurring_status = STATUS_ONGOING
                else:
                    self.donation.recurring_status = STATUS_NONRECURRING
                self.donation.save()
                # add checkHash to donation metas for checking purposes
                dmeta = DonationMeta(
                    donation=self.donation, field_key='checkHash', field_value=checkHash)
                dmeta.save()
                # add recurring_unique_id to donation metas for hooking up future recurring payments
                if 'recurring_unique_id' in data and data['recurring_unique_id'] != '':
                    dmeta = DonationMeta(
                        donation=self.donation, field_key='recurring_unique_id', field_value=data['recurring_unique_id'])
                    dmeta.save()
            elif self.request.path.find('return-from-gateway') != -1:
                print("--Incoming from return-from-gateway--", flush=True)
                # no need to do anything extra when return-from-gateway
            else:
                print("--Incoming from {}".format(self.request.path), flush=True)

            # for logging response purposes
            for key, val in data.items():
                print(
                    'Donation #{} - Received response {} = {}'.format(self.donation.id, key, val), flush=True)
        else:
            hashCheckResult = False
            # change donation payment_status to failed
            self.donation.payment_status = STATUS_FAILED
            self.donation.save()
            print('Received hash_value: {}'.format(hash_value), flush=True)
            print('Calculated checkHash: {}'.format(checkHash), flush=True)
        return hashCheckResult

    def format_payment_amount(self, amount):
        """ when submitting a new payment, use the donation's currency to format the donation amount """
        decnum = getCurrencyDictAt(self.donation.currency)[
            'setting']['number_decimals']
        new_amount = str(int(float(amount) * 10**decnum)
                         ) if decnum > 0 else str(int(amount))
        # 2c2p amount param has to be formatted into 12 digit format with leading zero.
        formatted = "{:0>12}".format(new_amount)
        return formatted

    @staticmethod
    def extract_payment_amount(currency_code, amount):
        """ When extracting payment amount from 2C2P response, use the response's currency data instead of the global currency settings in case that the global currency settings has already been changed """
        result = re.match('0*([1-9][0-9]*)', amount)
        if len(result.groups()) == 1:
            term = result.groups()[0]
        else:
            raiseObjectNone(
                'No valid amount extracted from the amount string in the 2C2P response')
        decPlaces = getCurrencyFromCode(currency_code)[
            'setting']['number_decimals']
        majorAmount = int(term[:-decPlaces])
        minorAmount = float('0.{}'.format(term[-decPlaces:]))
        return majorAmount+minorAmount

    @staticmethod
    def getRequestParamOrder():
        return [
            'version',
            'merchant_id',
            'payment_description',
            'order_id',
            'invoice_no',
            'currency',
            'amount',
            'customer_email',
            'pay_category_id',
            'promotion',
            'user_defined_1',
            'user_defined_2',
            'user_defined_3',
            'user_defined_4',
            'user_defined_5',
            'result_url_1',
            'result_url_2',
            'enable_store_card',
            'stored_card_unique_id',
            'request_3ds',
            'recurring',
            'order_prefix',
            'recurring_amount',
            'allow_accumulate',
            'max_accumulate_amount',
            'recurring_interval',
            'recurring_count',
            'charge_next_date',
            'charge_on_date',
            'payment_option',
            'ipp_interest_type',
            'payment_expiry',
            'default_lang',
            'statement_descriptor',
            'use_storedcard_only',
            'tokenize_without_authorization',
            'product',
            'ipp_period_filter',
            'sub_merchant_list',
            'qr_type',
            'custom_route_id',
            'airline_transaction',
            'airline_passenger_list',
            'address_list',
        ]

    @staticmethod
    def getResponseParamOrder():
        return [
            'version',
            'request_timestamp',
            'merchant_id',
            'order_id',
            'invoice_no',
            'currency',
            'amount',
            'transaction_ref',
            'approval_code',
            'eci',
            'transaction_datetime',
            'payment_channel',
            'payment_status',
            'channel_response_code',
            'channel_response_desc',
            'masked_pan',
            'stored_card_unique_id',
            'backend_invoice',
            'paid_channel',
            'paid_agent',
            'recurring_unique_id',
            'user_defined_1',
            'user_defined_2',
            'user_defined_3',
            'user_defined_4',
            'user_defined_5',
            'browser_info',
            'ippPeriod',
            'ippInterestType',
            'ippInterestRate',
            'ippMerchantAbsorbRate',
            'payment_scheme',
            'process_by',
            'sub_merchant_list',
        ]

    @staticmethod
    def RPPInquiryRequest(ruid):

        return ''
