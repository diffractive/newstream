from wagtail.core.blocks import StructBlock, StreamBlock, RichTextBlock, ChoiceBlock
from wagtail.images.blocks import ImageChooserBlock


class FullWidthImageBlock(StructBlock):
    banner = ImageChooserBlock()

    class Meta:
        icon = 'image'
        label = 'Full-width Image Block'
        admin_text = '{label}: image that extends to fit the screen width'.format(
            label=label)
        template = 'home/blocks/full_width_image.html'


class ColumnBlock(StructBlock):
    alignment_css = ChoiceBlock(choices=[
        ('richtext-center', 'center'),
        ('richtext-start', 'left'),
        ('richtext-end', 'right'),
    ], label="Horizontal Alignment of Column Content")

    class Meta:
        icon = 'placeholder'


class SingleColumnBlock(ColumnBlock):
    content = RichTextBlock(blank=True)

    class Meta:
        label = 'Single-Column Block'
        template = 'home/blocks/single_column.html'


class TwoColumnBlock(ColumnBlock):
    column_1 = RichTextBlock(blank=True)
    column_2 = RichTextBlock(blank=True)

    class Meta:
        label = 'Two-Column Block'
        template = 'home/blocks/two_column.html'


class ThreeColumnBlock(ColumnBlock):
    column_1 = RichTextBlock(blank=True)
    column_2 = RichTextBlock(blank=True)
    column_3 = RichTextBlock(blank=True)

    class Meta:
        label = 'Three-Column Block'
        template = 'home/blocks/three_column.html'


class SectionContentBlock(StreamBlock):
    single_column_block = SingleColumnBlock()
    two_column_block = TwoColumnBlock()
    three_column_block = ThreeColumnBlock()

    class Meta:
        icon = 'code'
        label = 'Section Content'


class FullWidthSectionBlock(StructBlock):
    width_css = ChoiceBlock(choices=[
        ('container', 'standard'),
        ('container-wide', 'wide'),
    ], icon='cog', label='Width of Inner Container')
    content = SectionContentBlock()

    class Meta:
        icon = 'form'
        label = 'Full-width Section'
        admin_text = '{label}: full-width section that can contains many more child blocks'.format(
            label=label)
        template = 'home/blocks/full_width_section.html'
