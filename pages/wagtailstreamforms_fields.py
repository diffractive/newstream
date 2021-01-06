from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

from wagtail.core import blocks
from wagtailstreamforms.fields import BaseField, register

from newstream.functions import getSiteSettings_from_default_site

@register('recaptcha')
class ReCaptchaField(BaseField):
    field_class = ReCaptchaField
    icon = 'success'
    label = 'ReCAPTCHA field'

    def get_options(self, block_value):
        siteSettings = getSiteSettings_from_default_site()
        options = super().get_options(block_value)
        options.update({
            'required': True,
            'public_key': siteSettings.recaptcha_public_key,
            'private_key': siteSettings.recaptcha_private_key,
            'widget': ReCaptchaV3
        })
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
        ], icon=self.icon, label=self.label)