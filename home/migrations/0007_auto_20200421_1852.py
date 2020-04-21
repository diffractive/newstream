# Generated by Django 3.0.5 on 2020-04-21 18:52

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20200421_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField([('full_width_image', wagtail.core.blocks.StructBlock([('banner', wagtail.images.blocks.ImageChooserBlock())])), ('full_width_section', wagtail.core.blocks.StructBlock([('width_css', wagtail.core.blocks.ChoiceBlock(choices=[('container', 'standard'), ('container-wide', 'wide')], icon='cog', label='Width of Inner Container')), ('content', wagtail.core.blocks.StreamBlock([('single_column_block', wagtail.core.blocks.StructBlock([('alignment_css', wagtail.core.blocks.ChoiceBlock(choices=[('flex flex-col items-center', 'center'), ('flex flex-col items-start', 'left'), ('flex flex-col items-end', 'right')], label='Horizontal Alignment of Column Content')), ('content', wagtail.core.blocks.RichTextBlock(blank=True))])), ('two_column_block', wagtail.core.blocks.StructBlock([('alignment_css', wagtail.core.blocks.ChoiceBlock(choices=[('flex flex-col items-center', 'center'), ('flex flex-col items-start', 'left'), ('flex flex-col items-end', 'right')], label='Horizontal Alignment of Column Content')), ('column_1', wagtail.core.blocks.RichTextBlock(blank=True)), ('column_2', wagtail.core.blocks.RichTextBlock(blank=True))])), ('three_column_block', wagtail.core.blocks.StructBlock([('alignment_css', wagtail.core.blocks.ChoiceBlock(choices=[('flex flex-col items-center', 'center'), ('flex flex-col items-start', 'left'), ('flex flex-col items-end', 'right')], label='Horizontal Alignment of Column Content')), ('column_1', wagtail.core.blocks.RichTextBlock(blank=True)), ('column_2', wagtail.core.blocks.RichTextBlock(blank=True)), ('column_3', wagtail.core.blocks.RichTextBlock(blank=True))]))]))])), ('raw_html', wagtail.core.blocks.RawHTMLBlock())]),
        ),
    ]
