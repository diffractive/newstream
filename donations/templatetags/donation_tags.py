from django import template
from django.utils.translation import gettext_lazy as _

from donations.models import STATUS_PAUSED, STATUS_ACTIVE, STATUS_PROCESSING, STATUS_CANCELLED, STATUS_INACTIVE
from donations.payment_gateways import isGatewayEditSubSupported, isGatewayToggleSubSupported, isGatewayCancelSubSupported

register = template.Library()


@register.filter(name='toggle_text')
def toggle_text(subscription):
    if subscription.recurring_status == STATUS_ACTIVE:
        return str(_('Pause Recurring Donation'))
    elif subscription.recurring_status == STATUS_PAUSED:
        return str(_('Resume Recurring Donation'))
    return '--'


@register.filter(name='is_gateway_editsub_supported')
def is_gateway_editsub_supported(subscription):
    return isGatewayEditSubSupported(subscription.gateway)


@register.filter(name='is_gateway_togglesub_supported')
def is_gateway_togglesub_supported(subscription):
    return isGatewayToggleSubSupported(subscription.gateway)


@register.filter(name='is_gateway_cancelsub_supported')
def is_gateway_cancelsub_supported(subscription):
    return isGatewayCancelSubSupported(subscription.gateway)


@register.filter(name='recurring_status_color')
def toggle_text(status):
    if status == STATUS_ACTIVE:
        return 'text-green-500'
    elif status == STATUS_PAUSED:
        return 'text-orange-500'
    elif status == STATUS_PROCESSING:
        return 'text-primary'
    elif status == STATUS_CANCELLED:
        return 'text-gray-500'
    elif status == STATUS_INACTIVE:
        return 'text-gray-500'
    return ''
