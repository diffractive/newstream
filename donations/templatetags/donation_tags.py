import os
from django import template

register = template.Library()


@register.filter(name='domain')
def domain(req):
    return ('https' if os.environ.get('HTTPS') == 'on' else 'http') + '://' + req.get_host()
