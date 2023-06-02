import json
import csv
from pprint import pprint
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied

from newstream.functions import _exception, uuid4_str, get_site_settings_from_default_site
from site_settings.models import PaymentGateway, GATEWAY_OFFLINE
from newstream_user.models import SUBS_ACTION_UPDATE, SUBS_ACTION_PAUSE, SUBS_ACTION_RESUME, SUBS_ACTION_CANCEL
from donations.models import DonationPaymentMeta, Subscription, SubscriptionInstance, SubscriptionPaymentMeta, Donation, TempDonation, STATUS_REVOKED, STATUS_CANCELLED, STATUS_PAUSED, STATUS_PROCESSING, STATUS_PENDING, STATUS_PROCESSED, STATUS_PAYMENT_FAILED
from donations.forms import DONATION_DETAILS_FIELDS, DonationDetailsForm
from donations.functions import isUpdateSubsFrequencyLimitationPassed, addUpdateSubsActionLog, gen_transaction_id, extract_temp_donation_meta, displayGateway, temp_donation_meta_to_donation_meta
from donations.payment_gateways import InitPaymentGateway, InitEditRecurringPaymentForm, getEditRecurringPaymentHtml, isGatewayHosted
from donations.payment_gateways.setting_classes import getOfflineSettings
User = get_user_model()


def donate(request):
    try:
        site_settings = get_site_settings_from_default_site()
        form_template = 'donations/donation_details_form.html'
        form_blueprint = site_settings.donation_form
        if not form_blueprint:
            raise Exception(_('Donation Form not yet set.'))
        if request.method == 'POST':
            form = DonationDetailsForm(
                request.POST, request=request, blueprint=form_blueprint, label_suffix='')
            if form.is_valid():
                # extract temp meta data
                temp_donation_metas = extract_temp_donation_meta(request.POST)

                # process donation amount
                if form.cleaned_data.get('donation_amount_custom', None) and form.cleaned_data['donation_amount_custom'] > 0:
                    is_amount_custom = True
                    donation_amount = form.cleaned_data['donation_amount_custom']
                else:
                    is_amount_custom = False
                    donation_amount = form.cleaned_data['donation_amount']

                # create/edit a pending temporary donation object
                payment_gateway = PaymentGateway.objects.get(
                    pk=form.cleaned_data['payment_gateway'])
                if request.session.get('temp_donation_id', ''):
                    temp_donation = TempDonation.objects.get(pk=request.session.get('temp_donation_id'))
                    temp_donation.gateway = payment_gateway
                    temp_donation.is_amount_custom = is_amount_custom
                    temp_donation.is_recurring = True if form.cleaned_data['donation_frequency'] == 'monthly' else False
                    temp_donation.donation_amount = donation_amount
                    temp_donation.currency = form.cleaned_data['currency']
                    temp_donation.temp_metas = temp_donation_metas
                    temp_donation.guest_email = form.cleaned_data.get('email', '')
                    temp_donation.guest_name = form.cleaned_data.get('name', '')
                    temp_donation.save()
                else:
                    temp_donation = TempDonation(
                        is_test=site_settings.sandbox_mode,
                        form=form_blueprint,
                        gateway=payment_gateway,
                        is_amount_custom=is_amount_custom,
                        is_recurring=True if form.cleaned_data['donation_frequency'] == 'monthly' else False,
                        donation_amount=donation_amount,
                        currency=form.cleaned_data['currency'],
                        status=STATUS_PENDING,
                        temp_metas=temp_donation_metas,
                        guest_email=form.cleaned_data.get('email', ''),
                        guest_name=form.cleaned_data.get('name', ''),
                    )
                    temp_donation.save()
                    request.session['temp_donation_id'] = temp_donation.id

                # determine path based on submit-choice
                if request.POST.get('submit-choice', '') == 'guest-submit' or request.POST.get('submit-choice', '') == 'loggedin-submit':
                    # skip to step 3 which is Donation Confirmation
                    return redirect('donations:confirm-donation')
                elif request.POST.get('submit-choice', '') == 'register-submit':
                    # proceed to step 2 which is Register or Login
                    return redirect('donations:register-signin')
                else:
                    raise Exception(_('No valid submit-choice is being submitted.'))
        else:
            form = DonationDetailsForm(
                request=request, blueprint=form_blueprint, label_suffix='')

        # see: https://docs.djangoproject.com/en/3.0/ref/forms/api/#django.forms.Form.field_order
        if form_blueprint.isAmountSteppedCustom():
            form.order_fields(
                ['donation_amount', 'donation_amount_custom', 'donation_frequency', 'payment_gateway', 'email'])
        else:
            form.order_fields(
                ['donation_amount', 'donation_frequency', 'payment_gateway', 'email'])
    except Exception as e:
        # Should rarely happen, but in case some bugs or order id repeats itself
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
        return redirect('donations:donate')

    # get offline gateway id and instructions text
    offline_gateway = PaymentGateway.objects.get(title=GATEWAY_OFFLINE)
    offline_gateway_id = offline_gateway.id
    offlineSettings = getOfflineSettings()
    # manually casting offline_instructions_text from LazyI18nString to str to avoid the "richtext expects a string" error in the template
    offline_instructions_html = str(offlineSettings.offline_instructions_text)

    return render(request, form_template, {'form': form, 'donation_details_fields': DONATION_DETAILS_FIELDS, 'offline_gateway_id': offline_gateway_id, 'offline_instructions_html': offline_instructions_html})


