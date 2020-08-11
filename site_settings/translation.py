from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import UserMetaField, SiteSettings


@register(SiteSettings)
class SiteSettingsTrans(TranslationOptions):
    fields = (
        'signup_footer_text',
    )


@register(UserMetaField)
class UserMetaFieldTrans(TranslationOptions):
    fields = (
        'label',
        'help_text',
        'choices',
        'default_value',
    )

