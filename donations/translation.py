from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import DonationForm, DonationMetaField


@register(DonationForm)
class DonationFormTrans(TranslationOptions):
    fields = (
        'donation_footer_text',
    )


@register(DonationMetaField)
class DonationMetaFieldTrans(TranslationOptions):
    fields = (
        'label',
        'help_text',
        'choices',
        'default_value',
    )

