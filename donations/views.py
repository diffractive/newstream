import json
from datetime import datetime, timezone
from pprint import pprint
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from newstream.functions import getSiteSettings, _exception, uuid4_str
from site_settings.models import PaymentGateway, GATEWAY_OFFLINE
from newstream_user.models import SUBS_ACTION_UPDATE, SUBS_ACTION_PAUSE, SUBS_ACTION_RESUME, SUBS_ACTION_CANCEL
from donations.models import DonationPaymentMeta, Subscription, Donation, TempDonation, STATUS_REVOKED, STATUS_CANCELLED, STATUS_PAUSED, STATUS_PROCESSING, STATUS_PENDING, STATUS_PROCESSED
from donations.forms import DONATION_DETAILS_FIELDS, DonationDetailsForm
from donations.functions import isUpdateSubsFrequencyLimitationPassed, addUpdateSubsActionLog, gen_transaction_id, process_temp_donation_meta
from donations.payment_gateways import InitPaymentGateway, InitEditRecurringPaymentForm, getEditRecurringPaymentHtml, isGatewayHosted
from donations.payment_gateways.setting_classes import getOfflineSettings
User = get_user_model()


def donate(request):
    try:
        siteSettings = getSiteSettings(request)
        form_template = 'donations/donation_details_form.html'
        form_blueprint = siteSettings.donation_form
        if not form_blueprint:
            raise Exception(_('Donation Form not yet set.'))
        if request.method == 'POST':
            form = DonationDetailsForm(
                request.POST, request=request, blueprint=form_blueprint, label_suffix='')
            if form.is_valid():
                # process temp meta data
                temp_donation_metas = process_temp_donation_meta(request)

                # process donation amount
                if form.cleaned_data.get('donation_amount_custom', None) and form.cleaned_data['donation_amount_custom'] > 0:
                    is_amount_custom = True
                    donation_amount = form.cleaned_data['donation_amount_custom']
                else:
                    is_amount_custom = False
                    donation_amount = form.cleaned_data['donation_amount']

                # create a pending temporary donation object
                payment_gateway = PaymentGateway.objects.get(
                    pk=form.cleaned_data['payment_gateway'])
                temp_donation = TempDonation(
                    is_test=siteSettings.sandbox_mode,
                    form=form_blueprint,
                    gateway=payment_gateway,
                    is_amount_custom=is_amount_custom,
                    is_recurring=True if form.cleaned_data['donation_frequency'] == 'monthly' else False,
                    donation_amount=donation_amount,
                    currency=form.cleaned_data['currency'],
                    status=STATUS_PENDING,
                    temp_metas=temp_donation_metas,
                    guest_email=form.cleaned_data.get('email', ''),
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
                    if form_blueprint.isAmountSteppedCustom():
                        form.order_fields(
                            ['donation_amount', 'donation_amount_custom', 'donation_frequency', 'payment_gateway', 'email'])
                    else:
                        form.order_fields(
                            ['donation_amount', 'donation_frequency', 'payment_gateway', 'email'])
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

    # get offline gateway id and instructions text
    offline_gateway = PaymentGateway.objects.get(title=GATEWAY_OFFLINE)
    offline_gateway_id = offline_gateway.id
    offlineSettings = getOfflineSettings(request)
    offline_instructions_html = offlineSettings.offline_instructions_text
    
    return render(request, form_template, {'form': form, 'donation_details_fields': DONATION_DETAILS_FIELDS, 'offline_gateway_id': offline_gateway_id, 'offline_instructions_html': offline_instructions_html})


def register_signin(request):
    return render(request, 'donations/signin_method.html')


def confirm_donation(request):
    try:
        siteSettings = getSiteSettings(request)
        tmpd = TempDonation.objects.get(pk=request.session.get('temp_donation_id', None))
        paymentMethod = getattr(siteSettings, tmpd.gateway.frontend_label_attr_name, tmpd.gateway.title)
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
                    payment_status=STATUS_PROCESSING,
                    metas=tmpd.temp_metas,
                    donation_date=datetime.now(timezone.utc),
                )
                # create a processing subscription if is_recurring
                if tmpd.is_recurring:
                    # create new Subscription object, with a temporary profile_id created by uuidv4
                    # user should have been authenticated according to flow logic
                    subscription = Subscription(
                        is_test=tmpd.is_test,
                        profile_id=uuid4_str(),
                        user=request.user if request.user.is_authenticated else None,
                        gateway=tmpd.gateway,
                        recurring_amount=tmpd.donation_amount,
                        currency=tmpd.currency,
                        recurring_status=STATUS_PROCESSING,
                        subscribe_date=datetime.now(timezone.utc)
                    )
                    subscription.save()
                    # link subscription to the donation
                    donation.subscription = subscription

                donation.save()
                request.session.pop('temp_donation_id')
                # delete temp donation instead of saving it as processed
                tmpd.delete()
                # tmpd.status = STATUS_PROCESSED
                # tmpd.save()

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

    except Exception as e:
        # Should rarely happen, but in case some bugs or order id repeats itself
        _exception(str(e))
    return render(request, 'donations/confirm_donation.html', {'tmpd': tmpd, 'paymentMethod': paymentMethod, 'isGatewayHosted': isGatewayHostedBool})


