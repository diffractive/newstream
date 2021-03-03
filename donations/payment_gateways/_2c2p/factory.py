import hmac
import hashlib
from django.utils.translation import gettext_lazy as _

from site_settings.models import GATEWAY_2C2P
from newstream.functions import printvars, _debug
from donations.models import Donation, Subscription
from donations.payment_gateways.gateway_factory import PaymentGatewayFactory
from donations.payment_gateways._2c2p.gateway import Gateway_2C2P
from donations.payment_gateways.setting_classes import get2C2PSettings
from donations.payment_gateways._2c2p.functions import getResponseParamOrder


class Factory_2C2P(PaymentGatewayFactory):
    @staticmethod
    def initGateway(request, donation, subscription, **kwargs):
        return Gateway_2C2P(request, donation, subscription, **kwargs)

    @staticmethod
    def initGatewayByVerification(request):
        settings = get2C2PSettings(request)
        data = {}
        # debugging POST params from 2C2P
        for key, value in request.POST.items():
            _debug(key + ': ' + value)
        for key in getResponseParamOrder():
            if key in request.POST:
                data[key] = request.POST[key]
        if 'hash_value' in request.POST and request.POST['hash_value']:
            hash_value = request.POST['hash_value']
            checkHashStr = ''
            for key in getResponseParamOrder():
                if key in data.keys():
                    checkHashStr += data[key]
            checkHash = hmac.new(
                bytes(settings.secret_key, 'utf-8'),
                bytes(checkHashStr, 'utf-8'), hashlib.sha256).hexdigest()
            if hash_value.lower() == checkHash.lower():
                # distinguish between various cases
                # case one: onetime payment response
                if request.POST['user_defined_1'] and not request.POST['recurring_unique_id']:
                    try:
                        donation = Donation.objects.get(pk=int(request.POST['user_defined_1']))
                        return Factory_2C2P.initGateway(request, donation, None, data=data)
                    except Donation.DoesNotExist:
                        raise ValueError(_('Cannot identify donation record from 2C2P request, id: %(id)s') % {'id': request.POST['user_defined_1']})
                # case two: either first time subscription or renewal donation
                elif request.POST['recurring_unique_id']:
                    try:
                        subscription = Subscription.objects.get(profile_id=str(request.POST['recurring_unique_id']), gateway__title=GATEWAY_2C2P)
                        _debug('--2C2P initGatewayByVerification: subscription found--')
                        # subscription object found, indicating this is a renewal request
                        return Factory_2C2P.initGateway(request, None, subscription, data=data)
                    except Subscription.DoesNotExist:
                        # Subscription object not created yet, indicating this is the first time subscription
                        try:
                            donation = Donation.objects.get(pk=int(request.POST['user_defined_1']))
                            return Factory_2C2P.initGateway(request, donation, None, data=data, first_time_subscription=True)
                        except Donation.DoesNotExist:
                            raise ValueError(_('Cannot identify donation record from 2C2P request, id: %(id)s') % {'id': request.POST['user_defined_1']})
            else:
                _debug("hash_value: "+hash_value)
                _debug("checkHash: "+checkHash)
                printvars(data)
                raise ValueError(_("hash_value does not match with checkHash, cannot verify request from 2C2P."))
        else:
            raise ValueError(_("No hash_value in request.POST, cannot verify request from 2C2P."))

    @staticmethod
    def initGatewayByReturn(request):
        # either onetime or recurring, the return request must have 'user_defined_1'
        # initializing gateway with donation record is enough
        if 'user_defined_1' in request.POST and request.POST['user_defined_1']:
            try:
                donation = Donation.objects.get(pk=int(request.POST['user_defined_1']))
                return Factory_2C2P.initGateway(request, donation, None, data=request.POST)
            except Donation.DoesNotExist:
                raise ValueError(_('Cannot identify donation record from 2C2P request, id: %(id)s') % {'id': request.POST['user_defined_1']})
        else:
            raise ValueError(_('No user_defined_1 in request.POST, cannot initialize gateway from 2C2P request.'))
