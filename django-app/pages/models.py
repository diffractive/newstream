import re
import os
from django.utils.translation import gettext_lazy as _

from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtailmetadata.models import MetadataPageMixin

from pages.blocks import FullWidthImageSectionBlock, FullWidthSectionBlock


class StaticPage(Page):
    """ To be deprecated. HomePage type might later become more generic e.g. GenericPage instead """
    body = StreamField([
        ('raw_html', blocks.RawHTMLBlock()),
        ('full_width_image', FullWidthImageSectionBlock()),
        ('full_width_section', FullWidthSectionBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body', heading=_('Page Body')),
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
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body', heading=_('Page Body')),
    ]

    class Meta:
        verbose_name = _('Home Page')
        verbose_name_plural = _('Home Pages')
