from django.db import models

from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtailtrans.models import TranslatablePage

from pages.blocks import FullWidthImageSectionBlock, FullWidthSectionBlock


class StaticPage(TranslatablePage):
    body = StreamField([
        ('full_width_image', FullWidthImageSectionBlock()),
        ('full_width_section', FullWidthSectionBlock()),
        ('raw_html', blocks.RawHTMLBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
    show_in_menus_default = True


class HomePage(TranslatablePage):
    body = StreamField([
        ('full_width_image', FullWidthImageSectionBlock()),
        ('full_width_section', FullWidthSectionBlock()),
        ('raw_html', blocks.RawHTMLBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
