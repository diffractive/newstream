import hmac
import hashlib
import os
from datetime import datetime, timezone
from xml.etree import ElementTree as ET
from subprocess import Popen, PIPE
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from newstream.functions import getFullReverseUrl, getSiteName, _debug
from donations.functions import getNextDateFromRecurringInterval, gen_order_prefix_2c2p, getCurrencyDictAt, currencyCodeToKey
from donations.email_functions import sendDonationNotifToAdmins, sendDonationReceiptToDonor, sendDonationRevokedToAdmins, sendDonationRevokedToDonor, sendRecurringAdjustedNotifToAdmins, sendRecurringAdjustedNotifToDonor, sendRecurringRescheduledNotifToAdmins, sendRecurringRescheduledNotifToDonor, sendRenewalNotifToAdmins, sendRenewalReceiptToDonor, sendRecurringCancelledNotifToAdmins, sendRecurringCancelledNotifToDonor
from donations.models import Donation, Subscription, STATUS_COMPLETE, STATUS_ACTIVE, STATUS_CANCELLED, STATUS_REVOKED
from donations.payment_gateways.gateway_manager import PaymentGatewayManager
from donations.payment_gateways.setting_classes import get2C2PSettings
from donations.payment_gateways._2c2p.functions import format_payment_amount, extract_payment_amount, map2C2PPaymentStatus, getRequestParamOrder


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
        return 'https://t.2c2p.com/RedirectV3/payment'

    def base_testmode_redirect_url(self):
        return 'https://demo2.2c2p.com/2C2PFrontEnd/RedirectV3/payment'

    def base_live_paymentaction_url(self):
        return 'https://t.2c2p.com/PaymentActionV2/PaymentAction.aspx'

    def base_testmode_paymentaction_url(self):
        return 'https://demo2.2c2p.com/2C2PFrontend/PaymentActionV2/PaymentAction.aspx'

    def base_gateway_redirect_url(self):
        if not self.testing_mode:
            return self.base_live_redirect_url()
        return self.base_testmode_redirect_url()

    def base_paymentaction_url(self):
        if not self.testing_mode:
            return self.base_live_paymentaction_url()
        return self.base_testmode_paymentaction_url()

    def redirect_to_gateway_url(self):
        """ 
        Overriding parent implementation as 2C2P has to receive a form post from client browser.
        See docs https://developer.2c2p.com/docs/payment-requestresponse-parameters on recurring parameters behavior
        """
        data = {}
        data['version'] = REDIRECT_API_VERSION
        data['merchant_id'] = self.settings.merchant_id
        data['order_id'] = self.donation.transaction_id
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
            data['recurring_count'] = 0
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
            if key in data.keys():
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
            self.donation.donation_date = datetime.now()
            self.donation.save()

            # email notifications
            if self.donation.payment_status == STATUS_REVOKED:
                sendDonationRevokedToDonor(self.request, self.donation)
                sendDonationRevokedToAdmins(self.request, self.donation)
            else:
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
                    is_test=self.testing_mode,
                    profile_id=self.data['recurring_unique_id'],
                    user=self.donation.user,
                    gateway=self.donation.gateway,
                    recurring_amount=extract_payment_amount(self.data['amount'], self.data['currency']),
                    currency=currencyCodeToKey(self.data['currency']),
                    recurring_status=STATUS_ACTIVE,
                    subscribe_date=datetime.now(timezone.utc)
                )
                subscription.save()
                # link subscription to the donation
                self.donation.subscription = subscription
                self.donation.save()

                # send the donation receipt to donor and notification to admins if subscription is just created
                sendDonationReceiptToDonor(self.request, self.donation)
                sendDonationNotifToAdmins(self.request, self.donation)

                return HttpResponse(200)
            else:
                raise ValueError(_("Cannot create subscription object due to donation payment_status: %(status)s") % {'status': self.donation.payment_status})
        # case 3: renewals
        if not self.donation and self.subscription:
            # find the first donation made for this subscription
            fDonation = Donation.objects.filter(subscription=self.subscription).order_by('id').first()
            # Create new donation record from fDonation
            donation = Donation(
                is_test=self.testing_mode,
                subscription=self.subscription,
                transaction_id=self.data['order_id'],
                user=fDonation.user,
                form=fDonation.form,
                gateway=fDonation.gateway,
                is_recurring=True,
                donation_amount=extract_payment_amount(self.data['amount'], self.data['currency']),
                currency=currencyCodeToKey(self.data['currency']),
                payment_status=map2C2PPaymentStatus(self.data['payment_status']),
                donation_date=datetime.now(timezone.utc),
            )
            _debug('Save renewal Donation:'+self.data['order_id'])
            donation.save()
            
            # email notifications
            if donation.payment_status == STATUS_REVOKED:
                sendDonationRevokedToDonor(self.request, donation)
                sendDonationRevokedToAdmins(self.request, donation)
            else:
                sendDonationReceiptToDonor(self.request, donation)
                sendDonationNotifToAdmins(self.request, donation)

            return HttpResponse(200)
        else:
            raise RuntimeError(_("Unable to process_webhook_response after verifying 2C2P request"))

    def update_recurring_payment(self, form_data):
        if not self.subscription:
            raise ValueError(_('Subscription object is None. Cannot update recurring payment.'))
        # init the params to the php-bridge script call
        script_path = os.path.dirname(os.path.realpath(__file__)) + '/php-bridge/payment_action.php'
        command_list = ['php', script_path, 
            '--api_url', self.base_paymentaction_url(),
            '--version', RPP_API_VERSION,
            '--mid', self.settings.merchant_id,
            '--secret', self.settings.secret_key,
            '--ruid', self.subscription.profile_id,
            '--type=U',
            '--status=Y',
            '--amount='+format_payment_amount(form_data['recurring_amount'], self.subscription.currency)
        ]
        inquire_command_list = ['php', script_path, 
            '--api_url', self.base_paymentaction_url(),
            '--version', RPP_API_VERSION,
            '--mid', self.settings.merchant_id,
            '--secret', self.settings.secret_key,
            '--ruid', self.subscription.profile_id,
            '--type=I'
        ]
        # make the call only either if donation amount is changed or billing_today is checked
        if form_data['recurring_amount'] != self.subscription.recurring_amount or form_data['billing_cycle_now']:
            if form_data['billing_cycle_now']:
                command_list.append('--bill_today')
            proc = Popen(command_list, stdout=PIPE, stderr=PIPE)
            output, errors = proc.communicate()
            if errors:
                raise RuntimeError(_('Cannot update 2C2P subscription: %(error)s') % {'error': errors.decode("utf-8")})
            xmlResp = ET.fromstring(output.decode("utf-8"))
            if xmlResp.find('respCode') != None and xmlResp.find('respCode').text == '00':
                # inquire payment record for most update values
                inqproc = Popen(inquire_command_list, stdout=PIPE, stderr=PIPE)
                output, errors = inqproc.communicate()
                if errors:
                    raise RuntimeError(_('Cannot inquire 2C2P subscription: %(error)s') % {'error': errors.decode("utf-8")})
                xmlResp = ET.fromstring(output.decode("utf-8"))
                if xmlResp.find('respCode') != None and xmlResp.find('respCode').text == '00':
                    # construct email wordings and messages
                    if form_data['recurring_amount'] != self.subscription.recurring_amount and form_data['billing_cycle_now']:
                        sendRecurringAdjustedNotifToAdmins(self.request, self.subscription)
                        sendRecurringAdjustedNotifToDonor(self.request, self.subscription)
                        sendRecurringRescheduledNotifToAdmins(self.request, self.subscription)
                        sendRecurringRescheduledNotifToDonor(self.request, self.subscription)
                        message_wordings = _("You have successfully reset your recurring donation's billing cycle to today's date, and updated the recurring donation amount at 2C2P.")
                    elif form_data['recurring_amount'] != self.subscription.recurring_amount:
                        sendRecurringAdjustedNotifToAdmins(self.request, self.subscription)
                        sendRecurringAdjustedNotifToDonor(self.request, self.subscription)
                        message_wordings = _("Your recurring donation amount at 2C2P is updated successfully.")
                    elif form_data['billing_cycle_now']:
                        sendRecurringRescheduledNotifToAdmins(self.request, self.subscription)
                        sendRecurringRescheduledNotifToDonor(self.request, self.subscription)
                        message_wordings = _("Your recurring donation at Stripe is set to bill on today's date every month.")
                    # update newstream record in database
                    if form_data['recurring_amount'] != self.subscription.recurring_amount:
                        self.subscription.recurring_amount = extract_payment_amount(xmlResp.find('amount').text, xmlResp.find('currency').text)
                        self.subscription.save()
                    # add message
                    messages.add_message(self.request, messages.SUCCESS, message_wordings)
                else:
                    raise RuntimeError(_("Cannot successfully inquire 2C2P subscription, ")+("respCode is :"+xmlResp.find('respCode').text if xmlResp.find('respCode') else "output is: "+output.decode('utf-8')))
            else:
                raise RuntimeError(_("Cannot successfully update 2C2P subscription, ")+("respCode is :"+xmlResp.find('respCode').text if xmlResp.find('respCode') else "output is: "+output.decode('utf-8')))
        else:
            messages.add_message(self.request, messages.INFO, _("Nothing is updated."))


    def cancel_recurring_payment(self):
        if not self.subscription:
            raise ValueError(_('Subscription object is None. Cannot cancel recurring payment.'))
        # init the params to the php-bridge script call
        script_path = os.path.dirname(os.path.realpath(__file__)) + '/php-bridge/payment_action.php'
        command_list = ['php', script_path, 
            '--api_url', self.base_paymentaction_url(),
            '--version', RPP_API_VERSION,
            '--mid', self.settings.merchant_id,
            '--secret', self.settings.secret_key,
            '--ruid', self.subscription.profile_id,
            '--type=C'
        ]
        # cancel subscription via 2c2p payment action call
        proc = Popen(command_list, stdout=PIPE, stderr=PIPE)
        output, errors = proc.communicate()
        if errors:
            raise RuntimeError(_('Cannot cancel 2C2P subscription: %(reason)s') % {'reason': errors.decode("utf-8")})
        xmlResp = ET.fromstring(output.decode("utf-8"))
        if xmlResp.find('respCode') != None and xmlResp.find('respCode').text == '00':
            # update newstream model
            self.subscription.recurring_status = STATUS_CANCELLED
            self.subscription.save()
            # email notifications
            sendRecurringCancelledNotifToAdmins(
                self.request, self.subscription)
            sendRecurringCancelledNotifToDonor(
                self.request, self.subscription)
        else:
            raise RuntimeError(_('Cannot cancel 2C2P subscription, ')+("respCode is :"+xmlResp.find('respCode').text if xmlResp.find('respCode') else "output is: "+output.decode('utf-8')))
