# Generated by Django 3.0.8 on 2020-07-30 07:09

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                  parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([('full_width_image', wagtail.core.blocks.StructBlock([('banner', wagtail.images.blocks.ImageChooserBlock())])), ('full_width_section', wagtail.core.blocks.StructBlock([('width_css', wagtail.core.blocks.ChoiceBlock(choices=[('container-tight', 'tight'), ('container', 'standard'), ('container-wide', 'wide')], icon='cog', label='Width of Inner Container')), ('background_color_css', wagtail.core.blocks.ChoiceBlock(choices=[('bg-primary', 'Primary Colour'), ('bg-primary-light', 'Primary Light Colour'), ('bg-primary-dark', 'Primary Dark Colour')], icon='view', label='Section Background Colour', required=False)), ('content', wagtail.core.blocks.StreamBlock([('single_column_row', wagtail.core.blocks.StructBlock([('alignment_css', wagtail.core.blocks.ChoiceBlock(choices=[('column-horz-align-center', 'center'), ('column-horz-align-start', 'left'), ('column-horz-align-end', 'right')], label='Horizontal Alignment of Column Content')), ('content', wagtail.core.blocks.StreamBlock([('heading_block', wagtail.core.blocks.StructBlock([('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('heading_text', wagtail.core.blocks.CharBlock())])), ('text_block', wagtail.core.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('button_text', wagtail.core.blocks.CharBlock()), ('button_link', wagtail.core.blocks.URLBlock()), ('target_window', wagtail.core.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.core.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.core.blocks.StructBlock([('items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('item_title', wagtail.core.blocks.CharBlock()), ('item_content', wagtail.core.blocks.RichTextBlock())]))), ('footer', wagtail.core.blocks.RichTextBlock())])), ('pagebreaker_block', wagtail.core.blocks.StructBlock([('width_css', wagtail.core.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))]))]))])), ('two_column_row', wagtail.core.blocks.StructBlock([('alignment_css', wagtail.core.blocks.ChoiceBlock(choices=[('column-horz-align-center', 'center'), ('column-horz-align-start', 'left'), ('column-horz-align-end', 'right')], label='Horizontal Alignment of Column Content')), ('column_1', wagtail.core.blocks.StreamBlock([('heading_block', wagtail.core.blocks.StructBlock([('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('heading_text', wagtail.core.blocks.CharBlock())])), ('text_block', wagtail.core.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('button_text', wagtail.core.blocks.CharBlock()), ('button_link', wagtail.core.blocks.URLBlock()), ('target_window', wagtail.core.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.core.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.core.blocks.StructBlock([('items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('item_title', wagtail.core.blocks.CharBlock()), ('item_content', wagtail.core.blocks.RichTextBlock())]))), ('footer', wagtail.core.blocks.RichTextBlock())])), ('pagebreaker_block', wagtail.core.blocks.StructBlock([('width_css', wagtail.core.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))]))], label='Column 1 Content')), ('column_2', wagtail.core.blocks.StreamBlock([('heading_block', wagtail.core.blocks.StructBlock([('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('heading_text', wagtail.core.blocks.CharBlock())])), ('text_block', wagtail.core.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('button_text', wagtail.core.blocks.CharBlock()), ('button_link', wagtail.core.blocks.URLBlock()), ('target_window', wagtail.core.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.core.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.core.blocks.StructBlock(
                    [('items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('item_title', wagtail.core.blocks.CharBlock()), ('item_content', wagtail.core.blocks.RichTextBlock())]))), ('footer', wagtail.core.blocks.RichTextBlock())])), ('pagebreaker_block', wagtail.core.blocks.StructBlock([('width_css', wagtail.core.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))]))], label='Column 2 Content'))])), ('three_column_row', wagtail.core.blocks.StructBlock([('alignment_css', wagtail.core.blocks.ChoiceBlock(choices=[('column-horz-align-center', 'center'), ('column-horz-align-start', 'left'), ('column-horz-align-end', 'right')], label='Horizontal Alignment of Column Content')), ('column_1', wagtail.core.blocks.StreamBlock([('heading_block', wagtail.core.blocks.StructBlock([('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('heading_text', wagtail.core.blocks.CharBlock())])), ('text_block', wagtail.core.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('button_text', wagtail.core.blocks.CharBlock()), ('button_link', wagtail.core.blocks.URLBlock()), ('target_window', wagtail.core.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.core.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.core.blocks.StructBlock([('items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('item_title', wagtail.core.blocks.CharBlock()), ('item_content', wagtail.core.blocks.RichTextBlock())]))), ('footer', wagtail.core.blocks.RichTextBlock())])), ('pagebreaker_block', wagtail.core.blocks.StructBlock([('width_css', wagtail.core.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))]))], label='Column 1 Content')), ('column_2', wagtail.core.blocks.StreamBlock([('heading_block', wagtail.core.blocks.StructBlock([('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('heading_text', wagtail.core.blocks.CharBlock())])), ('text_block', wagtail.core.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('button_text', wagtail.core.blocks.CharBlock()), ('button_link', wagtail.core.blocks.URLBlock()), ('target_window', wagtail.core.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.core.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.core.blocks.StructBlock([('items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('item_title', wagtail.core.blocks.CharBlock()), ('item_content', wagtail.core.blocks.RichTextBlock())]))), ('footer', wagtail.core.blocks.RichTextBlock())])), ('pagebreaker_block', wagtail.core.blocks.StructBlock([('width_css', wagtail.core.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))]))], label='Column 2 Content')), ('column_3', wagtail.core.blocks.StreamBlock([('heading_block', wagtail.core.blocks.StructBlock([('heading_size', wagtail.core.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('heading_text', wagtail.core.blocks.CharBlock())])), ('text_block', wagtail.core.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('button_text', wagtail.core.blocks.CharBlock()), ('button_link', wagtail.core.blocks.URLBlock()), ('target_window', wagtail.core.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.core.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.core.blocks.StructBlock([('items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('item_title', wagtail.core.blocks.CharBlock()), ('item_content', wagtail.core.blocks.RichTextBlock())]))), ('footer', wagtail.core.blocks.RichTextBlock())])), ('pagebreaker_block', wagtail.core.blocks.StructBlock([('width_css', wagtail.core.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))]))], label='Column 3 Content'))]))]))])), ('raw_html', wagtail.core.blocks.RawHTMLBlock())])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
