from django.middleware.csrf import CsrfViewMiddleware
from site_settings.models import Settings2C2P

class CustomCsrfViewMiddleware(CsrfViewMiddleware):

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.POST.get('merchant_id', False):
            settings_2c2p = Settings2C2P.for_site(request.site)
            if request.POST.get('merchant_id', False) == settings_2c2p.merchant_id:
                print("YESY!")
                return None
        return super().process_view(request, callback, callback_args, callback_kwargs)
