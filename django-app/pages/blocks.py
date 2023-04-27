from django.utils.translation import gettext_lazy as _

from wagtail.core.blocks import StructBlock, StreamBlock, RichTextBlock, ChoiceBlock, IntegerBlock, CharBlock, RawHTMLBlock, URLBlock, ListBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock


class LinkButtonBlock(StructBlock):
    button_text = CharBlock()
    button_link = CharBlock()
    target_window = ChoiceBlock(choices=[
        ('_blank', _('New Tab')),
        ('_self', _('Same Tab')),
    ])

    class Meta:
        icon = 'link'
        label = _('Link Button')
        template = 'pages/blocks/link_button.html'


class HeadingBlock(StructBlock):
    heading_size = ChoiceBlock(choices=[
        ('h1', 'H1'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('h5', 'H5'),
        ('h6', 'H6'),
    ])
    alignment_css = ChoiceBlock(choices=[
        ('justify-center', _('center')),
        ('justify-start', _('left')),
        ('justify-end', _('right')),
    ], label=_("Horizontal Alignment of Heading"), required=False)
    heading_text = CharBlock()
    heading_anchor_id = CharBlock(label=_("ID for Anchor Links"), required=False)

    class Meta:
        icon = 'title'
        template = 'pages/blocks/heading_block.html'
        label = _("Heading")


class AccordionItem(StructBlock):
    item_title = CharBlock()
    item_content = RichTextBlock()


class AccordionBlock(StructBlock):
    items = ListBlock(
        AccordionItem())
    footer = RichTextBlock(required=False)

    class Meta:
        icon = 'list-ul'
        template = 'pages/blocks/accordion_block.html'
        label = _('Accordion')


class PageBreaker(StructBlock):
    width_css = ChoiceBlock(choices=[
        ('w-1/4', '25%'),
        ('w-1/2', '50%'),
        ('w-3/4', '75%'),
        ('w-full', '100%'),
    ])

    class Meta:
        icon = "horizontalrule"
        template = 'pages/blocks/page_breaker_block.html'
        label = _('Page Breaker')


class ResponsiveVideoIframeBlock(StructBlock):
    iframe_embed = RawHTMLBlock(
        help_text=_('Currently only youtube/vimeo embeds can be responsive'))

    class Meta:
        icon = "media"
        template = 'pages/blocks/responsive_video_iframe_block.html'
        label = _('Responsive Video iFrame')


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    alignment_css = ChoiceBlock(choices=[
        ('justify-center', _('center')),
        ('justify-start', _('left')),
        ('justify-end', _('right')),
    ], label=_("Horizontal Alignment of Image"), required=False)
    width_css = TextBlock(required=False, label=_("Css Value for Width attribute"))
    alt_text = TextBlock(required=False, label=_("Alt Text"))

    class Meta:
        icon = 'image'
        label = _('Image Block')
        template = 'pages/blocks/image_block.html'


class ColumnContentBlock(StreamBlock):
    heading_block = HeadingBlock()
    text_block = RichTextBlock(
        template="pages/blocks/text_block.html", label=_("Text"))
    buttons_block = ListBlock(
        LinkButtonBlock(), template="pages/blocks/link_buttons_list.html", label=_("Action Buttons"))
    html_block = RawHTMLBlock(
        template="pages/blocks/raw_html.html", label="HTML")
    accordion_block = AccordionBlock()
    pagebreaker_block = PageBreaker()
    resp_video_iframe_block = ResponsiveVideoIframeBlock()
    image_block = ImageBlock()

    class Meta:
        icon = 'form'
        label = _('Column Content')


class ColumnBlock(StructBlock):
    alignment_css = ChoiceBlock(choices=[
        ('column-horz-align-center', _('center')),
        ('column-horz-align-start', _('left')),
        ('column-horz-align-end', _('right')),
    ], label=_("Horizontal Alignment of Column Content"), required=False)

    class Meta:
        icon = 'placeholder'


class SingleColumnBlock(ColumnBlock):
    content = ColumnContentBlock()

    class Meta:
        label = _('Single-Column Block')
        template = 'pages/blocks/single_column.html'


class TwoColumnBlock(ColumnBlock):
    column_1 = ColumnContentBlock(label=_("Column 1 Content"))
    column_2 = ColumnContentBlock(label=_("Column 2 Content"))

    class Meta:
        label = _('Two-Column Block')
        template = 'pages/blocks/two_column.html'


class ThreeColumnBlock(ColumnBlock):
    column_1 = ColumnContentBlock(label=_("Column 1 Content"))
    column_2 = ColumnContentBlock(label=_("Column 2 Content"))
    column_3 = ColumnContentBlock(label=_("Column 3 Content"))

    class Meta:
        label = _('Three-Column Block')
        template = 'pages/blocks/three_column.html'


class SectionContentBlock(StreamBlock):
    single_column_row = SingleColumnBlock()
    two_column_row = TwoColumnBlock()
    three_column_row = ThreeColumnBlock()

    class Meta:
        icon = 'form'
        label = _('Section Content')


class FullWidthImageSectionBlock(StructBlock):
    width_css = ChoiceBlock(choices=[
        ('container-tight', _('tight')),
        ('container', _('standard')),
        ('container-wide', _('wide')),
    ], icon='cog', label=_('Width of Inner Container'))
    min_height = IntegerBlock(
        min_value=0, help_text=_('Minimum height of this section(pixels)'))
    banner = ImageChooserBlock(label=_('Background Image'))
    text_color = ChoiceBlock(choices=[
        ('text-white', _('White')),
        ('text-black', _('Black')),
    ], label=_('Text Color of Inner Container'))
    content = SectionContentBlock(required=False)

    class Meta:
        icon = 'image'
        label = _('Full-width Image Block')
        admin_text = _('%(label)s: image that extends to fit the screen width') % {
            'label': label}
        template = 'pages/blocks/full_width_image.html'


class FullWidthSectionBlock(StructBlock):
    width_css = ChoiceBlock(choices=[
        ('container-tight', _('tight')),
        ('container', _('standard')),
        ('container-wide', _('wide')),
    ], icon='cog', label=_('Width of Inner Container'))
    background_color_css = ChoiceBlock(choices=[
        ('bg-primary', _('Primary Colour')),
        ('bg-primary-light', _('Primary Light Colour')),
        ('bg-primary-dark', _('Primary Dark Colour')),
    ], icon='view', label=_('Section Background Colour'), required=False)
    content = SectionContentBlock()

    class Meta:
        icon = 'placeholder'
        label = _('Full-width Section')
        admin_text = _(
            '%(label)s: full-width section that can contains many more child blocks') % {'label': label}
        template = 'pages/blocks/full_width_section.html'
