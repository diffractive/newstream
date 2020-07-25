from django.http import HttpResponse, Http404
from django.middleware.csrf import CsrfViewMiddleware

from newstream.functions import getSiteSettings


class DisableSocialLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.sociallogin_urls = [
            '/accounts/social/signup/',
            '/accounts/social/login/cancelled/',
            '/accounts/social/login/error/',
            '/accounts/social/connections/',
            '/accounts/google/login/',
            '/accounts/facebook/login/',
            '/accounts/twitter/login/',
        ]
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        siteSettings = getSiteSettings(request)
        print(request.path_info, flush=True)
        if not siteSettings.social_login_enabled:
            # return 404 for social login urls
            if request.path_info in self.sociallogin_urls:
                # todo: render nicer 404 templates
                print('Dropped in sociallogin_urls', flush=True)
                return HttpResponse('Page not found', status=404)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
