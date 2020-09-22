from django import template
from django.utils.translation import gettext_lazy as _

from donations.models import STATUS_PAUSED, STATUS_ACTIVE

register = template.Library()


@register.filter(name='toggle_text')
def toggle_text(subscription):
    if subscription.recurring_status == STATUS_ACTIVE:
        return str(_('Pause Recurring Donation'))
    elif subscription.recurring_status == STATUS_PAUSED:
        return str(_('Resume Recurring Donation'))
    return '--'
