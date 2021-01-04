from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from wagtail.contrib.modeladmin.views import InspectView, DeleteView
from wagtail.contrib.modeladmin.helpers import ButtonHelper

from newstream.functions import raiseObjectNone, getSiteSettings_from_default_site
from .models import Donation, Subscription, DonationForm, DonationMeta, DonationPaymentMeta, SubscriptionPaymentMeta, STATUS_COMPLETE, STATUS_ACTIVE, STATUS_PAUSED, STATUS_CANCELLED
from newstream_user.models import UserSubscriptionUpdatesLog
from .payment_gateways._2c2p.functions import RPPInquiryRequest


class DonationInspectView(InspectView):
    def get_fields_dict_as_dict(self):
        """
        Return a dictionary of field_name:{`label`/`value`} dictionaries to represent the
        fields named by the model_admin class's `get_inspect_view_fields` method
        """
        fields = {}
        for field_name in self.model_admin.get_inspect_view_fields():
            fields[field_name] = self.get_dict_for_field(field_name)
            if field_name == 'subscription' and self.instance.subscription:
                fields[field_name]['url'] = reverse('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': self.instance.subscription.id})
        return fields

    def get_donor_meta_data(self):
        """
        Return a list of DonationMeta mapped as dictionaries from self.instance
        DonationMeta are supposed to be input by donor in frontend
        """
        metas = []
        metasResult = DonationMeta.objects.filter(donation=self.instance)
        for meta in metasResult:
            metas.append({'key': meta.field_key, 'value': meta.field_value})
        return metas

    def get_system_meta_data(self):
        """
        Return a list of DonationPaymentMeta mapped as dictionaries from self.instance
        DonationPaymentMeta are supposed to be system-generated
        """
        metas = []
        metasResult = DonationPaymentMeta.objects.filter(donation=self.instance)
        for meta in metasResult:
            metas.append({'key': meta.field_key, 'value': meta.field_value})
        return metas
    
    def get_context_data(self, **kwargs):
        context = {
            'fields': self.get_fields_dict_as_dict(),
            'status_complete': STATUS_COMPLETE.capitalize(),
            'dmetas': self.get_donor_meta_data(),
            'smetas': self.get_system_meta_data(),
            'buttons': self.button_helper.get_buttons_for_obj(
                self.instance, exclude=['inspect', 'edit']),
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class SubscriptionInspectView(InspectView):
    def get_fields_dict_as_dict(self):
        """
        Return a dictionary of field_name:{`label`/`value`} dictionaries to represent the
        fields named by the model_admin class's `get_inspect_view_fields` method
        """
        fields = {}
        for field_name in self.model_admin.get_inspect_view_fields():
            fields[field_name] = self.get_dict_for_field(field_name)
        return fields

    def get_meta_data(self):
        """
        Return a list of SubscriptionPaymentMeta mapped as dictionaries from self.instance
        """
        metas = []
        metasResult = SubscriptionPaymentMeta.objects.filter(subscription=self.instance)
        for meta in metasResult:
            metas.append({'key': meta.field_key, 'value': meta.field_value})
        return metas

    def get_renewals(self):
        """
        Return a list of Donation(Renewals) from self.instance
        """
        return Donation.objects.filter(subscription=self.instance, deleted=False)

    def get_action_logs(self):
        """
        Return a list of UserSubscriptionUpdatesLog from self.instance
        """
        return UserSubscriptionUpdatesLog.objects.filter(subscription=self.instance).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = {
            'fields': self.get_fields_dict_as_dict(),
            'status_active': STATUS_ACTIVE.capitalize(),
            'status_paused': STATUS_PAUSED.capitalize(),
            'status_cancelled': STATUS_CANCELLED.capitalize(),
            'metas': self.get_meta_data(),
            'renewals': self.get_renewals(),
            'action_logs': self.get_action_logs(),
            'buttons': self.button_helper.get_buttons_for_obj(
                self.instance, exclude=['inspect', 'edit']),
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class DonationDeleteView(DeleteView):
    def __init__(self, *args, **kwargs):
        self.siteSettings = getSiteSettings_from_default_site()
        super().__init__(*args, **kwargs)

    def delete_instance(self):
        if self.siteSettings.donations_soft_delete_mode:
            self.instance.deleted = True
            self.instance.save()
        else:
            self.instance.delete()

    def confirmation_message(self):
        if self.siteSettings.donations_soft_delete_mode:
            return _(
                "Are you sure you want to soft-delete this %s? If other things in your "
                "site are related to it, they may also be affected. "
                "(Record will still persist in the database)"
            ) % self.verbose_name
        else:
            return super().confirmation_message()


class SubscriptionDeleteView(DeleteView):
    def __init__(self, *args, **kwargs):
        self.siteSettings = getSiteSettings_from_default_site()
        super().__init__(*args, **kwargs)
    
    def delete_instance(self):
        if self.siteSettings.donations_soft_delete_mode:
            self.instance.deleted = True
            self.instance.save()
        else:
            self.instance.delete()

    def confirmation_message(self):
        if self.siteSettings.donations_soft_delete_mode:
            return _(
                "Are you sure you want to soft-delete this %s? If other things in your "
                "site are related to it, they may also be affected. "
                "(Record will still persist in the database)"
            ) % self.verbose_name
        else:
            return super().confirmation_message()


class SubscriptionButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, obj, exclude=['edit'], classnames_add=None, classnames_exclude=None):
        """
        This function is originally used to gather all available buttons.
        We exclude the edit button to the btns list.
        """
        btns = super().get_buttons_for_obj(
            obj, exclude, classnames_add, classnames_exclude)
        return btns


class DonationButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, obj, exclude=['edit'], classnames_add=None, classnames_exclude=None):
        """
        This function is originally used to gather all available buttons.
        We exclude the edit button to the btns list.
        """
        btns = super().get_buttons_for_obj(
            obj, exclude, classnames_add, classnames_exclude)
        return btns


class DonationAdmin(ModelAdmin):
    model = Donation
    button_helper_class = DonationButtonHelper
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
    inspect_view_extra_css = ['css/admin_inspect.css']
    inspect_view_extra_js = ['js/admin_inspect.js']
    delete_view_class = DonationDeleteView

    def get_queryset(self, request):
        # only show records with deleted=False (which should be valid whether soft-delete is on/off)
        qs = super().get_queryset(request)
        return qs.filter(deleted=False)
    
    def user_column(self, obj):
        return obj.user.email if obj.user else '-'

    user_column.admin_order_field = 'user'  # Allows column order sorting
    user_column.short_description = _('User Email')  # Renames column head


class SubscriptionAdmin(ModelAdmin):
    model = Subscription
    button_helper_class = SubscriptionButtonHelper
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
    inspect_view_class = SubscriptionInspectView
    inspect_view_extra_css = ['css/admin_inspect.css']
    inspect_view_extra_js = ['js/admin_inspect.js']
    delete_view_class = SubscriptionDeleteView

    def user_column(self, obj):
        return obj.user.email if obj.user else '-'

    def get_queryset(self, request):
        # only show records with deleted=False (which should be valid whether soft-delete is on/off)
        qs = super().get_queryset(request)
        return qs.filter(deleted=False)

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