def register_signin(request):
    return render(request, 'donations/signin_method.html')


def confirm_donation(request):
    try:
        site_settings = get_site_settings_from_default_site()
        tmpd = TempDonation.objects.get(pk=request.session.get('temp_donation_id', None))
        paymentMethod = displayGateway(tmpd)
        isGatewayHostedBool = isGatewayHosted(tmpd.gateway)
        if request.method == 'POST':
            # determine path based on submit-choice
            if request.POST.get('submit-choice', '') == 'change-submit':
                # goes back to step 1 which is donation details
                return redirect('donations:donate')
            elif request.POST.get('submit-choice', '') == 'confirm-submit':
                # proceed with the rest of the payment procedures
                # create processing donation
                transaction_id = gen_transaction_id(gateway=tmpd.gateway)
                donation = Donation(
                    is_test=tmpd.is_test,
                    transaction_id=transaction_id,
                    user=request.user if request.user.is_authenticated else None,
                    form=tmpd.form,
                    gateway=tmpd.gateway,
                    is_recurring=tmpd.is_recurring,
                    donation_amount=tmpd.donation_amount,
                    currency=tmpd.currency,
                    guest_email=tmpd.guest_email if not request.user.is_authenticated else '',
                    guest_name=tmpd.guest_name if not request.user.is_authenticated else '',
                    payment_status=STATUS_PROCESSING,
                    metas=temp_donation_meta_to_donation_meta(tmpd.temp_metas.all()),
                    donation_date=timezone.now(),
                )
                # create a processing subscription if is_recurring
                if tmpd.is_recurring:
                    # user should have been authenticated according to flow logic
                    if not request.user or not request.user.is_authenticated:
                        raise PermissionDenied

                    # create new Subscription + SubscriptionInstance object, with a temporary profile_id created by uuidv4
                    subscription = Subscription(
                        user=request.user,
                        created_by=request.user,
                        subscription_created_at=timezone.now()
                    )
                    subscription.save()

                    instance = SubscriptionInstance(
                        is_test=tmpd.is_test,
                        profile_id=uuid4_str(),
                        user=request.user,
                        parent=subscription,
                        gateway=tmpd.gateway,
                        recurring_amount=tmpd.donation_amount,
                        currency=tmpd.currency,
                        recurring_status=STATUS_PROCESSING,
                        subscribe_date=timezone.now(),
                        created_by=request.user
                    )
                    instance.save()
                    # link subscription to the donation
                    donation.subscription = instance

                donation.save()
                request.session.pop('temp_donation_id')
                # delete temp donation instead of saving it as processed
                tmpd.delete()

                if 'first_time_registration' in request.session:
                    dpmeta = DonationPaymentMeta(
                        donation=donation, field_key='is_user_first_donation', field_value=request.session['first_time_registration'])
                    dpmeta.save()
                    request.session.pop('first_time_registration')

                # redirect to payment_gateway
                gatewayManager = InitPaymentGateway(
                    request, donation=donation)
                return gatewayManager.redirect_to_gateway_url()
            else:
                raise Exception(_('No valid submit-choice is being submitted.'))
    except TempDonation.DoesNotExist as e:
        messages.add_message(request, messages.ERROR, str(_('Session data has expired. Please enter the donation details again.')))
        return redirect('donations:donate')
    except PermissionDenied as e:
        messages.add_message(request, messages.ERROR, str(_('You are not allowed to make a recurring payment without user authentication.')))
        return redirect('donations:donate')
    except Exception as e:
        # Should rarely happen, but in case some bugs or order id repeats itself
        _exception(str(e))
    return render(request, 'donations/confirm_donation.html', {'tmpd': tmpd, 'paymentMethod': paymentMethod, 'isGatewayHosted': isGatewayHostedBool})


