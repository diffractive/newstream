from donations.email_functions import sendAccountCreatedNotifToAdmins, sendAccountDeletedNotifToAdmins, sendAccountDeletedNotifToDonor, sendDonationErrorNotifToAdmins, sendDonationNotifToAdmins, sendDonationReceiptToDonor, sendDonationRevokedToAdmins, sendDonationRevokedToDonor, sendDonationStatusChangeToDonor, sendNewRecurringNotifToAdmins, sendNewRecurringNotifToDonor, sendRecurringAdjustedNotifToAdmins, sendRecurringAdjustedNotifToDonor, sendRecurringCancelRequestNotifToAdmins, sendRecurringCancelledNotifToAdmins, sendRecurringCancelledNotifToDonor, sendRecurringPausedNotifToAdmins, sendRecurringPausedNotifToDonor, sendRecurringRescheduledNotifToAdmins, sendRecurringRescheduledNotifToDonor, sendRecurringResumedNotifToAdmins, sendRecurringResumedNotifToDonor, sendRenewalNotifToAdmins, sendRenewalReceiptToDonor, sendSubscriptionStatusChangeToDonor
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.views import InstanceSpecificView
from wagtail.contrib.modeladmin.helpers import ButtonHelper, AdminURLHelper
from wagtail.core.templatetags.wagtailcore_tags import richtext

User = get_user_model()


class EmailTemplateButtonHelper(ButtonHelper):
    """
    This class adds a 'Send Sample Email' button for each email template in the IndexView
    """

    send_button_classnames = ['button-small', 'button-secondary']

    def send_button(self, obj):
        # Define a label for our button
        text = 'Send Sample Email'
        return {
            'url': self.url_helper.get_action_url('send-sample-email', obj.id), # decide where the button links to
            'label': text,
            'classname': self.finalise_classname(self.send_button_classnames),
            'title': text,
        }

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        """
        This function is used to gather all available buttons.
        We append our custom button to the btns list.
        """
        btns = super().get_buttons_for_obj(obj, exclude, classnames_add, classnames_exclude)
        if 'send-sample-email' not in (exclude or []):
            btns.append(
                self.send_button(obj)
            )
        return btns


class SendSampleEmailTemplateView(InstanceSpecificView):
    """
    This class provides the View for the url of "Send Sample Email" button
    """

    def __init__(self, model_admin, instance_pk):
        super().__init__(model_admin, instance_pk)

    def check_action_permitted(self, user):
        return self.permission_helper.user_can_edit_obj(user, self.instance)

    def get_context_data(self, **kwargs):
        model = self.instance
        context = {
            'form_target_url': reverse('internal-send-sample-email'),
            'template_id': model.template_id,
            'template_subject': model.email_subject
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_template_names(self):
        return self.model_admin.get_templates('send_sample_email')


class SendSampleEmailMixin(object):
    """
    A mixin to add to the EmailTemplateAdmin which hooks the EmailTemplateButtonHelper and AdminURLHelper,
    the SendSampleEmailTemplateView and register the new url for 'send-sample-email'.
    """

    button_helper_class = EmailTemplateButtonHelper
    url_helper_class = AdminURLHelper

    send_sample_email_view_class = SendSampleEmailTemplateView

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls += (
            url(
                self.url_helper.get_action_url_pattern('send-sample-email'),
                self.send_sample_email_view,
                name=self.url_helper.get_action_url_name('send-sample-email')
            ),
        )
        return urls

    def send_sample_email_view(self, request, instance_pk):
        kwargs = {'model_admin': self, 'instance_pk': instance_pk}
        view_class = self.send_sample_email_view_class
        return view_class.as_view(**kwargs)(request)
