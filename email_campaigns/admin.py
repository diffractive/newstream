from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from omp.functions import raiseObjectNone
from .models import EmailTemplate, TargetGroup, Campaign
from .custom_classes import SendCampaignMAMixin


class EmailTemplateAdmin(ModelAdmin):
    model = EmailTemplate
    menu_label = 'Email Templates'
    menu_icon = 'pilcrow'
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'subject')
    search_fields = ('title', 'subject', 'plain_text')


class TargetGroupAdmin(ModelAdmin):
    model = TargetGroup
    menu_label = 'Target Groups'
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title',)
    search_fields = ('title',)


class CampaignAdmin(SendCampaignMAMixin, ModelAdmin):
    model = Campaign
    menu_label = 'Campaigns'
    menu_icon = 'pilcrow'
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'template', 'from_address', 'sent', 'sent_at')
    search_fields = ('title',)


class CampaignGroup(ModelAdminGroup):
    menu_label = 'Email Campaigns'
    menu_icon = 'folder-open-inverse'
    menu_order = 300
    items = (EmailTemplateAdmin, TargetGroupAdmin, CampaignAdmin)


modeladmin_register(CampaignGroup)
