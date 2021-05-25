from decimal import Decimal
from pytz import timezone as pytz_timezone, utc
from datetime import datetime, time, timezone
from django.contrib import messages
from django.urls import path, reverse
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

from wagtail.core import hooks

from donations.email_template_ids import ET_ADN_ACCOUNT_CREATED, ET_ADN_ACCOUNT_DELETED, ET_ADN_DONATION_ERROR, ET_ADN_DONATION_REVOKED, ET_ADN_NEW_DONATION, ET_ADN_NEW_SUBSCRIPTION, ET_ADN_RENEWAL_DONATION, ET_ADN_SUBSCRIPTION_ADJUSTED, ET_ADN_SUBSCRIPTION_CANCELLED, ET_ADN_SUBSCRIPTION_CANCEL_REQUEST, ET_ADN_SUBSCRIPTION_PAUSED, ET_ADN_SUBSCRIPTION_RESCHEDULED, ET_ADN_SUBSCRIPTION_RESUMED, ET_DNR_ACCOUNT_DELETED, ET_DNR_DONATION_RECEIPT, ET_DNR_DONATION_REVOKED, ET_DNR_DONATION_STATUS_UPDATED, ET_DNR_NEW_SUBSCRIPTION, ET_DNR_RENEWAL_RECEIPT, ET_DNR_SUBSCRIPTION_ADJUSTED, ET_DNR_SUBSCRIPTION_CANCELLED, ET_DNR_SUBSCRIPTION_PAUSED, ET_DNR_SUBSCRIPTION_RESCHEDULED, ET_DNR_SUBSCRIPTION_RESUMED, ET_DNR_SUBSCRIPTION_STATUS_UPDATED
from newstream.functions import _exception, getUserTimezone
from newstream_user.models import SUBS_ACTION_PAUSE, SUBS_ACTION_RESUME, SUBS_ACTION_CANCEL, SUBS_ACTION_MANUAL, DONATION_ACTION_MANUAL
from donations.models import Donation, STATUS_CANCELLED, STATUS_FAILED, STATUS_PROCESSING, STATUS_REVOKED, Subscription, STATUS_COMPLETE, STATUS_ACTIVE, STATUS_PAUSED
from donations.payment_gateways import InitPaymentGateway
from donations.functions import addUpdateSubsActionLog, addUpdateDonationActionLog
from donations.email_functions import sendAccountCreatedNotifToAdmins, sendAccountDeletedNotifToAdmins, sendAccountDeletedNotifToDonor, sendDonationErrorNotifToAdmins, sendDonationNotifToAdmins, sendDonationReceiptToDonor, sendDonationRevokedToAdmins, sendDonationRevokedToDonor, sendDonationStatusChangeToDonor, sendNewRecurringNotifToAdmins, sendNewRecurringNotifToDonor, sendRecurringAdjustedNotifToAdmins, sendRecurringAdjustedNotifToDonor, sendRecurringCancelRequestNotifToAdmins, sendRecurringCancelledNotifToAdmins, sendRecurringCancelledNotifToDonor, sendRecurringPausedNotifToAdmins, sendRecurringPausedNotifToDonor, sendRecurringRescheduledNotifToAdmins, sendRecurringRescheduledNotifToDonor, sendRecurringResumedNotifToAdmins, sendRecurringResumedNotifToDonor, sendRenewalNotifToAdmins, sendRenewalReceiptToDonor, sendSubscriptionStatusChangeToDonor
from site_settings.models import PaymentGateway, GATEWAY_STRIPE
User = get_user_model()

# for the reverse url naming rules of the modeladmin actions, see method 'get_action_url_name' in class 'AdminURLHelper' in wagtail/contrib/modeladmin/helpers/url.py

@login_required
def set_donation_status(request):
    try:
        if request.method == 'POST' and request.POST.get('id', None):
            id = int(request.POST.get('id'))
            donation = get_object_or_404(Donation, id=id)
            old_status = donation.payment_status
            if not request.POST.get('status', ''):
                raise _("Empty value submitted for donation status update")
            donation.payment_status = request.POST.get('status').lower()
            donation.save()
            new_status = donation.payment_status
            # add to the donation actions log
            addUpdateDonationActionLog(donation, DONATION_ACTION_MANUAL, action_notes='%s -> %s' % (old_status, new_status), user=request.user)
            # notify donor of action
            sendDonationStatusChangeToDonor(request, donation)

            messages.add_message(request, messages.SUCCESS, str(_('Donation %(id)d status set to %(status)s.') % {'id': id, 'status': donation.payment_status}))
            return redirect(reverse('donations_donation_modeladmin_inspect', kwargs={'instance_pk': id}))
    except Exception as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
    return redirect(reverse('donations_donation_modeladmin_index'))


