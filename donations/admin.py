from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Donor, Donation, PaymentGateway, DonationForm

# Register your models here.


class DonorAdmin(ModelAdmin):
    model = Donor
    menu_label = 'Donors'
    menu_icon = 'pilcrow'
    menu_order = 0
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('first_name', 'last_name', 'email',)
    search_fields = ('first_name', 'last_name', 'email',)


class DonationAdmin(ModelAdmin):
    model = Donation
    menu_label = 'Donations'
    menu_icon = 'pilcrow'
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('donation_amount', 'gateway',
                    'donor', 'is_recurring', 'payment_status', 'created_at',)
    list_filter = ('is_recurring', 'payment_status', 'created_at',)
    search_fields = ('order_number', 'donation_amount',
                     'payment_status', 'is_recurring', 'donor', 'created_at',)
    # inspect_view_enabled = True
    # inspect_view_fields = ['order_number']


class PaymentGatewayAdmin(ModelAdmin):
    model = PaymentGateway
    menu_label = 'Payment Gateways'
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title',)
    search_fields = ('title',)


class DonationFormAdmin(ModelAdmin):
    model = DonationForm
    menu_label = 'Donation Forms'
    menu_icon = 'pilcrow'
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'description', 'is_recurring')
    search_fields = ('title', 'description')


class DonationGroup(ModelAdminGroup):
    menu_label = 'Donations'
    menu_icon = 'folder-open-inverse'
    menu_order = 200
    items = (DonorAdmin, DonationAdmin, PaymentGatewayAdmin, DonationFormAdmin)


modeladmin_register(DonationGroup)
