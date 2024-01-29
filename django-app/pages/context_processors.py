from django.core.exceptions import MultipleObjectsReturned

from wagtail.models import Page

from newstream.functions import get_site_settings_from_default_site


def homepage(request):
    try:
        site_settings = get_site_settings_from_default_site()
        homepage = request.site.root_page
        # candidates = TranslatablePage.objects.live().specific().child_of(
        #     root_page).filter(content_type__model='homepage')
        # homepage = candidates.filter(language__code=language).get()
        return {
            'homepage': homepage,
            'privacy_policy_link': site_settings.privacy_policy_link
        }
    except MultipleObjectsReturned as e:
        print(e, flush=True)
        return {
            'homepage': None
        }
