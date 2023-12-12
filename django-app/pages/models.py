import re
import os
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtailmetadata.models import MetadataPageMixin

from pages.blocks import FullWidthImageSectionBlock, FullWidthSectionBlock


class StaticPage(Page):
    """ To be deprecated. HomePage type might later become more generic e.g. GenericPage instead """
    body = StreamField([
        ('raw_html', blocks.RawHTMLBlock()),
        ('full_width_image', FullWidthImageSectionBlock()),
        ('full_width_section', FullWidthSectionBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', heading=_('Page Body')),
    ]

    class Meta:
        verbose_name = _('Static Page')
        verbose_name_plural = _('Static Pages')


class _MetadataPageMixin(MetadataPageMixin):
    def get_meta_url(self):
        return ('https' if os.environ.get('HTTPS') == 'on' else 'http') + '://' + re.sub(r'^(https://|http://)', '', self.full_url)

    class Meta:
        abstract = True


class HomePage(_MetadataPageMixin, Page):
    body = StreamField([
        ('full_width_image', FullWidthImageSectionBlock()),
        ('full_width_section', FullWidthSectionBlock()),
        ('raw_html', blocks.RawHTMLBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', heading=_('Page Body')),
    ]

    class Meta:
        verbose_name = _('Home Page')
        verbose_name_plural = _('Home Pages')
