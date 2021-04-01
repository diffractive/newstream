import html
from decimal import Decimal
from django import forms
from django.utils.translation import gettext_lazy as _

from donations.functions import getCurrencyDictAt

class RecurringPaymentForm_2C2P(forms.Form):
    subscription_id = forms.CharField(label=_('Recurring donation identifier(fixed)'), required=False)
    currency = forms.CharField(label=('Donation Currency(fixed)'), required=False)
    billing_cycle_now = forms.BooleanField(label=_('Change Billing Cycle to Now'), required=False)

    def __init__(self, *args, request=None, subscription=None, **kwargs):
        super().__init__(*args, **kwargs)
        currency_set = getCurrencyDictAt(subscription.currency)
        if not request:
            raise ValueError(_('Please provide a request object'))
        if not subscription:
            raise ValueError(_('Please provide a subscription object'))
        self.fields["subscription_id"].initial = subscription.profile_id
        self.fields["subscription_id"].widget.attrs['disabled'] = True
        self.fields["currency"].initial = html.unescape(currency_set['admin_label'])
        self.fields["currency"].widget.attrs['disabled'] = True
        self.fields["recurring_amount"] = forms.DecimalField(label=_('Recurring donation amount'), min_value=Decimal('0.01'), decimal_places=getCurrencyDictAt(subscription.currency)['setting']['number_decimals'])
        self.fields["recurring_amount"].initial = subscription.recurring_amount if currency_set['setting']['number_decimals'] != 0 else int(subscription.recurring_amount)