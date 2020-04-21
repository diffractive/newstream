from django.db import models

from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from home.blocks import FullWidthImageBlock, FullWidthSectionBlock


class HomePage(Page):
    body = StreamField([
        ('full_width_image', FullWidthImageBlock()),
        ('full_width_section', FullWidthSectionBlock()),
        ('raw_html', blocks.RawHTMLBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