def thank_you(request):
    reminders_html = None
    extra_text = None
    is_tmp_transaction_id = False
    if 'error-title' in request.session or 'error-message' in request.session:
        error_title = request.session.pop('error-title', '')
        error_message = request.session.pop('error-message', '')
        return render(request, 'donations/thankyou.html', {'isValid': False, 'error_message': error_message, 'error_title': error_title})
    if 'return-donation-id' in request.session:
        donation = Donation.objects.get(
            pk=request.session['return-donation-id'])
        paymentMethod = displayGateway(donation)
        # logs user in
        if donation.user:
            login(request, donation.user,
                  backend='django.contrib.auth.backends.ModelBackend')
        # display extra html if donation is offline
        if donation.gateway.is_offline():
            offlineSettings = getOfflineSettings()
            # manually casting offline_thankyou_text from LazyI18nString to str to avoid the "richtext expects a string" error in the template
            reminders_html = str(offlineSettings.offline_thankyou_text)
        # display extra text for certain scenarios
        if donation.gateway.is_paypal() and donation.payment_status == STATUS_PROCESSING:
            extra_text = _('Your donation should be complete in 1-2 minutes. ')
            is_tmp_transaction_id = True
        if donation.gateway.is_offline() and donation.payment_status == STATUS_PROCESSING:
            extra_text = _('Please complete your donation by following either one of the payment methods stated below. ')
        return render(request, 'donations/thankyou.html', {'reminders_html': reminders_html, 'is_tmp_transaction_id': is_tmp_transaction_id, 'isValid': True, 'paymentMethod': paymentMethod, 'extra_text': extra_text, 'isFirstTime': donation.is_user_first_donation, 'donation': donation})
    return render(request, 'donations/thankyou.html', {'reminders_html': reminders_html, 'is_tmp_transaction_id': is_tmp_transaction_id, 'isValid': False, 'extra_text': extra_text, 'error_message': _('No Payment Data is received.'), 'error_title': _("Unknown Error")})


def cancelled(request):
    if 'error-title' in request.session or 'error-message' in request.session:
        error_title = request.session.pop('error-title', '')
        error_message = request.session.pop('error-message', '')
        return render(request, 'donations/cancelled.html', {'isValid': False, 'error_message': error_message, 'error_title': error_title})
    if 'return-donation-id' in request.session:
        donation = Donation.objects.get(
            pk=request.session['return-donation-id'])
        paymentMethod = displayGateway(donation)
        donation.payment_status = STATUS_CANCELLED
        donation.save()
        if donation.subscription:
            donation.subscription.recurring_status = STATUS_CANCELLED
            donation.subscription.cancel_reason = SubscriptionInstance.CancelReason.DECLINED_CHECKOUT
            donation.subscription.save()
        # logs user in
        if donation.user:
            login(request, donation.user,
                  backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'donations/cancelled.html', {'isValid': True, 'isFirstTime': donation.is_user_first_donation, 'paymentMethod': paymentMethod, 'donation': donation})
    return render(request, 'donations/cancelled.html', {'isValid': False, 'error_message': _('No Payment Data is received.'), 'error_title': _("Unknown Error")})


