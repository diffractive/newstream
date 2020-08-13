import re
import os
import html
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from donations.functions import getCurrencyDictAt
from newstream.functions import getSiteName, printvars, getSiteSettings

register = template.Library()


@register.filter(name='sociallogin_enabled')
def sociallogin_enabled(req):
    settings = getSiteSettings(req)
    return settings.social_login_enabled


@register.filter(name='googlelogin_enabled')
def googlelogin_enabled(req):
    settings = getSiteSettings(req)
    return settings.google_login_enabled


@register.filter(name='facebooklogin_enabled')
def facebooklogin_enabled(req):
    settings = getSiteSettings(req)
    return settings.facebook_login_enabled


@register.filter(name='twitterlogin_enabled')
def twitterlogin_enabled(req):
    settings = getSiteSettings(req)
    return settings.twitter_login_enabled


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


@register.filter(name='domain')
def domain(req):
    return ('https' if os.environ.get('HTTPS') == 'on' else 'http') + '://' + req.get_host()


@register.filter(name='brand_logo')
def getBrandLogo(req):
    settings = getSiteSettings(req)
    return settings.brand_logo


@register.filter(name='site_icon')
def getSiteIcon(req):
    settings = getSiteSettings(req)
    return settings.site_icon


@register.filter(name='site_name')
def returnSiteName(req):
    return getSiteName(req)


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
def next_path_filter(request):
    exceptions = ['/reset/key/done/']
    for exception in exceptions:
        if exception in request.path:
            return ''
    return '?next=' + request.path


@register.filter(name='is_active_page')
def returnIsActivePage(request, urlname):
    if urlname in request.path:
        return 'active-page'
    return ''


# @register.filter(name='trans_url')
# def trans_url(request, lang_code):
#     current_url = request.path
#     parts = current_url.split('/')
#     parts[1] = lang_code
#     return '/'.join(parts)


@register.filter(name='amount_with_currency')
def displayDonationAmountWithCurrency(donation):
    currency_set = getCurrencyDictAt(donation.currency)
    return mark_safe(html.unescape(currency_set['symbol']+" "+str(donation.donation_amount)))


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
    if user.first_name and user.last_name:
        return user.first_name + ' ' + user.last_name
    else:
        return user.email
