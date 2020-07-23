import re
import os
import html
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from site_settings.models import SiteSettings
from donations.functions import getCurrencyDictAt
from newstream.functions import getSiteName, pickleprint

register = template.Library()


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
    settings = SiteSettings.for_site(req.site)
    return settings.brand_logo


@register.filter(name='site_icon')
def getSiteIcon(req):
    settings = SiteSettings.for_site(req.site)
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


@register.filter(name='amount_with_currency')
def displayDonationAmountWithCurrency(donation):
    currency_set = getCurrencyDictAt(donation.currency)
    return mark_safe(html.unescape(currency_set['symbol']+" "+str(donation.donation_amount)))


@register.filter(name='pickleprint')
def _pickleprint(obj):
    pickleprint(obj)
    return ''


@register.filter(name='remember_filter')
def remember_filter(html):
    return mark_safe(re.sub(r':', '?', html))


@register.filter(name='display_username')
def display_username(user):
    if user.first_name and user.last_name:
        return user.first_name + ' ' + user.last_name
    else:
        return user.email
