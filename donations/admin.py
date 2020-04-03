from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import PaymentGateway, DonationForm

# Register your models here.
class PaymentGatewayAdmin(ModelAdmin):
    model = PaymentGateway
    menu_label = 'Payment Gateways'
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)

class DonationFormAdmin(ModelAdmin):
    model = DonationForm
    menu_label = 'Donation Forms'
    menu_icon = 'pilcrow'
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title','description','is_recurring')
    list_filter = ('title','description')
    search_fields = ('title','description')

class DonationGroup(ModelAdminGroup):
    menu_label = 'Donations'
    menu_icon = 'folder-open-inverse'
    menu_order = 200
    items = (PaymentGatewayAdmin, DonationFormAdmin)

modeladmin_register(DonationGroup)
