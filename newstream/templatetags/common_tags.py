import re
import os
from django import template
from django.utils.safestring import mark_safe

from donations.functions import displayDonationAmountWithCurrency, displayRecurringAmountWithCurrency
from newstream.functions import get_site_name, get_site_url, printvars, get_site_settings_from_default_site

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


@register.filter(name='strip_lang')
def get_attr(current_url, current_lang):
    return re.sub("^/%s/" % current_lang, "/", current_url)


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
    can be used as a filter in django templates like this: {{ donations_url|site_url }}
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
    so I write my own filter instead
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
    return user.fullname
