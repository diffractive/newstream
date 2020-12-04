import re
from decimal import *

from donations.models import STATUS_COMPLETE, STATUS_REVOKED, STATUS_CANCELLED, STATUS_FAILED, STATUS_PROCESSING
from newstream.functions import raiseObjectNone
from donations.functions import getCurrencyDictAt, getCurrencyFromCode


def format_payment_amount(amount, currency_code):
    """ 
    When submitting a new payment, use the donation's currency to format the donation amount .
    Amount needs to be formatted into 12 digit format with leading zero.
    Minor unit appended to the last digit depending on number of Minor unit specified in ISO 4217. https://developer.2c2p.com/docs/payment-requestresponse-parameters
    """
    currency = getCurrencyDictAt(currency_code)
    decnum = currency['setting']['number_decimals']
    amount_str = str(int(Decimal(amount) * 10**decnum)) if decnum != 0 else str(int(amount))
    formatted = "{:0>12}".format(amount_str)
    return formatted


def extract_payment_amount(amount, currency_code):
    """ When extracting payment amount from 2C2P response, use the response's currency data instead of the global currency settings in case that the global currency settings has already been changed """
    currency = getCurrencyFromCode(currency_code)
    decnum = currency['setting']['number_decimals']
    
    result = re.match('0*([1-9][0-9]*)', amount)
    if len(result.groups()) == 1:
        term = result.groups()[0]
    else:
        raiseObjectNone(
            'No valid amount extracted from the amount string in the 2C2P response')
    majorAmount = int(term[:-decnum])
    minorAmount = Decimal('0.{}'.format(term[-decnum:]))
    return majorAmount+minorAmount


def map2C2PPaymentStatus(payment_status):
    if payment_status == '000':
        return STATUS_COMPLETE
    elif payment_status == '002':
        return STATUS_REVOKED
    elif payment_status == '003':
        return STATUS_CANCELLED
    elif payment_status == '999':
        return STATUS_FAILED
    else:
        return STATUS_PROCESSING


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


def RPPInquiryRequest(ruid):
    return ''