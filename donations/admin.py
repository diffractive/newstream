from .models import Donor, Donation, PaymentGateway, DonationForm, DonationMeta
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from django.contrib import admin
from wagtail.contrib.modeladmin.views import InspectView
from omp.functions import raiseObjectNone
from .payment_gateways._2c2p import Gateway_2C2P


class DonationInspectView(InspectView):
    def get_context_data(self, **kwargs):
        model = self.instance
        if not model:
            raiseObjectNone(
                'No reference to Donation instance in overridden DonationInspectView')

        # 2C2P specific, recurring payment inquiry
        if model.is_recurring:
            metaSet = DonationMeta.objects.filter(
                donation=model, field_key='recurring_unique_id')
            if len(metaSet) == 1:
                ruid = metaSet[0].field_value
                # make RPP Maintenance Request
                response = Gateway_2C2P.RPPInquiryRequest(ruid)
                context = {
                    'rpp_response': response
                }
                context.update(kwargs)
                return super().get_context_data(**context)

        return super().get_context_data(**kwargs)


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
    # todo: format donation amount upon display according the currency_dict
    list_display = ('donation_amount', 'gateway',
                    'donor', 'is_recurring', 'payment_status', 'created_at',)
    list_filter = ('is_recurring', 'payment_status', 'created_at',)
    search_fields = ('order_number', 'donation_amount',
                     'payment_status', 'is_recurring', 'donor', 'created_at',)
    inspect_view_enabled = True
    inspect_view_class = DonationInspectView


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
    list_display = ('title', 'description', 'is_active')
    search_fields = ('title', 'description')


class DonationGroup(ModelAdminGroup):
    menu_label = 'Donations'
    menu_icon = 'folder-open-inverse'
    menu_order = 200
    items = (DonorAdmin, DonationAdmin, PaymentGatewayAdmin, DonationFormAdmin)


modeladmin_register(DonationGroup)
