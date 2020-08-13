from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import EmailTemplate


@register(EmailTemplate)
class EmailTemplateTrans(TranslationOptions):
    fields = (
        'subject',
        'plain_text',
        'html_body'
    )