@login_required
def set_subscription_status(request):
    try:
        if request.method == 'POST' and request.POST.get('id', None):
            id = int(request.POST.get('id'))
            subscription = get_object_or_404(Subscription, id=id)
            old_status = subscription.recurring_status
            if not request.POST.get('status', ''):
                raise _("Empty value submitted for subscription status update")
            subscription.recurring_status = request.POST.get('status').lower()
            subscription.save()
            new_status = subscription.recurring_status
            # add to the update actions log
            addUpdateSubsActionLog(subscription, SUBS_ACTION_MANUAL, action_notes='%s -> %s' % (old_status, new_status), user=request.user)
            # notify donor of action
            sendSubscriptionStatusChangeToDonor(request, subscription)

            messages.add_message(request, messages.SUCCESS, str(_('Subscription %(id)d status set to %(status)s.') % {'id': id, 'status': subscription.recurring_status}))
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
            addUpdateSubsActionLog(gatewayManager.subscription, SUBS_ACTION_PAUSE if resultSet['recurring-status'] == STATUS_PAUSED else SUBS_ACTION_RESUME, user=request.user)

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
            addUpdateSubsActionLog(gatewayManager.subscription, SUBS_ACTION_CANCEL, user=request.user)

            messages.add_message(request, messages.SUCCESS, str(_('Subscription %(id)d status is cancelled.') % {'id': subscription_id}))
            return redirect(reverse('donations_subscription_modeladmin_inspect', kwargs={'instance_pk': subscription_id}))
    except Exception as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
    return redirect(reverse('donations_subscription_modeladmin_index'))