def revoked(request):
    if 'error-title' in request.session or 'error-message' in request.session:
        error_title = request.session.pop('error-title', '')
        error_message = request.session.pop('error-message', '')
        return render(request, 'donations/revoked.html', {'isValid': False, 'error_message': error_message, 'error_title': error_title})
    if 'return-donation-id' in request.session:
        donation = Donation.objects.get(
            pk=request.session['return-donation-id'])
        paymentMethod = displayGateway(donation)
        donation.payment_status = STATUS_REVOKED
        # No need to update recurring_status as no subscription object has been created yet
        donation.save()
        # logs user in
        if donation.user:
            login(request, donation.user,
                  backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'donations/revoked.html', {'isValid': True, 'isFirstTime': donation.is_user_first_donation, 'paymentMethod': paymentMethod, 'donation': donation})
    return render(request, 'donations/revoked.html', {'isValid': False, 'error_message': _('No Payment Data is received.'), 'error_title': _("Unknown Error")})


@login_required
def cancel_recurring(request):
    """ This is called when the user clicks confirm when cancelling a recurring donation on page donations.views.my_recurring_donations
        We only cancel the subscription if it is owned by request.user
        Action is logged for the corresponding subscription, action logs can be viewed by inspecting the subscription's 'Action Log' tab

        Sample (JSON) request: {
            'subscription_id': 1,
            'csrfmiddlewaretoken': 'LZSpOsb364pn9R3gEPXdw2nN3dBEi7RWtMCBeaCse2QawCFIndu93fD3yv9wy0ij'
        }

        @todo: revise error handling, avoid catching all exceptions at the end
    """

    try:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            if 'subscription_id' not in json_data:
                print("No subscription_id in JSON body", flush=True)
                return HttpResponse(status=400)
            subscription_id = int(json_data['subscription_id'])
            subscription_instance = get_object_or_404(SubscriptionInstance, id=subscription_id)
            if subscription_instance.user == request.user:
                gatewayManager = InitPaymentGateway(
                    request, subscription=subscription_instance)
                gatewayManager.cancel_recurring_payment(reason=SubscriptionInstance.CancelReason.BY_DONOR)
                # add to the update actions log
                addUpdateSubsActionLog(gatewayManager.subscription, SUBS_ACTION_CANCEL)
                return JsonResponse({'status': 'success', 'button-text': str(_('View all renewals')), 'recurring-status': str(_(STATUS_CANCELLED.capitalize())), 'button-href': reverse('donations:my-renewals', kwargs={'uuid': subscription_instance.parent.uuid})})
            else:
                raise PermissionError(_('You are not authorized to cancel subscription %(id)d.') % {'id': subscription_id})
        else:
            return HttpResponse(400)
    except (ValueError, PermissionError, RuntimeError, Exception) as e:
        _exception(str(e))
        return JsonResponse({'status': 'failure', 'reason': str(e)})


