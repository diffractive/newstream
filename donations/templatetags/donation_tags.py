from django import template

register = template.Library()


@register.filter(name='domain')
def domain(req):
    return req.build_absolute_uri('/')[:-1]
