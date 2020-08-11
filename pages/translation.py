from .models import StaticPage, HomePage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(StaticPage)
class StaticPageTR(TranslationOptions):
    fields = (
        'body',
    )


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'body',
    )
