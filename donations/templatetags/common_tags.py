import os
from django import template
from site_settings.models import AppearanceSettings
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
