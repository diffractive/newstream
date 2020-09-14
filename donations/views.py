import re
import secrets
import json
from pprint import pprint
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt

from newstream.functions import getSiteSettings, printvars
from site_settings.models import PaymentGateway
from .models import *
from .forms import *
from .functions import *
from donations.payment_gateways import InitPaymentGateway
User = get_user_model()


def thank_you(request):
    if 'return-donation-id' in request.session:
        donation = Donation.objects.get(
            pk=request.session['return-donation-id'])
        # logs user in
        if donation.user:
            login(request, donation.user,
                  backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'donations/thankyou.html', {'isValid': True, 'isFirstTime': donation.is_user_first_donation, 'donation': donation})
    if 'return-error' in request.session:
        return render(request, 'donations/thankyou.html', {'isValid': False, 'error_message': request.session['return-error']})
    return render(request, 'donations/thankyou.html', {'isValid': False, 'error_message': _('No Payment Data is received.')})


def cancelled(request):
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
    if 'return-error' in request.session:
        return render(request, 'donations/cancelled.html', {'isValid': False, 'error_message': request.session['return-error']})
    return render(request, 'donations/cancelled.html', {'isValid': False, 'error_message': _('No Payment Data is received.')})


def donate(request):
    if request.user.is_authenticated:
        # skip step 1 (personal info) and go to step 2 (donation details)
        return redirect('donations:donation-details')
    else:
        # show login or sign-up options page
        return render(request, 'donations/signin_method.html')


@login_required
@csrf_exempt
def cancel_recurring(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        if 'subscription_id' not in json_data:
            print("No subscription_id in JSON body", flush=True)
            return HttpResponse(status=400)
        subscription_id = int(json_data['subscription_id'])
        subscription = get_object_or_404(Subscription, id=subscription_id)
        gatewayManager = InitPaymentGateway(
                    request, subscription=subscription)
        resultSet = gatewayManager.cancel_recurring_payment()
        if resultSet['status']:
            return JsonResponse({'status': 'success', 'button-html': str(_('View all renewals')), 'recurring-status': str(_(STATUS_CANCELLED.capitalize())), 'button-href': reverse('donations:my-renewals', kwargs={'id': subscription_id})})
        else:
            return JsonResponse({'status': 'failure', 'reason': resultSet['reason']})
    else:
        return HttpResponse(400)


def donation_details(request):
    # todo: allow custom value in fixed_steps payment option
    if not request.user.is_authenticated:
        return redirect('donations:donate')
    form_template = 'donations/donation_details_form.html'
    try:
        form_blueprint = DonationForm.objects.get(
            is_active__exact=True)
    except Exception as e:
        print("There should be exactly one active DonationForm.", flush=True)
        raise e
    if request.method == 'POST':
        form = DonationDetailsForm(
            request.POST, request=request, blueprint=form_blueprint, label_suffix='')
        if form.is_valid():
            # process meta data
            donation_metas = process_donation_meta(request)

            # create pending donation
            payment_gateway = PaymentGateway.objects.get(
                pk=form.cleaned_data['payment_gateway'])
            order_id = gen_order_id(gateway=payment_gateway)
            donation = Donation(
                order_number=order_id,
                user=request.user,
                form=form_blueprint,
                gateway=payment_gateway,
                is_recurring=True if form.cleaned_data['donation_frequency'] == 'monthly' else False,
                donation_amount=form.cleaned_data['donation_amount'],
                currency=form.cleaned_data['currency'],
                payment_status=STATUS_PENDING,
                metas=donation_metas,
            )

            try:
                donation.save()

                if 'first_time_registration' in request.session:
                    dpmeta = DonationPaymentMeta(
                        donation=donation, field_key='is_user_first_donation', field_value=request.session['first_time_registration'])
                    dpmeta.save()
            except Exception as e:
                # Should rarely happen, but in case some bugs or order id repeats itself
                print(str(e), flush=True)
                form.add_error(None, 'Server error, please retry.')
                return render(request, form_template, {'form': form, 'donation_details_fields': DONATION_DETAILS_FIELDS})

            # redirect to payment_gateway
            gatewayManager = InitPaymentGateway(
                request, donation=donation)
            return gatewayManager.redirect_to_gateway_url()
        else:
            pprint(form.errors)
    else:
        form = DonationDetailsForm(
            request=request, blueprint=form_blueprint, label_suffix='')

    # see: https://docs.djangoproject.com/en/3.0/ref/forms/api/#django.forms.Form.field_order
    form.order_fields(
        ['donation_amount', 'donation_frequency', 'payment_gateway'])
    return render(request, form_template, {'form': form, 'donation_details_fields': DONATION_DETAILS_FIELDS})


@login_required
def my_onetime_donations(request):
    # todo: separate one-time and recurring donations, with a sidebar like in my profile
    donations = Donation.objects.filter(
        user=request.user, is_recurring=False).order_by('-created_at')
    siteSettings = getSiteSettings(request)
    return render(request, 'donations/my_onetime_donations.html', {'donations': donations, 'siteSettings': siteSettings})


@login_required
def my_recurring_donations(request):
    # todo: separate one-time and recurring donations, with a sidebar like in my profile
    subscriptions = Subscription.objects.filter(user=request.user).order_by('-created_at')
    siteSettings = getSiteSettings(request)
    return render(request, 'donations/my_recurring_donations.html', {'subscriptions': subscriptions, 'siteSettings': siteSettings})


@login_required
def my_renewals(request, id):
    subscription = get_object_or_404(Subscription, id=id)
    renewals = Donation.objects.filter(subscription=subscription).order_by('-created_at')
    siteSettings = getSiteSettings(request)
    return render(request, 'donations/my_renewals.html', {'subscription': subscription, 'renewals': renewals, 'siteSettings': siteSettings})