@login_required
def send_sample_email(request):
    try:
        if request.method == 'POST' and request.POST.get('template_id', None) and request.POST.get('to_email', None):
            template_id = request.POST.get('template_id')
            to_email = request.POST.get('to_email')
            result_code = 0

            # create sample donation object
            sample_donation = Donation(
                is_test=True,
                transaction_id="SAMPLE-ABCDE12345",
                user=request.user,
                gateway=PaymentGateway.objects.get(title=GATEWAY_STRIPE),
                is_recurring=False,
                donation_amount=Decimal("10.00"),
                currency="HKD",
                guest_email='',
                payment_status=STATUS_COMPLETE,
                donation_date=datetime.now(timezone.utc),
            )
            # create sample subscription object
            sample_subscription = Subscription(
                is_test=True,
                profile_id='SAMPLE-FGHIJ67890',
                user=request.user,
                gateway=PaymentGateway.objects.get(title=GATEWAY_STRIPE),
                recurring_amount=Decimal("10.00"),
                currency="HKD",
                recurring_status=STATUS_ACTIVE,
                subscribe_date=datetime.now(timezone.utc)
            )
            # create sample renewal donation object
            sample_renewal_donation = Donation(
                is_test=True,
                transaction_id="SAMPLE-ABCDE12345",
                user=request.user,
                gateway=PaymentGateway.objects.get(title=GATEWAY_STRIPE),
                is_recurring=True,
                donation_amount=Decimal("10.00"),
                subscription=sample_subscription,
                currency="HKD",
                guest_email='',
                payment_status=STATUS_COMPLETE,
                donation_date=datetime.now(timezone.utc),
            )
            # just set the subscription id to an arbitrary number
            # to prevent the django.urls.exceptions.NoReverseMatch error when using getFullReverseUrl in plain_texts.get_renewal_receipt_text
            sample_renewal_donation.subscription.id = 1
            
            if template_id == ET_DNR_DONATION_RECEIPT:
                result_code = sendDonationReceiptToDonor(request, sample_donation, override_email=to_email)
            if template_id == ET_DNR_DONATION_REVOKED:
                sample_donation.payment_status = STATUS_REVOKED
                result_code = sendDonationRevokedToDonor(request, sample_donation, override_email=to_email)
            if template_id == ET_DNR_DONATION_STATUS_UPDATED:
                result_code = sendDonationStatusChangeToDonor(request, sample_donation, override_email=to_email)
            if template_id == ET_DNR_SUBSCRIPTION_STATUS_UPDATED:
                result_code = sendSubscriptionStatusChangeToDonor(request, sample_subscription, override_email=to_email)
            if template_id == ET_DNR_RENEWAL_RECEIPT:
                result_code = sendRenewalReceiptToDonor(request, sample_renewal_donation, override_email=to_email)
            if template_id == ET_DNR_SUBSCRIPTION_ADJUSTED:
                result_code = sendRecurringAdjustedNotifToDonor(request, sample_subscription, override_email=to_email)
            if template_id == ET_DNR_NEW_SUBSCRIPTION:
                result_code = sendNewRecurringNotifToDonor(request, sample_subscription, override_email=to_email)
            if template_id == ET_DNR_SUBSCRIPTION_RESCHEDULED:
                result_code = sendRecurringRescheduledNotifToDonor(request, sample_subscription, override_email=to_email)
            if template_id == ET_DNR_SUBSCRIPTION_PAUSED:
                sample_subscription.recurring_status = STATUS_PAUSED
                result_code = sendRecurringPausedNotifToDonor(request, sample_subscription, override_email=to_email)
            if template_id == ET_DNR_SUBSCRIPTION_RESUMED:
                result_code = sendRecurringResumedNotifToDonor(request, sample_subscription, override_email=to_email)
            if template_id == ET_DNR_SUBSCRIPTION_CANCELLED:
                sample_subscription.recurring_status = STATUS_CANCELLED
                result_code = sendRecurringCancelledNotifToDonor(request, sample_subscription, override_email=to_email)
            if template_id == ET_DNR_ACCOUNT_DELETED:
                result_code = sendAccountDeletedNotifToDonor(request, request.user, override_email=to_email)
            if template_id == ET_ADN_DONATION_ERROR:
                sample_donation.payment_status = STATUS_FAILED
                result_code = sendDonationErrorNotifToAdmins(request, sample_donation, override_flag=True, override_emails=[to_email])
            if template_id == ET_ADN_NEW_DONATION:
                result_code = sendDonationNotifToAdmins(request, sample_donation, override_flag=True, override_emails=[to_email])
            if template_id == ET_ADN_DONATION_REVOKED:
                sample_donation.payment_status = STATUS_REVOKED
                result_code = sendDonationRevokedToAdmins(request, sample_donation, override_flag=True, override_emails=[to_email])
            if template_id == ET_ADN_SUBSCRIPTION_ADJUSTED:
                result_code = sendRecurringAdjustedNotifToAdmins(request, sample_subscription, override_flag=True, override_emails=[to_email])
            if template_id == ET_ADN_NEW_SUBSCRIPTION:
                result_code = sendNewRecurringNotifToAdmins(request, sample_subscription, override_flag=True, override_emails=[to_email])
            if template_id == ET_ADN_SUBSCRIPTION_RESCHEDULED:
                result_code = sendRecurringRescheduledNotifToAdmins(request, sample_subscription, override_flag=True, override_emails=[to_email])
            if template_id == ET_ADN_RENEWAL_DONATION:
                result_code = sendRenewalNotifToAdmins(request, sample_renewal_donation, override_flag=True, override_emails=[to_email])
            if template_id == ET_ADN_SUBSCRIPTION_PAUSED:
                sample_subscription.recurring_status = STATUS_PAUSED
                result_code = sendRecurringPausedNotifToAdmins(request, sample_subscription, override_flag=True, override_emails=[to_email])
            if template_id == ET_ADN_SUBSCRIPTION_RESUMED:
                result_code = sendRecurringResumedNotifToAdmins(request, sample_subscription, override_flag=True, override_emails=[to_email])
            if template_id == ET_ADN_SUBSCRIPTION_CANCELLED:
                sample_subscription.recurring_status = STATUS_CANCELLED
                result_code = sendRecurringCancelledNotifToAdmins(request, sample_subscription, override_flag=True, override_emails=[to_email])
            if template_id == ET_ADN_SUBSCRIPTION_CANCEL_REQUEST:
                sample_subscription.recurring_status = STATUS_PROCESSING
                result_code = sendRecurringCancelRequestNotifToAdmins(request, sample_subscription, override_emails=[to_email])
            if template_id == ET_ADN_ACCOUNT_CREATED:
                result_code = sendAccountCreatedNotifToAdmins(request, request.user, override_flag=True, override_emails=[to_email])
            if template_id == ET_ADN_ACCOUNT_DELETED:
                result_code = sendAccountDeletedNotifToAdmins(request, request.user, override_flag=True, override_emails=[to_email])

            if result_code == 1:
                messages.add_message(request, messages.SUCCESS, str(_('Sample Email successfully sent to %(email)s.') % {'email': to_email}))
            if result_code == 0:
                messages.add_message(request, messages.WARNING, str(_('Sample Email cannot be delivered to %(email)s. Please check with technical support.') % {'email': to_email}))
            if result_code == -1:
                messages.add_message(request, messages.WARNING, str(_('Sample Email cannot be sent to %(email)s. Please check with technical support.') % {'email': to_email}))
                
            return redirect(reverse('donations_emailtemplate_modeladmin_index'))
    except Exception as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
    return redirect(reverse('donations_emailtemplate_modeladmin_index'))


