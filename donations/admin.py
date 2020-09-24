from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from wagtail.contrib.modeladmin.views import InspectView

from newstream.functions import raiseObjectNone
from .models import Donation, Subscription, DonationForm, DonationMeta, DonationPaymentMeta
from .payment_gateways._2c2p.gateway import Gateway_2C2P


class DonationInspectView(InspectView):
    def get_context_data(self, **kwargs):
        model = self.instance
        if not model:
            raiseObjectNone(
                _('No reference to Donation instance in overridden DonationInspectView'))

        # 2C2P specific, recurring payment inquiry
        if model.is_recurring:
            metaSet = DonationPaymentMeta.objects.filter(
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


class DonationAdmin(ModelAdmin):
    model = Donation
    menu_label = _('Donations')
    menu_icon = 'pilcrow'
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('donation_amount', 'gateway',
                    'is_recurring', 'payment_status', 'user_column', 'created_at',)
    list_filter = ('is_recurring', 'payment_status', 'created_at',)
    search_fields = ('order_number', 'donation_amount',
                     'payment_status', 'is_recurring', 'created_at',)
    inspect_view_enabled = True
    inspect_view_class = DonationInspectView

    def user_column(self, obj):
        return obj.user.email if obj.user else '-'

    user_column.admin_order_field = 'user'  # Allows column order sorting
    user_column.short_description = _('User Email')  # Renames column head


class SubscriptionAdmin(ModelAdmin):
    model = Subscription
    menu_label = _('Subscriptions')
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('recurring_amount', 'gateway',
                    'recurring_status', 'user_column', 'created_at',)
    list_filter = ('recurring_status', 'created_at',)
    search_fields = ('object_id', 'recurring_amount',
                     'recurring_status', 'created_at',)
    inspect_view_enabled = True

    def user_column(self, obj):
        return obj.user.email if obj.user else '-'

    user_column.admin_order_field = 'user'  # Allows column order sorting
    user_column.short_description = _('User Email')  # Renames column head


class DonationFormAdmin(ModelAdmin):
    model = DonationForm
    menu_label = _('Donation Forms')
    menu_icon = 'pilcrow'
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'description')
    search_fields = ('title', 'description')


class DonationGroup(ModelAdminGroup):
    menu_label = _('Donations')
    menu_icon = 'folder-open-inverse'
    menu_order = 200
    items = (DonationAdmin, SubscriptionAdmin, DonationFormAdmin)


modeladmin_register(DonationGroup)
