from django.middleware.csrf import CsrfViewMiddleware
from site_settings.models import Settings2C2P


class CustomCsrfViewMiddleware(CsrfViewMiddleware):

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.POST.get('merchant_id', False):
            settings_2c2p = Settings2C2P.for_site(request.site)
            if request.POST.get('merchant_id', False) == settings_2c2p.merchant_id:
                print("---Incoming response from 2C2P server---")
                # skip default process_view which includes checking of csrf
                return None
        return super().process_view(request, callback, callback_args, callback_kwargs)