@hooks.register('register_admin_urls')
def extra_urls():
    return [
        path('internal-set-donation-status/', set_donation_status, name='internal-set-donation-status'),
        path('internal-set-subscription-status/', set_subscription_status, name='internal-set-subscription-status'),
        path('internal-toggle-subscription/', toggle_subscription, name='internal-toggle-subscription'),
        path('internal-cancel-subscription/', cancel_subscription, name='internal-cancel-subscription'),
        path('internal-send-sample-email/', send_sample_email, name='internal-send-sample-email'),
    ]


class TodayStatisticsPanel:
    order = 10

    def __init__(self, request):
        self.request = request

    def render(self):
        tz = pytz_timezone(getUserTimezone(self.request.user))
        dt_now = datetime.now(tz)
        today = dt_now.date()
        midnight = tz.localize(datetime.combine(today, time(0, 0)), is_dst=None)
        utc_dt = midnight.astimezone(utc) 
        today_donations = Donation.objects.filter(donation_date__gte=utc_dt, payment_status=STATUS_COMPLETE, deleted=False).count()
        today_subscriptions = Subscription.objects.filter(subscribe_date__gte=utc_dt, recurring_status=STATUS_ACTIVE, deleted=False).count()
        today_donors = User.objects.filter(date_joined__gte=utc_dt, is_staff=False).count()
        return mark_safe("<section class=\"summary nice-padding today-stats-panel\"><h1><strong>Today's Statistics ({})</strong></h1><ul class=\"stats\"><li><span>{}</span>New Completed Donations</li><li><span>{}</span>New Active Subscriptions</li><li><span>{}</span>New Donors</li></ul></section>".format(today, today_donations, today_subscriptions, today_donors))


class TotalStatisticsPanel:
    order = 20

    def render(self):
        total_completed_donations = Donation.objects.filter(payment_status=STATUS_COMPLETE, deleted=False).count()
        total_donations = Donation.objects.filter(deleted=False).count()
        total_donors = User.objects.filter(is_staff=False).count()
        total_active_subscriptions = Subscription.objects.filter(recurring_status=STATUS_ACTIVE, deleted=False).count()
        total_subscriptions = Subscription.objects.filter(deleted=False).count()
        return mark_safe("<section class=\"summary nice-padding total-stats-panel\"><h1><strong>Total Statistics</strong></h1><ul class=\"stats\"><li><span>{}</span>Completed Donations</li><li><span>{}</span>Total Donations</li><li><span>{}</span>All Donors</li><li><span>{}</span>Active Subscriptions</li><li><span>{}</span>All Subscriptions</li></ul></section>".format(total_completed_donations, total_donations, total_donors, total_active_subscriptions, total_subscriptions))

@hooks.register('construct_homepage_panels')
def add_statistics_panel(request, panels):
    panels.append(TodayStatisticsPanel(request))
    panels.append(TotalStatisticsPanel())