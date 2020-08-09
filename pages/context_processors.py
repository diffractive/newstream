from django.core.exceptions import MultipleObjectsReturned

from wagtailtrans.models import TranslatablePage

from newstream.functions import printvars


def homepage(request):
    try:
        language = request.LANGUAGE_CODE
        root_page = request.site.root_page
        candidates = TranslatablePage.objects.live().specific().child_of(
            root_page).filter(content_type__model='homepage')
        homepage = candidates.filter(language__code=language).get()
        return {
            'homepage': homepage
        }
    except MultipleObjectsReturned as e:
        print(e, flush=True)
        return {
            'homepage': None
        }
