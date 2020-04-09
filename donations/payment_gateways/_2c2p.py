from donations.payment_gateways.core import PaymentGatewayManager
from donations.functions import get2C2PSettings, getFullReverseUrl
from donations.models import DonationMeta, STATUS_COMPLETE, STATUS_FAILED
from urllib.parse import urlencode
import hmac
import hashlib
from django.shortcuts import render
import logging

log = logging.getLogger()


class Gateway_2C2P(PaymentGatewayManager):

    def __init__(self, request, donation):
        super().__init__(request, donation)
        # set 2c2p settings object
        self.settings = get2C2PSettings(request)

    def base_live_redirect_url(self):
        # todo: to be confirmed
        return 'https://2c2p.com/2C2PFrontEnd/RedirectV3/payment'

    def base_testmode_redirect_url(self):
        return 'https://demo2.2c2p.com/2C2PFrontEnd/RedirectV3/payment'

    def build_redirect_url_params(self):
        pass

    def redirect_to_gateway_url(self):
        """ Overriding parent implementation as 2C2P has to receive a form post from client browser """
        data = {}
        data['version'] = '8.5'
        data['merchant_id'] = self.settings.merchant_id
        # todo: need backend input
        data['payment_description'] = 'Test Onetime Payment'
        data['order_id'] = self.donation.order_number
        data['currency'] = self.settings.currency_code
        print(self.donation.donation_amount, flush=True)
        data['amount'] = self.format_payment_amount(
            self.donation.donation_amount)
        data['result_url_1'] = getFullReverseUrl(
            self.request, 'donations:verify-gateway-response')
        data['user_defined_1'] = str(self.donation.id)

        params = ''
        for key in self.getRequestParamOrder():
            if key in data:
                params += data[key]

        # python 3.6 code
        data['hash_value'] = hmac.new(
            bytes(self.settings.secret_key, 'utf-8'),
            bytes(params, 'utf-8'), hashlib.sha256).hexdigest()

        # append hash_value to donation metas for checking purposes
        dmeta = DonationMeta(
            donation=self.donation, field_key='hash_value', field_value=data['hash_value'])
        dmeta.save()

        return render(self.request, 'donations/onetime_2c2p_form.html', {'action': self.base_gateway_redirect_url, 'data': data})

    def verify_gateway_response(self):
        data = {}
        for key in self.getResponseParamOrder():
            if key in self.request.POST:
                data[key] = self.request.POST[key]
                print(
                    'Donation #{} - Received response {} = {}'.format(self.donation.id, key, data[key]), flush=True)
        hash_value = self.request.POST['hash_value']
        checkHashStr = ''
        for key in self.getResponseParamOrder():
            if key in data:
                checkHashStr += data[key]
        checkHash = hmac.new(
            bytes(self.settings.secret_key, 'utf-8'),
            bytes(checkHashStr, 'utf-8'), hashlib.sha256).hexdigest()
        if hash_value.lower() == checkHash.lower():
            hashCheckResult = True
            # change donation payment_status to complete
            self.donation.payment_status = STATUS_COMPLETE
            self.donation.save()
            # add checkHash to donation metas for checking purposes
            dmeta = DonationMeta(
                donation=self.donation, field_key='checkHash', field_value=checkHash)
            dmeta.save()
        else:
            hashCheckResult = False
            # change donation payment_status to failed
            self.donation.payment_status = STATUS_FAILED
            self.donation.save()
            print('Received hash_value: {}'.format(hash_value), flush=True)
            print('Calculated checkHash: {}'.format(checkHash), flush=True)
        return hashCheckResult

    def format_payment_amount(self, amount):
        decnum = self.getDecimalPlacesFromCurrency(self.settings.currency_code)
        new_amount = str(int(float(amount) * 10**decnum)
                         ) if decnum > 0 else str(int(amount))
        print(new_amount, flush=True)
        # 2c2p amount param has to be formatted into 12 digit format with leading zero.
        formatted = "{:0>12}".format(new_amount)
        print(formatted, flush=True)
        return formatted

    def getDecimalPlacesFromCurrency(self, cc):
        # todo: double check this list
        # 2c2p amount param rule: Minor unit appended to the last digit depending on number of Minor unit specified in ISO 4217.
        # https://en.wikipedia.org/wiki/ISO_4217#Active_codes
        specialCurrencyDecimals = {
            '048': 3,
            '108': 0,
            '990': 4,
            '152': 0,
            '262': 0,
            '324': 0,
            '368': 3,
            '352': 0,
            '400': 3,
            '392': 0,
            '174': 0,
            '410': 0,
            '414': 3,
            '434': 3,
            '512': 3,
            '600': 0,
            '646': 0,
            '788': 3,
            '800': 0,
            '940': 0,
            '927': 4,
            '704': 0,
            '548': 0,
            '950': 0,
            '952': 0,
            '953': 0
        }
        if cc not in specialCurrencyDecimals:
            return 2
        else:
            return specialCurrencyDecimals[cc]

    def getRequestParamOrder(self):
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

    def getResponseParamOrder(self):
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
