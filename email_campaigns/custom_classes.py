from datetime import datetime, timezone
from django.shortcuts import get_object_or_404
from django.conf.urls import url
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.utils import translation

from wagtail.contrib.modeladmin.views import InstanceSpecificView
from wagtail.contrib.modeladmin.helpers import ButtonHelper, AdminURLHelper
from wagtail.core.templatetags.wagtailcore_tags import richtext

from newstream.functions import generateIDSecretHash, reverse_with_site_url
from email_campaigns.models import Campaign
User = get_user_model()


class CampaignButtonHelper(ButtonHelper):

    # Define classes for our button, here we can set an icon for example
    send_button_classnames = ['button-small', 'button-secondary']

    def send_email_button(self, obj):
        # Define a label for our button
        text = _('Send Emails')
        return {
            # decide where the button links to
            'url': self.url_helper.get_action_url('send', obj.id),
            'label': text,
            'classname': self.finalise_classname(self.send_button_classnames),
            'title': text,
        }

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        """
        This function is used to gather all available buttons.
        We append our custom button to the btns list.
        """
        btns = super().get_buttons_for_obj(
            obj, exclude, classnames_add, classnames_exclude)
        if 'send' not in (exclude or []):
            btns.append(
                self.send_email_button(obj)
            )
        return btns


class SendCampaignView(InstanceSpecificView):
    """
    A Class Based View which will generate 
    """

    def __init__(self, model_admin, instance_pk):
        super().__init__(model_admin, instance_pk)

    def check_action_permitted(self, user):
        return user.is_authenticated
        # todo: refactor to the right way to deal with permissions
        # return self.permission_helper.user_can_inspect_obj(user, self.instance)

    def getUnsubscriptionLink(self, email):
        user = get_object_or_404(User, email=email)
        digest = generateIDSecretHash(user.id)
        return reverse_with_site_url('unsubscribe', kwargs={'email': email, 'hash': digest})

    def textAppendUnsubscribeLink(self, email, text):
        fullurl = self.getUnsubscriptionLink(email)
        text += "\n" + str(_("Link to unsubscribe: ")) + fullurl
        return text

    def htmlAppendUnsubscribeLink(self, email, html):
        fullurl = self.getUnsubscriptionLink(email)
        html += '<br><a href="' + fullurl + \
            '" target="_blank" rel="noopener noreferrer">' + str(_('Unsubscribe')) + '</a>'
        return html

    def send_emails(self):
        if isinstance(self.instance, Campaign):
            original_lang = translation.get_language()

            model = self.instance
            template = model.template
            email_list = []
            target_groups = model.recipients.all()
            for grp in target_groups:
                email_list += [(x.email, x.language_preference)
                               for x in grp.users.all()]
            unique_list = list(set(email_list))
            self.mails_tobe_sent = len(unique_list)

            self.mails_sent = 0
            self.refused_list = []
            for recipient, lang_pref in unique_list:
                # if lang_pref:
                #     translation.activate(lang_pref)
                # else:
                #     translation.activate(settings.LANGUAGE_CODE)
                num = send_mail(template.subject, self.textAppendUnsubscribeLink(recipient, template.plain_text), model.from_address, [
                                recipient], html_message=self.htmlAppendUnsubscribeLink(recipient, richtext(template.html_body)))
                if num == 0:
                    self.refused_list.append(recipient)
                self.mails_sent += num

            # reactivate original lang
            # if original_lang:
            #     translation.activate(original_lang)
            # else:
            #     translation.activate(settings.LANGUAGE_CODE)

            if self.mails_sent > 0:
                model.sent = True
                model.sent_at = datetime.now(timezone.utc)
                model.save()

    def get_context_data(self, **kwargs):
        context = {
            'mails_tobe_sent': self.mails_tobe_sent if self.mails_tobe_sent else 0,
            'mails_sent': self.mails_sent if self.mails_sent else 0,
            'refused_list': self.refused_list if self.refused_list else []
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_template_names(self):
        return self.model_admin.get_templates('send_emails')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # send emails before dispatch
        self.send_emails()
        # in dispatch, the handler corresponding with the appropriate http verb (e.g. get post...) will be called
        # get_context_data is called in the get handler
        return super().dispatch(request, *args, **kwargs)


class SendCampaignMAMixin(object):
    """
    A mixin to add to your model admin which hooks the different helpers, the view
    and register the new urls.
    """

    button_helper_class = CampaignButtonHelper
    url_helper_class = AdminURLHelper

    send_campaign_view_class = SendCampaignView

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls += (
            url(
                self.url_helper.get_action_url_pattern('send'),
                self.send_campaign_view,
                name=self.url_helper.get_action_url_name('send')
            ),
        )
        return urls

    def send_campaign_view(self, request, instance_pk):
        kwargs = {'model_admin': self, 'instance_pk': instance_pk}
        view_class = self.send_campaign_view_class
        return view_class.as_view(**kwargs)(request)
