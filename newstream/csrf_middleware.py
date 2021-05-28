from django.middleware.csrf import CsrfViewMiddleware
from donations.payment_gateways.setting_classes import get2C2PSettings


# This class is now useless; I moved towards the @csrf_exempt approach at donations.views
class CustomCsrfViewMiddleware(CsrfViewMiddleware):

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.POST.get('merchant_id', False):
            settings_2c2p = get2C2PSettings()
            if request.POST.get('merchant_id', False) == settings_2c2p.merchant_id:
                print("---Incoming response from 2C2P server---")
                # skip default process_view which includes checking of csrf
                return None
        return super().process_view(request, callback, callback_args, callback_kwargs)