@login_required
def toggle_recurring(request):
    """ This is called when the user clicks the 'Pause/Resume recurring donation' button on page donations.views.my_recurring_donations
        We only update the subscription if it is owned by request.user
        Action is logged for the corresponding subscription, action logs can be viewed by inspecting the subscription's 'Action Log' tab

        Sample request: {
            'subscription_id': 1,
            'csrfmiddlewaretoken': 'LZSpOsb364pn9R3gEPXdw2nN3dBEi7RWtMCBeaCse2QawCFIndu93fD3yv9wy0ij'
        }

        @todo: revise error handling, avoid catching all exceptions at the end
    """

    try:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            if 'subscription_id' not in json_data:
                print("No subscription_id in JSON body", flush=True)
                return HttpResponse(status=400)
            subscription_id = int(json_data['subscription_id'])
            subscription = get_object_or_404(SubscriptionInstance, id=subscription_id)
            if subscription.user == request.user:
                gatewayManager = InitPaymentGateway(
                    request, subscription=subscription)
                # check if frequency limitation is enabled and passed
                if not isUpdateSubsFrequencyLimitationPassed(gatewayManager):
                    raise Exception(_('You have already carried out 5 subscription update action in the last 5 minutes, our current limit is 5 subscription update actions(edit/pause/resume) every 5 minutes.'))
                resultSet = gatewayManager.toggle_recurring_payment()
                # add to the update actions log
                addUpdateSubsActionLog(gatewayManager.subscription, SUBS_ACTION_PAUSE if resultSet['recurring-status'] == STATUS_PAUSED else SUBS_ACTION_RESUME)
                return JsonResponse({'status': 'success', 'button-text': resultSet['button-text'], 'recurring-status': str(_(resultSet['recurring-status'].capitalize())), 'success-message': resultSet['success-message']})
            else:
                raise PermissionError(_('You are not authorized to pause/resume subscription %(id)d.') % {'id': subscription_id})
        else:
            return HttpResponse(400)
    except (ValueError, PermissionError, RuntimeError, Exception) as e:
        _exception(str(e))
        return JsonResponse({'status': 'failure', 'reason': str(e)})


@login_required
def edit_recurring(request, id):
    """ This is called when the user clicks the 'Edit recurring donation' button on page donations.views.my_recurring_donations
        We only update the subscription if it is owned by request.user
        Action is logged for the corresponding subscription, action logs can be viewed by inspecting the subscription's 'Action Log' tab

        Sample (Form) request: {
            'recurring_amount': 10.00,
            'billing_cycle_now': 'on'
        }
        * only Stripe's form has the billing_cycle_now option

        @todo: revise error handling, avoid catching all exceptions at the end
    """
    try:
        subscription = get_object_or_404(SubscriptionInstance, id=id)
        if subscription.user == request.user:
            # Form object is initialized according to the specific gateway and if request.method=='POST'
            form = InitEditRecurringPaymentForm(request.POST, request.method, subscription)
            if request.method == 'POST':
                if form.is_valid():
                    # use gatewayManager to process the data in form.cleaned_data as required
                    gatewayManager = InitPaymentGateway(
                        request, subscription=subscription)
                    # check if frequency limitation is enabled and passed
                    if not isUpdateSubsFrequencyLimitationPassed(gatewayManager):
                        raise Exception(_('You have already carried out 5 subscription update action in the last 5 minutes, our current limit is 5 subscription update actions(edit/pause/resume) every 5 minutes.'))
                    original_value = gatewayManager.subscription.recurring_amount
                    gatewayManager.update_recurring_payment(form.cleaned_data)
                    new_value = gatewayManager.subscription.recurring_amount
                    # add to the update actions log
                    addUpdateSubsActionLog(gatewayManager.subscription, SUBS_ACTION_UPDATE, 'Recurring Amount: %s -> %s' % (str(original_value), str(new_value)))
                    return redirect('donations:edit-recurring', id=id)
        else:
            raise PermissionError(_('You are not authorized to edit subscription %(id)d.') % {'id': id})
    except PermissionError as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
        return redirect('donations:my-recurring-donations')
    except (ValueError, RuntimeError, Exception) as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
    return render(request, getEditRecurringPaymentHtml(subscription), {'form': form, 'subscription': subscription})

