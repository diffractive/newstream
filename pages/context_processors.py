from django.core.exceptions import MultipleObjectsReturned

from wagtail.core.models import Page

from newstream.functions import getSiteSettings


def homepage(request):
    try:
        siteSettings = getSiteSettings(request)
        homepage = request.site.root_page
        # candidates = TranslatablePage.objects.live().specific().child_of(
        #     root_page).filter(content_type__model='homepage')
        # homepage = candidates.filter(language__code=language).get()
        return {
            'homepage': homepage,
            'privacy_policy_link': siteSettings.privacy_policy_link
        }
    except MultipleObjectsReturned as e:
        print(e, flush=True)
        return {
            'homepage': None
        }
