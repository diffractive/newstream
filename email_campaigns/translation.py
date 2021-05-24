from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from .models import CampaignEmailTemplate


@register(CampaignEmailTemplate)
class CampaignEmailTemplateTrans(TranslationOptions):
    fields = (
        'subject',
        'plain_text',
        'html_body'
    )
