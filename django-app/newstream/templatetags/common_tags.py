import re
import os
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

from donations.functions import displayDonationAmountWithCurrency, displayRecurringAmountWithCurrency
from newstream.functions import get_site_name, get_site_url, printvars, get_site_settings_from_default_site
from donations.models import STATUS_ACTIVE, STATUS_CANCELLED, STATUS_PAYMENT_FAILED, STATUS_PAUSED, STATUS_PROCESSING, SubscriptionInstance

register = template.Library()


@register.filter(name='has_socialaccount')
def has_socialaccount(user):
    accounts = user.socialaccount_set.all()
    if len(accounts) > 0:
        return True
    else:
        return False


@register.filter(name='startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='get_attr')
def get_attr(object, key):
    return getattr(object, key, '')


@register.simple_tag
def site_url():
    """
    can be used as a tag in django templates like this: {% site_url %}
    returns a full site url e.g. https://newstream.example.com
    """
    return get_site_url()


@register.filter(name='site_rel_url')
def site_rel_url(relurl):
    """
    can be used as a filter in django templates like this: {{ donations_url|site_rel_url }}
    rel_url is expected to start with a forward slash
    """
    return get_site_url() + relurl


@register.simple_tag
def site_name():
    return get_site_name()


@register.filter(name='site_name_filter')
def site_name_filter(var):
    """
    This is a workaround

    I cannot find a way to simply assign a simple_tag value to a variable used in blocktrans(e.g. in unsubscription.html)
    So I resort to using a filter but ignoring the passed variable
    """
    return get_site_name()


@register.filter(name='site_settings')
def site_settings(attribute):
    """
    The standard way of fetching custom site settings is too clumsy:
    (see: https://docs.wagtail.io/en/v2.12/reference/contrib/settings.html#using-in-django-templates)

    This filter should allow templates to be more succinct
    """

    settings = get_site_settings_from_default_site()
    return getattr(settings, attribute, None)


@register.filter(name='email_css')
def returnEmailInlineCss(element):
    if element == 'heading':
        return 'font-family:Arial,Helvetica;font-size:22px;font-weight:bold;margin:0;margin-bottom:30px'
    elif element == 'last-parag':
        return 'font-family:Arial,Helvetica;font-size:16px;font-weight:normal;margin:0;margin-bottom:30px'
    else:
        return 'font-family:Arial,Helvetica;font-size:16px;font-weight:normal;margin:0;margin-bottom:15px'


@register.filter(name='alert_class')
def getAlertClass(tags):
    if 'debug' in tags or 'info' in tags:
        return "bg-blue-100 border-l-4 border-blue-500 text-blue-700 p4"
    elif 'success' in tags:
        return "bg-green-100 border-l-4 border-green-500 text-green-700 p4"
    elif 'warning' in tags:
        return "bg-orange-100 border-l-4 border-orange-500 text-orange-700 p4"
    elif 'error' in tags:
        return "bg-red-100 border-l-4 border-red-500 text-red-700 p4"
    else:
        return "bg-blue-100 border-l-4 border-blue-500 text-blue-700 p4"


@register.filter(name='next_path_filter')
def next_path_filter(rel_path):
    exceptions = ['/reset/key/done/']
    for exception in exceptions:
        if exception in rel_path:
            return ''
    return '?next=' + rel_path


@register.filter(name='is_active_page')
def is_active_page(rel_path, urlname):
    if urlname in rel_path:
        return 'active-page'
    return ''


# @register.filter(name='trans_url')
# def trans_url(request, lang_code):
#     current_url = request.path
#     parts = current_url.split('/')
#     parts[1] = lang_code
#     return '/'.join(parts)


@register.filter(name='amount_with_currency')
def amount_with_currency(donation):
    return displayDonationAmountWithCurrency(donation)


@register.filter(name='recurring_amount_with_currency')
def recurring_amount_with_currency(subscription):
    return displayRecurringAmountWithCurrency(subscription)


@register.filter(name='printvars')
def _printvars(obj):
    printvars(obj)
    return ''


# @register.filter(name='translate_href')
# def translate_href(request, menuitem):
#     lang_code = request.LANGUAGE_CODE
#     if menuitem.link_page_id:
#         page = menuitem.link_page
#         if page.+:
#             trans_page = page.+
#             printvars(trans_page)
#             if trans_page.language.code == lang_code:
#                 # no need to translate href
#                 return menuitem.href
#             else:
#                 if lang_code == 'en':
#                     translated_page = TranslatablePage.objects.live().specific().filter(translatable_page_ptr_id=trans_page.canonical_page_id)
#     else:
#         return menuitem.href


@register.filter(name='remember_filter')
def remember_filter(html):
    return mark_safe(re.sub(r':', '?', html))


@register.filter(name='display_username')
def display_username(user):
    return user.display_fullname()


@register.filter(name='display_donor')
def display_donor(donation):
    return donation.display_donor()


@register.filter(name="status_icon")
def status_icon(instance):
    status = instance.recurring_status
    if status == STATUS_ACTIVE:
        return 'active-icon'
    elif status == STATUS_PAUSED:
        return 'paused-icon'
    elif status == STATUS_PAYMENT_FAILED:
        return 'payment-failed-icon'
    elif status == STATUS_PROCESSING:
        return 'processing-icon'
    elif instance.cancel_reason == SubscriptionInstance.CancelReason.PAYMENTS_FAILED:
        return 'cancelled-warning-icon'
    else:
        return 'cancelled-icon'


@register.filter(name="status_bg_color")
def status_bg_color(instance):
    status = instance.recurring_status
    if status == STATUS_ACTIVE:
        return 'bg-primary-light'
    elif status == STATUS_PAYMENT_FAILED:
        return 'bg-caution-light'
    elif instance.cancel_reason == SubscriptionInstance.CancelReason.PAYMENTS_FAILED:
        return 'bg-warning-light'
    else:
        return 'bg-gray-light'


@register.filter(name="status_text_color")
def status_text_color(instance):
    status = instance.recurring_status
    if status == STATUS_ACTIVE:
        return 'text-primary'
    elif status == STATUS_PAYMENT_FAILED:
        return 'text-caution'
    elif instance.cancel_reason == SubscriptionInstance.CancelReason.PAYMENTS_FAILED:
        return 'text-warning'
    else:
        return 'text-gray'

@register.filter(name="status_text")
def status_text(status):
    if status == STATUS_PAYMENT_FAILED:
        return 'Payment failed'
    else:
        return status.capitalize()

@register.filter(name='get_sys_default_value')
def get_sys_default_value(field):
    """ This tag is used to display the defined env var for certain site settings fields
    """
    # map to the corresponding env var key
    envkey = "NEWSTREAM_"+field.strip().upper()
    envval = getattr(settings, envkey, None)
    if envkey.startswith("NEWSTREAM_STRIPE") or envkey.startswith("NEWSTREAM_PAYPAL"):
        # mask credentials
        envval = envval[0:10] + "*****"
    return envval
