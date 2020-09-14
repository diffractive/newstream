from django import forms
from django.utils.translation import gettext_lazy as _


class RecurringPaymentForm_Paypal(forms.Form):
    recurring_amount = forms.DecimalField(label=_('Recurring Donation Amount'))
    billing_cycle_now = forms.BooleanField(label=_('Change Billing Cycle to Now'))

    def __init__(self, *args, subscription=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not subscription:
            raiseObjectNone('Please provide a subscription object')
        self.fields["recurring_amount"].initial = subscription.recurring_amount