def thank_you(request):
    reminders_html = None
    extra_text = None
    if 'error-title' in request.session or 'error-message' in request.session:
        error_title = request.session.pop('error-title', '')
        error_message = request.session.pop('error-message', '')
        return render(request, 'donations/thankyou.html', {'isValid': False, 'error_message': error_message, 'error_title': error_title})
    if 'return-donation-id' in request.session:
        donation = Donation.objects.get(
            pk=request.session['return-donation-id'])
        # logs user in
        if donation.user:
            login(request, donation.user,
                  backend='django.contrib.auth.backends.ModelBackend')
        # display extra html if donation is offline
        if donation.gateway.is_offline():
            offlineSettings = getOfflineSettings(request)
            reminders_html = offlineSettings.offline_thankyou_text
        # display extra text for certain scenarios
        if donation.gateway.is_paypal() and donation.payment_status == STATUS_PROCESSING:
            extra_text = _('Your donation should be complete in 1-2 minutes.')
        if donation.gateway.is_offline() and donation.payment_status == STATUS_PROCESSING:
            extra_text = _('Please complete your donation by following either one of the payment methods stated below.')
        return render(request, 'donations/thankyou.html', {'reminders_html': reminders_html, 'isValid': True, 'extra_text': extra_text, 'isFirstTime': donation.is_user_first_donation, 'donation': donation})
    return render(request, 'donations/thankyou.html', {'reminders_html': reminders_html, 'isValid': False, 'extra_text': extra_text, 'error_message': _('No Payment Data is received.'), 'error_title': _("Unknown Error")})


def cancelled(request):
    if 'error-title' in request.session or 'error-message' in request.session:
        error_title = request.session.pop('error-title', '')
        error_message = request.session.pop('error-message', '')
        return render(request, 'donations/cancelled.html', {'isValid': False, 'error_message': error_message, 'error_title': error_title})
    if 'return-donation-id' in request.session:
        donation = Donation.objects.get(
            pk=request.session['return-donation-id'])
        donation.payment_status = STATUS_CANCELLED
        # No need to update recurring_status as no subscription object has been created yet
        donation.save()
        # logs user in
        if donation.user:
            login(request, donation.user,
                  backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'donations/cancelled.html', {'isValid': True, 'isFirstTime': donation.is_user_first_donation, 'donation': donation})
    return render(request, 'donations/cancelled.html', {'isValid': False, 'error_message': _('No Payment Data is received.'), 'error_title': _("Unknown Error")})


def revoked(request):
    if 'error-title' in request.session or 'error-message' in request.session:
        error_title = request.session.pop('error-title', '')
        error_message = request.session.pop('error-message', '')
        return render(request, 'donations/revoked.html', {'isValid': False, 'error_message': error_message, 'error_title': error_title})
    if 'return-donation-id' in request.session:
        donation = Donation.objects.get(
            pk=request.session['return-donation-id'])
        donation.payment_status = STATUS_REVOKED
        # No need to update recurring_status as no subscription object has been created yet
        donation.save()
        # logs user in
        if donation.user:
            login(request, donation.user,
                  backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'donations/revoked.html', {'isValid': True, 'isFirstTime': donation.is_user_first_donation, 'donation': donation})
    return render(request, 'donations/revoked.html', {'isValid': False, 'error_message': _('No Payment Data is received.'), 'error_title': _("Unknown Error")})


