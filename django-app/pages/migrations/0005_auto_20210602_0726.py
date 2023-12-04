# Generated by Django 3.1.11 on 2021-06-02 07:26

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20210521_0236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='body_en',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='body_id_id',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='body_ms',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='body_tl',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='body_zh_hant',
        ),
        migrations.RemoveField(
            model_name='staticpage',
            name='body_en',
        ),
        migrations.RemoveField(
            model_name='staticpage',
            name='body_id_id',
        ),
        migrations.RemoveField(
            model_name='staticpage',
            name='body_ms',
        ),
        migrations.RemoveField(
            model_name='staticpage',
            name='body_tl',
        ),
        migrations.RemoveField(
            model_name='staticpage',
            name='body_zh_hant',
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='body',
            field=wagtail.fields.StreamField([('raw_html', wagtail.blocks.RawHTMLBlock()), ('full_width_image', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('container-tight', 'tight'), ('container', 'standard'), ('container-wide', 'wide')], icon='cog', label='Width of Inner Container')), ('min_height', wagtail.blocks.IntegerBlock(help_text='Minimum height of this section(pixels)', min_value=0)), ('banner', wagtail.images.blocks.ImageChooserBlock(label='Background Image')), ('text_color', wagtail.blocks.ChoiceBlock(choices=[('text-white', 'White'), ('text-black', 'Black')], label='Text Color of Inner Container')), ('content', wagtail.blocks.StreamBlock([('single_column_row', wagtail.blocks.StructBlock([('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('column-horz-align-center', 'center'), ('column-horz-align-start', 'left'), ('column-horz-align-end', 'right')], label='Horizontal Alignment of Column Content', required=False)), ('content', wagtail.blocks.StreamBlock([('heading_block', wagtail.blocks.StructBlock([('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Heading', required=False)), ('heading_text', wagtail.blocks.CharBlock()), ('heading_anchor_id', wagtail.blocks.CharBlock(label='ID for Anchor Links', required=False))])), ('text_block', wagtail.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock()), ('button_link', wagtail.blocks.CharBlock()), ('target_window', wagtail.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.blocks.StructBlock([('items', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('item_title', wagtail.blocks.CharBlock()), ('item_content', wagtail.blocks.RichTextBlock())]))), ('footer', wagtail.blocks.RichTextBlock(required=False))])), ('pagebreaker_block', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))])), ('resp_video_iframe_block', wagtail.blocks.StructBlock([('iframe_embed', wagtail.blocks.RawHTMLBlock(help_text='Currently only youtube/vimeo embeds can be responsive'))])), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Image', required=False)), ('width_css', wagtail.blocks.TextBlock(label='Css Value for Width attribute', required=False)), ('alt_text', wagtail.blocks.TextBlock(label='Alt Text', required=False))]))]))])), ('two_column_row', wagtail.blocks.StructBlock([('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('column-horz-align-center', 'center'), ('column-horz-align-start', 'left'), ('column-horz-align-end', 'right')], label='Horizontal Alignment of Column Content', required=False)), ('column_1', wagtail.blocks.StreamBlock([('heading_block', wagtail.blocks.StructBlock([('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Heading', required=False)), ('heading_text', wagtail.blocks.CharBlock()), ('heading_anchor_id', wagtail.blocks.CharBlock(label='ID for Anchor Links', required=False))])), ('text_block', wagtail.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock()), ('button_link', wagtail.blocks.CharBlock()), ('target_window', wagtail.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.blocks.StructBlock([('items', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('item_title', wagtail.blocks.CharBlock()), ('item_content', wagtail.blocks.RichTextBlock())]))), ('footer', wagtail.blocks.RichTextBlock(required=False))])), ('pagebreaker_block', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))])), ('resp_video_iframe_block', wagtail.blocks.StructBlock([('iframe_embed', wagtail.blocks.RawHTMLBlock(help_text='Currently only youtube/vimeo embeds can be responsive'))])), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Image', required=False)), ('width_css', wagtail.blocks.TextBlock(label='Css Value for Width attribute', required=False)), ('alt_text', wagtail.blocks.TextBlock(label='Alt Text', required=False))]))], label='Column 1 Content')), ('column_2', wagtail.blocks.StreamBlock([('heading_block', wagtail.blocks.StructBlock([('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Heading', required=False)), ('heading_text', wagtail.blocks.CharBlock()), ('heading_anchor_id', wagtail.blocks.CharBlock(label='ID for Anchor Links', required=False))])), ('text_block', wagtail.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock()), ('button_link', wagtail.blocks.CharBlock()), ('target_window', wagtail.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.blocks.StructBlock([('items', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('item_title', wagtail.blocks.CharBlock()), ('item_content', wagtail.blocks.RichTextBlock())]))), ('footer', wagtail.blocks.RichTextBlock(required=False))])), ('pagebreaker_block', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))])), ('resp_video_iframe_block', wagtail.blocks.StructBlock([('iframe_embed', wagtail.blocks.RawHTMLBlock(help_text='Currently only youtube/vimeo embeds can be responsive'))])), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Image', required=False)), ('width_css', wagtail.blocks.TextBlock(label='Css Value for Width attribute', required=False)), ('alt_text', wagtail.blocks.TextBlock(label='Alt Text', required=False))]))], label='Column 2 Content'))])), ('three_column_row', wagtail.blocks.StructBlock([('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('column-horz-align-center', 'center'), ('column-horz-align-start', 'left'), ('column-horz-align-end', 'right')], label='Horizontal Alignment of Column Content', required=False)), ('column_1', wagtail.blocks.StreamBlock([('heading_block', wagtail.blocks.StructBlock([('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Heading', required=False)), ('heading_text', wagtail.blocks.CharBlock()), ('heading_anchor_id', wagtail.blocks.CharBlock(label='ID for Anchor Links', required=False))])), ('text_block', wagtail.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock()), ('button_link', wagtail.blocks.CharBlock()), ('target_window', wagtail.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.blocks.StructBlock([('items', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('item_title', wagtail.blocks.CharBlock()), ('item_content', wagtail.blocks.RichTextBlock())]))), ('footer', wagtail.blocks.RichTextBlock(required=False))])), ('pagebreaker_block', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))])), ('resp_video_iframe_block', wagtail.blocks.StructBlock([('iframe_embed', wagtail.blocks.RawHTMLBlock(help_text='Currently only youtube/vimeo embeds can be responsive'))])), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Image', required=False)), ('width_css', wagtail.blocks.TextBlock(label='Css Value for Width attribute', required=False)), ('alt_text', wagtail.blocks.TextBlock(label='Alt Text', required=False))]))], label='Column 1 Content')), ('column_2', wagtail.blocks.StreamBlock([('heading_block', wagtail.blocks.StructBlock([('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Heading', required=False)), ('heading_text', wagtail.blocks.CharBlock()), ('heading_anchor_id', wagtail.blocks.CharBlock(label='ID for Anchor Links', required=False))])), ('text_block', wagtail.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock()), ('button_link', wagtail.blocks.CharBlock()), ('target_window', wagtail.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.blocks.StructBlock([('items', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('item_title', wagtail.blocks.CharBlock()), ('item_content', wagtail.blocks.RichTextBlock())]))), ('footer', wagtail.blocks.RichTextBlock(required=False))])), ('pagebreaker_block', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))])), ('resp_video_iframe_block', wagtail.blocks.StructBlock([('iframe_embed', wagtail.blocks.RawHTMLBlock(help_text='Currently only youtube/vimeo embeds can be responsive'))])), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Image', required=False)), ('width_css', wagtail.blocks.TextBlock(label='Css Value for Width attribute', required=False)), ('alt_text', wagtail.blocks.TextBlock(label='Alt Text', required=False))]))], label='Column 2 Content')), ('column_3', wagtail.blocks.StreamBlock([('heading_block', wagtail.blocks.StructBlock([('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Heading', required=False)), ('heading_text', wagtail.blocks.CharBlock()), ('heading_anchor_id', wagtail.blocks.CharBlock(label='ID for Anchor Links', required=False))])), ('text_block', wagtail.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock()), ('button_link', wagtail.blocks.CharBlock()), ('target_window', wagtail.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.blocks.StructBlock([('items', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('item_title', wagtail.blocks.CharBlock()), ('item_content', wagtail.blocks.RichTextBlock())]))), ('footer', wagtail.blocks.RichTextBlock(required=False))])), ('pagebreaker_block', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))])), ('resp_video_iframe_block', wagtail.blocks.StructBlock([('iframe_embed', wagtail.blocks.RawHTMLBlock(help_text='Currently only youtube/vimeo embeds can be responsive'))])), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Image', required=False)), ('width_css', wagtail.blocks.TextBlock(label='Css Value for Width attribute', required=False)), ('alt_text', wagtail.blocks.TextBlock(label='Alt Text', required=False))]))], label='Column 3 Content'))]))], required=False))])), ('full_width_section', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('container-tight', 'tight'), ('container', 'standard'), ('container-wide', 'wide')], icon='cog', label='Width of Inner Container')), ('background_color_css', wagtail.blocks.ChoiceBlock(choices=[('bg-primary', 'Primary Colour'), ('bg-primary-light', 'Primary Light Colour'), ('bg-primary-dark', 'Primary Dark Colour')], icon='view', label='Section Background Colour', required=False)), ('content', wagtail.blocks.StreamBlock([('single_column_row', wagtail.blocks.StructBlock([('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('column-horz-align-center', 'center'), ('column-horz-align-start', 'left'), ('column-horz-align-end', 'right')], label='Horizontal Alignment of Column Content', required=False)), ('content', wagtail.blocks.StreamBlock([('heading_block', wagtail.blocks.StructBlock([('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Heading', required=False)), ('heading_text', wagtail.blocks.CharBlock()), ('heading_anchor_id', wagtail.blocks.CharBlock(label='ID for Anchor Links', required=False))])), ('text_block', wagtail.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock()), ('button_link', wagtail.blocks.CharBlock()), ('target_window', wagtail.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.blocks.StructBlock([('items', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('item_title', wagtail.blocks.CharBlock()), ('item_content', wagtail.blocks.RichTextBlock())]))), ('footer', wagtail.blocks.RichTextBlock(required=False))])), ('pagebreaker_block', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))])), ('resp_video_iframe_block', wagtail.blocks.StructBlock([('iframe_embed', wagtail.blocks.RawHTMLBlock(help_text='Currently only youtube/vimeo embeds can be responsive'))])), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Image', required=False)), ('width_css', wagtail.blocks.TextBlock(label='Css Value for Width attribute', required=False)), ('alt_text', wagtail.blocks.TextBlock(label='Alt Text', required=False))]))]))])), ('two_column_row', wagtail.blocks.StructBlock([('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('column-horz-align-center', 'center'), ('column-horz-align-start', 'left'), ('column-horz-align-end', 'right')], label='Horizontal Alignment of Column Content', required=False)), ('column_1', wagtail.blocks.StreamBlock([('heading_block', wagtail.blocks.StructBlock([('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Heading', required=False)), ('heading_text', wagtail.blocks.CharBlock()), ('heading_anchor_id', wagtail.blocks.CharBlock(label='ID for Anchor Links', required=False))])), ('text_block', wagtail.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock()), ('button_link', wagtail.blocks.CharBlock()), ('target_window', wagtail.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.blocks.StructBlock([('items', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('item_title', wagtail.blocks.CharBlock()), ('item_content', wagtail.blocks.RichTextBlock())]))), ('footer', wagtail.blocks.RichTextBlock(required=False))])), ('pagebreaker_block', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))])), ('resp_video_iframe_block', wagtail.blocks.StructBlock([('iframe_embed', wagtail.blocks.RawHTMLBlock(help_text='Currently only youtube/vimeo embeds can be responsive'))])), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Image', required=False)), ('width_css', wagtail.blocks.TextBlock(label='Css Value for Width attribute', required=False)), ('alt_text', wagtail.blocks.TextBlock(label='Alt Text', required=False))]))], label='Column 1 Content')), ('column_2', wagtail.blocks.StreamBlock([('heading_block', wagtail.blocks.StructBlock([('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Heading', required=False)), ('heading_text', wagtail.blocks.CharBlock()), ('heading_anchor_id', wagtail.blocks.CharBlock(label='ID for Anchor Links', required=False))])), ('text_block', wagtail.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock()), ('button_link', wagtail.blocks.CharBlock()), ('target_window', wagtail.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.blocks.StructBlock([('items', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('item_title', wagtail.blocks.CharBlock()), ('item_content', wagtail.blocks.RichTextBlock())]))), ('footer', wagtail.blocks.RichTextBlock(required=False))])), ('pagebreaker_block', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))])), ('resp_video_iframe_block', wagtail.blocks.StructBlock([('iframe_embed', wagtail.blocks.RawHTMLBlock(help_text='Currently only youtube/vimeo embeds can be responsive'))])), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Image', required=False)), ('width_css', wagtail.blocks.TextBlock(label='Css Value for Width attribute', required=False)), ('alt_text', wagtail.blocks.TextBlock(label='Alt Text', required=False))]))], label='Column 2 Content'))])), ('three_column_row', wagtail.blocks.StructBlock([('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('column-horz-align-center', 'center'), ('column-horz-align-start', 'left'), ('column-horz-align-end', 'right')], label='Horizontal Alignment of Column Content', required=False)), ('column_1', wagtail.blocks.StreamBlock([('heading_block', wagtail.blocks.StructBlock([('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Heading', required=False)), ('heading_text', wagtail.blocks.CharBlock()), ('heading_anchor_id', wagtail.blocks.CharBlock(label='ID for Anchor Links', required=False))])), ('text_block', wagtail.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock()), ('button_link', wagtail.blocks.CharBlock()), ('target_window', wagtail.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.blocks.StructBlock([('items', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('item_title', wagtail.blocks.CharBlock()), ('item_content', wagtail.blocks.RichTextBlock())]))), ('footer', wagtail.blocks.RichTextBlock(required=False))])), ('pagebreaker_block', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))])), ('resp_video_iframe_block', wagtail.blocks.StructBlock([('iframe_embed', wagtail.blocks.RawHTMLBlock(help_text='Currently only youtube/vimeo embeds can be responsive'))])), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Image', required=False)), ('width_css', wagtail.blocks.TextBlock(label='Css Value for Width attribute', required=False)), ('alt_text', wagtail.blocks.TextBlock(label='Alt Text', required=False))]))], label='Column 1 Content')), ('column_2', wagtail.blocks.StreamBlock([('heading_block', wagtail.blocks.StructBlock([('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Heading', required=False)), ('heading_text', wagtail.blocks.CharBlock()), ('heading_anchor_id', wagtail.blocks.CharBlock(label='ID for Anchor Links', required=False))])), ('text_block', wagtail.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock()), ('button_link', wagtail.blocks.CharBlock()), ('target_window', wagtail.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.blocks.StructBlock([('items', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('item_title', wagtail.blocks.CharBlock()), ('item_content', wagtail.blocks.RichTextBlock())]))), ('footer', wagtail.blocks.RichTextBlock(required=False))])), ('pagebreaker_block', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))])), ('resp_video_iframe_block', wagtail.blocks.StructBlock([('iframe_embed', wagtail.blocks.RawHTMLBlock(help_text='Currently only youtube/vimeo embeds can be responsive'))])), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Image', required=False)), ('width_css', wagtail.blocks.TextBlock(label='Css Value for Width attribute', required=False)), ('alt_text', wagtail.blocks.TextBlock(label='Alt Text', required=False))]))], label='Column 2 Content')), ('column_3', wagtail.blocks.StreamBlock([('heading_block', wagtail.blocks.StructBlock([('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')])), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Heading', required=False)), ('heading_text', wagtail.blocks.CharBlock()), ('heading_anchor_id', wagtail.blocks.CharBlock(label='ID for Anchor Links', required=False))])), ('text_block', wagtail.blocks.RichTextBlock(label='Text', template='pages/blocks/text_block.html')), ('buttons_block', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock()), ('button_link', wagtail.blocks.CharBlock()), ('target_window', wagtail.blocks.ChoiceBlock(choices=[('_blank', 'New Tab'), ('_self', 'Same Tab')]))]), label='Action Buttons', template='pages/blocks/link_buttons_list.html')), ('html_block', wagtail.blocks.RawHTMLBlock(label='HTML', template='pages/blocks/raw_html.html')), ('accordion_block', wagtail.blocks.StructBlock([('items', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('item_title', wagtail.blocks.CharBlock()), ('item_content', wagtail.blocks.RichTextBlock())]))), ('footer', wagtail.blocks.RichTextBlock(required=False))])), ('pagebreaker_block', wagtail.blocks.StructBlock([('width_css', wagtail.blocks.ChoiceBlock(choices=[('w-1/4', '25%'), ('w-1/2', '50%'), ('w-3/4', '75%'), ('w-full', '100%')]))])), ('resp_video_iframe_block', wagtail.blocks.StructBlock([('iframe_embed', wagtail.blocks.RawHTMLBlock(help_text='Currently only youtube/vimeo embeds can be responsive'))])), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alignment_css', wagtail.blocks.ChoiceBlock(choices=[('justify-center', 'center'), ('justify-start', 'left'), ('justify-end', 'right')], label='Horizontal Alignment of Image', required=False)), ('width_css', wagtail.blocks.TextBlock(label='Css Value for Width attribute', required=False)), ('alt_text', wagtail.blocks.TextBlock(label='Alt Text', required=False))]))], label='Column 3 Content'))]))]))]))]),
        ),
    ]
