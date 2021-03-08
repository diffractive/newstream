from django.utils.translation import gettext_lazy as _

from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtailstreamforms.blocks import WagtailFormBlock

from pages.blocks import FullWidthImageSectionBlock, FullWidthSectionBlock


class StaticPage(Page):
    body = StreamField([
        ('full_width_image', FullWidthImageSectionBlock()),
        ('full_width_section', FullWidthSectionBlock()),
        ('form', WagtailFormBlock()),
        ('raw_html', blocks.RawHTMLBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body', heading=_('Page Body')),
    ]

    class Meta:
        verbose_name = _('Static Page')
        verbose_name_plural = _('Static Pages')


class HomePage(Page):
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