@login_required
def confirm_update_card_details(request, id):
    """
    We cancel a subscription and start the process of creating a new subscription.
    """
    try:
        subscription = get_object_or_404(SubscriptionInstance, id=id)
        if subscription.user == request.user:
            if request.method == 'POST':
                # proceed with the rest of the payment procedures
                # create processing donation
                transaction_id = gen_transaction_id(gateway=subscription.gateway)
                form = Donation.objects.filter(subscription=subscription).order_by('id').first().form
                donation = Donation(
                    is_test=subscription.is_test,
                    transaction_id=transaction_id,
                    user=request.user,
                    form=form,
                    gateway=subscription.gateway,
                    is_recurring=True,
                    donation_amount=subscription.recurring_amount,
                    currency=subscription.currency,
                    payment_status=STATUS_PROCESSING,
                    donation_date=timezone.now(),
                )

                instance = SubscriptionInstance(
                    is_test=subscription.is_test,
                    profile_id=uuid4_str(),
                    user=request.user,
                    parent=subscription.parent,
                    gateway=subscription.gateway,
                    recurring_amount=subscription.recurring_amount,
                    currency=subscription.currency,
                    recurring_status=STATUS_PROCESSING,
                    subscribe_date=timezone.now(),
                    created_by=request.user
                )
                instance.save()

                # Save old_instance_id with the subscription id, so that we can fetch information from the failed payment
                spmeta = SubscriptionPaymentMeta(
                    subscription=instance, field_key='old_instance_id', field_value=id)
                spmeta.save()

                # link subscription to the donation
                donation.subscription = instance

                donation.save()

                # redirect to payment_gateway
                gatewayManager = InitPaymentGateway(
                    request, donation=donation)
                return gatewayManager.redirect_to_gateway_url()
        else:
            raise PermissionError(_('You are not authorized to edit subscription %(id)d.') % {'id': id})
    except PermissionError as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
        return redirect('donations:my-recurring-donations')
    except (ValueError, RuntimeError, Exception) as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
    return render(request, 'donations/update_payment_details.html', {'subscription': subscription})

@login_required
def my_onetime_donations(request):
    # deleted=False should be valid whether soft-delete mode is on or off
    # previously deleted records should still be hidden even soft-delete mode is turned off afterwards
    donations = Donation.objects.filter(
        user=request.user, is_recurring=False, deleted=False).order_by('-donation_date')
    site_settings = get_site_settings_from_default_site()
    return render(request, 'donations/my_onetime_donations.html', {'donations': donations, 'site_settings': site_settings})


@login_required
def my_recurring_donations(request):
    # deleted=False should be valid whether soft-delete mode is on or off
    subscriptions = Subscription.objects.filter(
        user=request.user, deleted=False).order_by('-subscription_created_at')
    site_settings = get_site_settings_from_default_site()

    # Add success mesasge if returning from updated card flow
    if request.session.get('updated-card'):
        messages.add_message(request, messages.SUCCESS, _(
                            'Your payment is successful. Recurring donation is resumed active.'))
        del request.session['updated-card']

    # Display error message if theres a payment failure
    for sub in subscriptions:
        if sub.latest_instance.recurring_status == STATUS_PAYMENT_FAILED:
            messages.add_message(request, messages.ERROR, _(
                'A recent payment of your recurring donation has failed. Please update the corresponding payment method.'
            ))
            break
    return render(request, 'donations/my_recurring_donations.html', {'subscriptions': subscriptions, 'site_settings': site_settings})


@login_required
def my_renewals(request, uuid):
    # deleted=False should be valid whether soft-delete mode is on or off
    subscription = get_object_or_404(Subscription, uuid=uuid, deleted=False)
    try:
        if subscription.user == request.user:
            # find donations under all SubscriptionInstances under the same Subscription
            renewals = Donation.objects.filter(
                subscription__parent=subscription, deleted=False).order_by('-donation_date')
            site_settings = get_site_settings_from_default_site()
            # subscription details should be fetched from the latest instance
            return render(request, 'donations/my_renewals.html', {'subscription': subscription.latest_instance, 'renewals': renewals, 'site_settings': site_settings})
        else:
            raise PermissionError(_('You are not authorized to view renewals of subscription %(id)d.') % {'id': id})
    except PermissionError as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
        return redirect('donations:my-recurring-donations')

