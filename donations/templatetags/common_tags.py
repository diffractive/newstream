import os
import html
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from site_settings.models import AppearanceSettings
from donations.functions import getCurrencyDictAt
from omp.functions import getSiteName

register = template.Library()


@register.filter(name='domain')
def domain(req):
    return ('https' if os.environ.get('HTTPS') == 'on' else 'http') + '://' + req.get_host()


@register.filter(name='brand_logo')
def getBrandLogo(req):
    settings = AppearanceSettings.for_site(req.site)
    return settings.brand_logo


@register.filter(name='site_icon')
def getSiteIcon(req):
    settings = AppearanceSettings.for_site(req.site)
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


@register.filter(name='is_active_page')
def returnIsActivePage(request, urlname):
    if urlname in request.path:
        return 'active-page'
    return ''


@register.filter(name='amount_with_currency')
def displayDonationAmountWithCurrency(donation):
    currency_set = getCurrencyDictAt(donation.currency)
    return mark_safe(html.unescape(currency_set['symbol']+" "+str(donation.donation_amount)))