@login_required
@csrf_exempt
def cancel_recurring(request):
    try:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            if 'subscription_id' not in json_data:
                print("No subscription_id in JSON body", flush=True)
                return HttpResponse(status=400)
            subscription_id = int(json_data['subscription_id'])
            subscription = get_object_or_404(Subscription, id=subscription_id)
            gatewayManager = InitPaymentGateway(
                request, subscription=subscription)
            gatewayManager.cancel_recurring_payment()
            # add to the update actions log
            addUpdateSubsActionLog(gatewayManager.subscription, SUBS_ACTION_CANCEL)
            return JsonResponse({'status': 'success', 'button-html': str(_('View all renewals')), 'recurring-status': str(_(STATUS_CANCELLED.capitalize())), 'button-href': reverse('donations:my-renewals', kwargs={'id': subscription_id})})
        else:
            return HttpResponse(400)
    except ValueError as e:
        _exception(str(e))
        return JsonResponse({'status': 'failure', 'reason': str(e)})
    except RuntimeError as e:
        _exception(str(e))
        return JsonResponse({'status': 'failure', 'reason': str(e)})
    except Exception as e:
        _exception(str(e))
        return JsonResponse({'status': 'failure', 'reason': str(e)})


@login_required
@csrf_exempt
def toggle_recurring(request):
    try:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            if 'subscription_id' not in json_data:
                print("No subscription_id in JSON body", flush=True)
                return HttpResponse(status=400)
            subscription_id = int(json_data['subscription_id'])
            subscription = get_object_or_404(Subscription, id=subscription_id)
            gatewayManager = InitPaymentGateway(
                request, subscription=subscription)
            # check if frequency limitation is enabled and passed
            if not isUpdateSubsFrequencyLimitationPassed(gatewayManager):
                raise Exception(_('You have already carried out 5 subscription update action in the last 5 minutes, our current limit is 5 subscription update actions(edit/pause/resume) every 5 minutes.'))
            resultSet = gatewayManager.toggle_recurring_payment()
            # add to the update actions log
            addUpdateSubsActionLog(gatewayManager.subscription, SUBS_ACTION_PAUSE if resultSet['recurring-status'] == STATUS_PAUSED else SUBS_ACTION_RESUME)
            return JsonResponse({'status': 'success', 'button-html': resultSet['button-html'], 'recurring-status': str(_(resultSet['recurring-status'].capitalize())), 'success-message': resultSet['success-message']})
        else:
            return HttpResponse(400)
    except ValueError as e:
        _exception(str(e))
        return JsonResponse({'status': 'failure', 'reason': str(e)})
    except RuntimeError as e:
        _exception(str(e))
        return JsonResponse({'status': 'failure', 'reason': str(e)})
    except Exception as e:
        _exception(str(e))
        return JsonResponse({'status': 'failure', 'reason': str(e)})


@login_required
def edit_recurring(request, id):
    try:
        subscription = get_object_or_404(Subscription, id=id)
        # Form object is initialized according to the specific gateway and if request.method=='POST'
        form = InitEditRecurringPaymentForm(request, subscription)
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
    except ValueError as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
    except RuntimeError as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
    except Exception as e:
        _exception(str(e))
        messages.add_message(request, messages.ERROR, str(e))
    return render(request, getEditRecurringPaymentHtml(subscription), {'form': form, 'subscription': subscription})


@login_required
def my_onetime_donations(request):
    # deleted=False should be valid whether soft-delete mode is on or off
    # previously deleted records should still be hidden even soft-delete mode is turned off afterwards
    donations = Donation.objects.filter(
        user=request.user, is_recurring=False, deleted=False).order_by('-donation_date')
    siteSettings = getSiteSettings(request)
    return render(request, 'donations/my_onetime_donations.html', {'donations': donations, 'siteSettings': siteSettings})


@login_required
def my_recurring_donations(request):
    # deleted=False should be valid whether soft-delete mode is on or off
    subscriptions = Subscription.objects.filter(
        user=request.user, deleted=False).order_by('-created_at')
    siteSettings = getSiteSettings(request)
    return render(request, 'donations/my_recurring_donations.html', {'subscriptions': subscriptions, 'siteSettings': siteSettings})


@login_required
def my_renewals(request, id):
    # deleted=False should be valid whether soft-delete mode is on or off
    subscription = get_object_or_404(Subscription, id=id, deleted=False)
    renewals = Donation.objects.filter(
        subscription=subscription, deleted=False).order_by('-donation_date')
    siteSettings = getSiteSettings(request)
    return render(request, 'donations/my_renewals.html', {'subscription': subscription, 'renewals': renewals, 'siteSettings': siteSettings})
