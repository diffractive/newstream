import hmac
import hashlib

from newstream.functions import raiseObjectNone
from donations.models import Donation, Subscription, STATUS_PENDING
from donations.payment_gateways.gateway_factory import PaymentGatewayFactory
from donations.payment_gateways._2c2p.gateway import Gateway_2C2P
from donations.payment_gateways.setting_classes import get2C2PSettings
from .functions import extract_payment_amount, getResponseParamOrder


class Factory_2C2P(PaymentGatewayFactory):
    @staticmethod
    def initGateway(request, donation, subscription, **kwargs):
        return Gateway_2C2P(request, donation, subscription, **kwargs)

    @staticmethod
    def initGatewayByVerification(request):
        settings = get2C2PSettings(request)
        data = {}
        for key in getResponseParamOrder():
            if key in self.request.POST:
                data[key] = self.request.POST[key]
        if 'hash_value' in self.request.POST and self.request.POST['hash_value']:
            hash_value = self.request.POST['hash_value']
            checkHashStr = ''
            for key in getResponseParamOrder():
                if key in data:
                    checkHashStr += data[key]
            checkHash = hmac.new(
                bytes(settings.secret_key, 'utf-8'),
                bytes(checkHashStr, 'utf-8'), hashlib.sha256).hexdigest()
            if hash_value.lower() == checkHash.lower():
                # distinguish between various cases
                # case one: onetime payment response
                if 'user_defined_1' in request.POST and request.POST['user_defined_1'] and 'recurring_unique_id' not in request.POST:
                    try:
                        donation = Donation.objects.get(pk=int(request.POST['user_defined_1']))
                        return Factory_2C2P.initGateway(request, donation, None, {'data': data})
                    except Donation.DoesNotExist:
                        print('Cannot identify donation record from 2C2P request.', flush=True)
                        return None
                # case two: either first time subscription or renewal donation
                elif 'recurring_unique_id' in request.POST and request.POST['recurring_unique_id']:
                    try:
                        subscription = Subscription.objects.get(object_id=int(request.POST['recurring_unique_id']))
                        # subscription object found, indicating this is a renewal request
                        return Factory_2C2P.initGateway(request, None, subscription, {'data': data})
                    except Subscription.DoesNotExist:
                        # Subscription object not created yet, indicating this is the first time subscription
                        try:
                            donation = Donation.objects.get(pk=int(request.POST['user_defined_1']))
                            return Factory_2C2P.initGateway(request, donation, None, {'data': data, 'first_time_subscription': True})
                        except Donation.DoesNotExist:
                            print('Cannot identify donation record from 2C2P request.', flush=True)
                            return None

            print('hash_value does not match with checkHash, cannot verify request from 2C2P.', flush=True)
            return None
        else:
            print('No hash_value in request.POST, cannot verify request from 2C2P.', flush=True)
            return None

    @staticmethod
    def initGatewayByReturn(request):
        # either onetime or recurring, the return request must have 'user_defined_1'
        # initializing gateway with donation record is enough
        if 'user_defined_1' in request.POST and request.POST['user_defined_1']:
            try:
                donation = Donation.objects.get(pk=int(request.POST['user_defined_1']))
                return Factory_2C2P.initGateway(request, donation, None)
            except Donation.DoesNotExist:
                print('Cannot identify donation record from 2C2P request.', flush=True)
                return None
        print('No user_defined_1 in request.POST, cannot initialize gateway from 2C2P request.', flush=True)
        return None
