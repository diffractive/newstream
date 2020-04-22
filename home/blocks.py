from wagtail.core.blocks import StructBlock, StreamBlock, RichTextBlock, ChoiceBlock, CharBlock, URLBlock, ListBlock
from wagtail.images.blocks import ImageChooserBlock


class FullWidthImageBlock(StructBlock):
    banner = ImageChooserBlock()

    class Meta:
        icon = 'image'
        label = 'Full-width Image Block'
        admin_text = '{label}: image that extends to fit the screen width'.format(
            label=label)
        template = 'home/blocks/full_width_image.html'


class LinkButtonBlock(StructBlock):
    button_text = CharBlock()
    button_link = URLBlock()
    target_window = ChoiceBlock(choices=[
        ('_blank', 'New Tab'),
        ('_self', 'Same Tab'),
    ])

    class Meta:
        icon = 'link'
        label = 'Link Button'
        template = 'home/blocks/link_button.html'


class HeadingBlock(StructBlock):
    heading_size = ChoiceBlock(choices=[
        ('h1', 'H1'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('h5', 'H5'),
        ('h6', 'H6'),
    ])
    heading_text = CharBlock()

    class Meta:
        icon = 'title'
        template = 'home/blocks/heading_block.html'


class ColumnContentBlock(StreamBlock):
    heading_block = HeadingBlock()
    text_block = RichTextBlock(template="home/blocks/text_block.html")
    buttons_block = ListBlock(
        LinkButtonBlock(), template="home/blocks/link_buttons_list.html")

    class Meta:
        icon = 'form'
        label = 'Column Content'


class ColumnBlock(StructBlock):
    alignment_css = ChoiceBlock(choices=[
        ('column-horz-align-center', 'center'),
        ('column-horz-align-start', 'left'),
        ('column-horz-align-end', 'right'),
    ], label="Horizontal Alignment of Column Content")

    class Meta:
        icon = 'placeholder'


class SingleColumnBlock(ColumnBlock):
    content = ColumnContentBlock()

    class Meta:
        label = 'Single-Column Block'
        template = 'home/blocks/single_column.html'


class TwoColumnBlock(ColumnBlock):
    column_1 = ColumnContentBlock(label="Column 1 Content")
    column_2 = ColumnContentBlock(label="Column 2 Content")

    class Meta:
        label = 'Two-Column Block'
        template = 'home/blocks/two_column.html'


class ThreeColumnBlock(ColumnBlock):
    column_1 = ColumnContentBlock(label="Column 1 Content")
    column_2 = ColumnContentBlock(label="Column 2 Content")
    column_3 = ColumnContentBlock(label="Column 3 Content")

    class Meta:
        label = 'Three-Column Block'
        template = 'home/blocks/three_column.html'


class SectionContentBlock(StreamBlock):
    single_column_row = SingleColumnBlock()
    two_column_row = TwoColumnBlock()
    three_column_row = ThreeColumnBlock()

    class Meta:
        icon = 'form'
        label = 'Section Content'


class FullWidthSectionBlock(StructBlock):
    width_css = ChoiceBlock(choices=[
        ('container-tight', 'tight'),
        ('container', 'standard'),
        ('container-wide', 'wide'),
    ], icon='cog', label='Width of Inner Container')
    content = SectionContentBlock()

    class Meta:
        icon = 'placeholder'
        label = 'Full-width Section'
        admin_text = '{label}: full-width section that can contains many more child blocks'.format(
            label=label)
        template = 'home/blocks/full_width_section.html'
