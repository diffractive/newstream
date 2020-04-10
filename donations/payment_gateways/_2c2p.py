from donations.payment_gateways.core import PaymentGatewayManager
from donations.functions import get2C2PSettings, getFullReverseUrl, getNextDateFromRecurringInterval, gen_order_prefix_2c2p
from donations.models import DonationMeta, STATUS_COMPLETE, STATUS_FAILED, STATUS_ONGOING, STATUS_NONRECURRING, STATUS_PENDING, STATUS_REVOKED, STATUS_CANCELLED
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
        data['order_id'] = self.donation.order_number
        data['currency'] = self.settings.currency_code
        data['amount'] = self.format_payment_amount(
            self.donation.donation_amount)
        data['result_url_1'] = getFullReverseUrl(
            self.request, 'donations:verify-gateway-response')
        data['user_defined_1'] = str(self.donation.id)

        if self.donation.is_recurring:
            data['payment_description'] = 'Test Recurring Payment'
            data['request_3ds'] = 'Y'
            data['recurring'] = 'Y'
            data['order_prefix'] = gen_order_prefix_2c2p()
            data['recurring_amount'] = self.format_payment_amount(
                self.donation.donation_amount)
            data['allow_accumulate'] = 'N'
            # data['max_accumulate_amount'] = '000000020000'
            # todo: to be changed to monthly here, need a mechanism to ensure card is charged exactly monthly
            data['recurring_interval'] = 1
            # todo: to be changed to 0 for endless loop until cancel
            data['recurring_count'] = 10
            # todo: to be changed to monthly here, need a mechanism to ensure card is charged exactly monthly
            # todo: create a simple
            data['charge_next_date'] = getNextDateFromRecurringInterval(
                data['recurring_interval'], '%d%m%Y')
            data['charge_on_date'] = ''
            data['payment_option'] = 'A'
        else:
            # todo: payment description need backend input
            data['payment_description'] = 'Test Onetime Payment'

        params = ''
        for key in self.getRequestParamOrder():
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
            if self.request.path.find('thank-you') == -1:
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
        # 2c2p amount param has to be formatted into 12 digit format with leading zero.
        formatted = "{:0>12}".format(new_amount)
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