@login_required
def export_donations(request):
    if not request.user.is_staff:
        raise PermissionDenied
    filename = timezone.now().strftime("%Y%m%d-%H%M%S") + 'donations.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    headings1 = ['id', 'transaction_id','donation_amount','is_recurring', 'currency', 'payment_status']
    headings2 = ['created_at', 'updated_at', 'linked_donor_deleted', 'donation_form', 'donor_name', 'donor_email']
    headings3 = ['gateway', 'subscription_id', 'is_test']
    headings4 = ['donation_date', 'created_by', 'guest_email']
    donations = Donation.objects.all().select_related('user').select_related('gateway')
    headings =  headings1 + headings2 + headings3 + headings4

    writer = csv.writer(response)
    writer.writerow(headings)
    for donation in donations:
        data_row = [getattr(donation, field) for field in headings1]

        created_at = getattr(donation, 'created_at').strftime("%Y-%m-%d %H:%M:%S")
        updated_at = getattr(donation, 'updated_at').strftime("%Y-%m-%d %H:%M:%S")
        data_row += [created_at, updated_at]
        data_row += [getattr(donation, 'linked_user_deleted'), getattr(donation, 'form')]
        if donation.user is None:
            data_row += ['', getattr(donation, 'guest_email')]
        else:
            data_row += [donation.display_donor_name(), getattr(donation.user, 'email')]

        data_row += [getattr(donation, field) for field in headings3]
        donation_date = getattr(donation, 'donation_date').strftime("%Y-%m-%d")
        data_row += [donation_date, getattr(donation, 'created_by'), getattr(donation, 'guest_email')]
        writer.writerow(data_row)

    return response

@login_required
def export_subscriptions(request):
    if not request.user.is_staff:
        raise PermissionDenied
    filename = timezone.now().strftime("%Y%m%d-%H%M%S") + 'subscriptions.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    headings1 = ['id', 'profile_id','recurring_amount', 'currency', 'recurring_status']
    headings2 = ['created_at', 'updated_at', 'linked_donor_deleted', 'gateway', 'donor_name', 'donor_email']
    headings3 = ['is_test', 'subscribe_date', 'created_by']
    subscriptions = SubscriptionInstance.objects.all().select_related('user').select_related('gateway')
    headings =  headings1 + headings2 + headings3

    writer = csv.writer(response)
    writer.writerow(headings)
    for subscription in subscriptions:
        data_row = [getattr(subscription, field) for field in headings1]

        created_at = getattr(subscription, 'created_at').strftime("%Y-%m-%d %H:%M:%S")
        updated_at = getattr(subscription, 'updated_at').strftime("%Y-%m-%d %H:%M:%S")
        data_row += [created_at, updated_at]

        data_row += [getattr(subscription, 'linked_user_deleted'), getattr(subscription, 'gateway')]
        if subscription.user is None:
            data_row += ['', '']
        else:
            data_row += [subscription.user.display_fullname(), getattr(subscription.user, 'email')]
        subscribe_date = getattr(subscription, 'subscribe_date').strftime("%Y-%m-%d")
        data_row += [getattr(subscription, 'is_test'), subscribe_date, getattr(subscription, 'created_by')]
        writer.writerow(data_row)

    return response

@login_required
def export_donors(request):
    if not request.user.is_staff:
        raise PermissionDenied
    filename = timezone.now().strftime("%Y%m%d-%H%M%S") + 'donors.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    donors = User.objects.all()
    headings1 = ['id', 'first_name', 'last_name', 'email', 'is_active']
    headings2 = ['date_joined', 'opt_in_mailing_list']
    headings = headings1 + headings2

    writer = csv.writer(response)
    writer.writerow(headings)
    for donor in donors:
        data_row = ([getattr(donor, field) for field in headings1])
        date_joined = getattr(donor, 'date_joined').strftime("%Y-%m-%d %H:%M:%S")
        data_row += [date_joined, getattr(donor, 'opt_in_mailing_list')]
        writer.writerow(data_row)
    guests = Donation.objects.order_by().values_list('guest_email', flat=True).distinct()
    for guest in guests:
        if guest:
            writer.writerow(['','','', guest,'','',''])
    return response
