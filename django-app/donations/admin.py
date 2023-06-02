from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from wagtail.contrib.modeladmin.views import InspectView, DeleteView, CreateView
from wagtail.contrib.modeladmin.helpers import ButtonHelper

from newstream.functions import get_site_settings_from_default_site
from site_settings.models import GATEWAY_OFFLINE, GATEWAY_PAYPAL_LEGACY
from donations.models import Donation, Subscription, SubscriptionInstance, DonationForm, DonationMeta, DonationPaymentMeta, SubscriptionPaymentMeta, STATUS_COMPLETE, STATUS_REFUNDED, STATUS_REVOKED, STATUS_FAILED, STATUS_ACTIVE, STATUS_PAUSED, STATUS_CANCELLED, STATUS_PROCESSING, STATUS_INACTIVE, STATUS_PAYMENT_FAILED
from newstream_user.models import UserSubscriptionUpdatesLog, UserDonationUpdatesLog
from donations.payment_gateways import isGatewayEditSubSupported, isGatewayToggleSubSupported, isGatewayCancelSubSupported


class DonationCreateView(CreateView):
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SubscriptionCreateView(CreateView):
    def form_valid(self, form):
        # save parent Subscription object
        subscription = Subscription(
            user=form.instance.user,
            created_by=self.request.user
        )
        subscription.save()
        
        form.instance.parent = subscription
        form.instance.created_by = self.request.user
        return super().form_valid(form)


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
                fields[field_name]['url'] = reverse('donations_subscriptioninstance_modeladmin_inspect', kwargs={'instance_pk': self.instance.subscription.id})
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

    def get_action_logs(self):
        """
        Return a list of UserDonationUpdatesLog from self.instance
        """
        return UserDonationUpdatesLog.objects.filter(donation=self.instance).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = {
            'fields': self.get_fields_dict_as_dict(),
            'donation': self.instance,
            'status_complete': STATUS_COMPLETE,
            'status_processing': STATUS_PROCESSING,
            'status_refunded': STATUS_REFUNDED,
            'status_revoked': STATUS_REVOKED,
            'status_failed': STATUS_FAILED,
            'status_cancelled': STATUS_CANCELLED,
            'dmetas': self.get_donor_meta_data(),
            'smetas': self.get_system_meta_data(),
            'buttons': self.button_helper.get_buttons_for_obj(
                self.instance, exclude=['inspect', 'edit']),
            'action_logs': self.get_action_logs(),
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
        toggle_exclusion = [GATEWAY_OFFLINE, GATEWAY_PAYPAL_LEGACY]
        cancel_exclusion = [GATEWAY_OFFLINE, GATEWAY_PAYPAL_LEGACY]
        context = {
            'fields': self.get_fields_dict_as_dict(),
            'subscription': self.instance,
            'status_active': STATUS_ACTIVE,
            'status_paused': STATUS_PAUSED,
            'status_cancelled': STATUS_CANCELLED,
            'status_processing': STATUS_PROCESSING,
            'status_inactive': STATUS_INACTIVE,
            'status_payment_failed': STATUS_PAYMENT_FAILED,
            'gateway_editsub_supported': isGatewayEditSubSupported(self.instance.gateway),
            'gateway_togglesub_supported': isGatewayToggleSubSupported(self.instance.gateway) and self.instance.gateway.title not in toggle_exclusion,
            'gateway_cancelsub_supported': isGatewayCancelSubSupported(self.instance.gateway) and self.instance.gateway.title not in cancel_exclusion,
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
        self.site_settings = get_site_settings_from_default_site()
        super().__init__(*args, **kwargs)

    def delete_instance(self):
        if self.site_settings.donations_soft_delete_mode:
            self.instance.deleted = True
            self.instance.save()
        else:
            self.instance.delete()

    def confirmation_message(self):
        if self.site_settings.donations_soft_delete_mode:
            return _(
                "Are you sure you want to soft-delete this %s? If other things in your "
                "site are related to it, they may also be affected. "
                "(Record will still persist in the database)"
            ) % self.verbose_name
        else:
            return super().confirmation_message()


class SubscriptionDeleteView(DeleteView):
    def __init__(self, *args, **kwargs):
        self.site_settings = get_site_settings_from_default_site()
        super().__init__(*args, **kwargs)
    
    def delete_instance(self):
        # loop all child instances, if all others are deleted or this is the only instance to be deleted
        # proceed to set parent to deleted as well
        delete_parent = True
        for instance in self.instance.parent.subscription_instances.all():
            if instance.id == self.instance.id:
                continue
            elif not instance.deleted:
                delete_parent = False

        if self.site_settings.donations_soft_delete_mode:
            if delete_parent:
                self.instance.parent.deleted = True
                self.instance.parent.save()
            self.instance.deleted = True
            self.instance.save()
        else:
            if delete_parent:
                self.instance.parent.delete()
            self.instance.delete()

    def confirmation_message(self):
        if self.site_settings.donations_soft_delete_mode:
            return _(
                "Are you sure you want to soft-delete this %s? If other things in your "
                "site are related to it, they may also be affected. "
                "(Record will still persist in the database)"
            ) % self.verbose_name
        else:
            return super().confirmation_message()


class SubscriptionButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        """
        This function is originally used to gather all available buttons.
        We exclude the edit button to the btns list.
        """
        # only exclude edit for subscriptions not created by a staff
        exclude = ['edit']
        if obj.created_by != None and obj.created_by.is_staff:
            exclude = None
        btns = super().get_buttons_for_obj(
            obj, exclude, classnames_add, classnames_exclude)
        return btns


class DonationButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        """
        This function is originally used to gather all available buttons.
        We exclude the edit button to the btns list.
        """
        # only exclude edit for donations not created by a staff
        exclude = ['edit']
        if obj.created_by != None and obj.created_by.is_staff:
            exclude = None
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
                    'is_recurring', 'payment_status', 'donor_column', 'donation_date',)
    list_filter = ('is_test', 'is_recurring', 'payment_status', 'donation_date',)
    search_fields = ('transaction_id', 'donation_amount',
                     'guest_email', 'user__email', 'donation_date',)
    inspect_view_enabled = True
    create_view_class = DonationCreateView
    inspect_view_class = DonationInspectView
    inspect_view_extra_css = ['css/admin_inspect.css']
    inspect_view_extra_js = ['js/admin_inspect.js']
    delete_view_class = DonationDeleteView
    form_fields_exclude = ['created_by']

    def get_queryset(self, request):
        # only show records with deleted=False (which should be valid whether soft-delete is on/off)
        qs = super().get_queryset(request)
        return qs.filter(deleted=False)
    
    def donor_column(self, obj):
        return obj.user.email if obj.user else (obj.guest_email if obj.guest_email else '-')

    donor_column.admin_order_field = 'user'  # Allows column order sorting
    donor_column.short_description = _('Donor Email')  # Renames column head


class SubscriptionAdmin(ModelAdmin):
    model = SubscriptionInstance
    button_helper_class = SubscriptionButtonHelper
    menu_label = _('Subscriptions')
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('recurring_amount', 'gateway',
                    'recurring_status', 'donor_column', 'subscribe_date',)
    list_filter = ('is_test', 'recurring_status', 'subscribe_date',)
    search_fields = ('profile_id', 'recurring_amount',
                     'user__email', 'subscribe_date',)
    inspect_view_enabled = True
    create_view_class = SubscriptionCreateView
    inspect_view_class = SubscriptionInspectView
    inspect_view_extra_css = ['css/admin_inspect.css']
    inspect_view_extra_js = ['js/admin_inspect.js']
    delete_view_class = SubscriptionDeleteView
    form_fields_exclude = ['created_by']

    def donor_column(self, obj):
        return obj.user.email if obj.user else '-'

    def get_queryset(self, request):
        # only show records with deleted=False (which should be valid whether soft-delete is on/off)
        qs = super().get_queryset(request)
        return qs.filter(deleted=False)

    donor_column.admin_order_field = 'user'  # Allows column order sorting
    donor_column.short_description = _('Donor Email')  # Renames column head


class DonationFormAdmin(ModelAdmin):
    model = DonationForm
    menu_label = _('Donation Forms')
    menu_icon = 'pilcrow'
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'description')
    search_fields = ('title', 'description')
    form_view_extra_js = ['js/admin_defaultstep.js']


class DonationGroup(ModelAdminGroup):
    menu_label = _('Donations')
    menu_icon = 'folder-open-inverse'
    menu_order = 200
    items = (DonationAdmin, SubscriptionAdmin, DonationFormAdmin)


modeladmin_register(DonationGroup)
