from django.http import HttpResponse
from django.contrib import messages
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

from wagtail.core import hooks

from newstream.functions import _exception, _debug
from newstream_user.models import SUBS_ACTION_PAUSE, SUBS_ACTION_RESUME, SUBS_ACTION_CANCEL
from donations.models import Donation, Subscription, STATUS_COMPLETE, STATUS_ACTIVE, STATUS_PAUSED
from donations.payment_gateways import InitPaymentGateway
from donations.functions import addUpdateSubsActionLog

# for the reverse url naming rules of the modeladmin actions, see method 'get_action_url_name' in class 'AdminURLHelper' in wagtail/contrib/modeladmin/helpers/url.py

@login_required
def complete_donation(request):
    try:
        if request.method == 'POST' and request.POST.get('id', None):
            id = int(request.POST.get('id'))
            donation = get_object_or_404(Donation, id=id)
            donation.payment_status = STATUS_COMPLETE
            donation.save()
            messages.add_message(request, messages.SUCCESS, str(_('Donation %(id)d status set to Complete.') % {'id': id}))
            return redirect(reverse('donations_donation_modeladmin_inspect', kwargs={'instance_pk': id}))
    except Exception as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
    return redirect(reverse('donations_donation_modeladmin_index'))


@login_required
def setactive_subscription(request):
    try:
        if request.method == 'POST' and request.POST.get('id', None):
            id = int(request.POST.get('id'))
            subscription = get_object_or_404(Subscription, id=id)
            subscription.recurring_status = STATUS_ACTIVE
            subscription.save()
            messages.add_message(request, messages.SUCCESS, str(_('Subscription %(id)d status set to Active.') % {'id': id}))
            return redirect(reverse('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': id}))
    except Exception as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
    return redirect(reverse('donations_subscription_modeladmin_index'))

@login_required
def toggle_subscription(request):
    try:
        if request.method == 'POST' and request.POST.get('id', None):
            subscription_id = int(request.POST.get('id'))
            subscription = get_object_or_404(Subscription, id=subscription_id)
            gatewayManager = InitPaymentGateway(
                request, subscription=subscription)
            resultSet = gatewayManager.toggle_recurring_payment()
            # add to the update actions log
            addUpdateSubsActionLog(gatewayManager, SUBS_ACTION_PAUSE if resultSet['recurring-status'] == STATUS_PAUSED else SUBS_ACTION_RESUME, user=request.user)

            messages.add_message(request, messages.SUCCESS, str(_('Subscription %(id)d status is toggled to %(status)s.') % {'id': subscription_id, 'status': resultSet['recurring-status'].capitalize()}))
            return redirect(reverse('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription_id}))
    except Exception as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
    return redirect(reverse('donations_subscription_modeladmin_index'))


@login_required
def cancel_subscription(request):
    try:
        if request.method == 'POST' and request.POST.get('id', None):
            subscription_id = int(request.POST.get('id'))
            subscription = get_object_or_404(Subscription, id=subscription_id)
            gatewayManager = InitPaymentGateway(
                request, subscription=subscription)
            resultSet = gatewayManager.cancel_recurring_payment()
            # add to the update actions log
            addUpdateSubsActionLog(gatewayManager, SUBS_ACTION_CANCEL, user=request.user)

            messages.add_message(request, messages.SUCCESS, str(_('Subscription %(id)d status is cancelled.') % {'id': subscription_id}))
            return redirect(reverse('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription_id}))
    except Exception as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
    return redirect(reverse('donations_subscription_modeladmin_index'))


@hooks.register('register_admin_urls')
def extra_urls():
    return [
        path('internal-complete-donation/', complete_donation, name='internal-complete-donation'),
        path('internal-setactive-subscription/', setactive_subscription, name='internal-setactive-subscription'),
        path('internal-toggle-subscription/', toggle_subscription, name='internal-toggle-subscription'),
        path('internal-cancel-subscription/', cancel_subscription, name='internal-cancel-subscription'),
    ]