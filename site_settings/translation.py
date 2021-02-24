from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import UserMetaField, SiteSettings


@register(SiteSettings)
class SiteSettingsTrans(TranslationOptions):
    fields = (
        'signup_footer_text',
        '_2c2p_frontend_label',
        'paypal_frontend_label',
        'stripe_frontend_label',
        'manual_frontend_label',
        'offline_frontend_label',
        'offline_instructions_text',
        'offline_thankyou_text',
    )


@register(UserMetaField)
class UserMetaFieldTrans(TranslationOptions):
    fields = (
        'label',
        'help_text',
        'choices',
        'default_value',
    )
