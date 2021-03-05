from django.utils.translation import gettext_lazy as _

from donations.models import Donation
from donations.payment_gateways.setting_classes import getPayPalLegacySettings
from donations.payment_gateways.gateway_factory import PaymentGatewayFactory
from donations.payment_gateways.paypal_legacy.gateway import Gateway_Paypal_Legacy
from donations.payment_gateways.paypal_legacy.functions import curlPaypalIPN


class Factory_Paypal_Legacy(PaymentGatewayFactory):
    @staticmethod
    def initGateway(request, donation, subscription, **kwargs):
        return Gateway_Paypal_Legacy(request, donation, subscription, **kwargs)

    @staticmethod
    def initGatewayByVerification(request):
        # Regular PayPal IPN
        # give-listener=IPN param check is done in the nginx config file
        if request.method == 'POST':
            paypalLegacySettings = getPayPalLegacySettings(request)

            raw_post_data = request.body.decode('utf-8')
            req_data = 'cmd=_notify-validate'
            if raw_post_data:
                req_data += '&' + raw_post_data
            curl_ipn_result = curlPaypalIPN(paypalLegacySettings.ipn_url, ['Connection: Close'], req_data)

            if curl_ipn_result == 'VERIFIED':
                # todo: update give_last_paypal_ipn_received meta and insert payment note just like givewp

                donation_id = None
                kwargs = {}

                # get donation_id from renewal ipn's custom param
                if request.POST.get('custom', None):
                    donation_id = request.POST.get('custom')
                else:
                    raise ValueError(_('Missing custom(donation_id) in PayPal\'s incoming renewal IPN'))
                
                try:
                    # pk can be string or int
                    donation = Donation.objects.get(pk=donation_id)
                    return Factory_Paypal_Legacy.initGateway(request, donation, donation.subscription)
                except Donation.DoesNotExist:
                    raise ValueError(_("Donation object not found by id: ")+str(donation_id))
            else:
                raise Exception(_("IPN is not verified by PayPal"))
        else:
            raise Exception(_("Not POST request from PayPal IPN"))

    @staticmethod
    def initGatewayByReturn(request):
        pass
