import re
import secrets
from pprint import pprint
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.utils.translation import gettext_lazy as _
from django.utils import translation

from newstream.functions import getFullReverseUrl
from .models import *
from .forms import *
from .functions import *
from .payment_gateways.gateway_factory import PaymentGatewayFactory
User = get_user_model()


def verify_gateway_response(request):
    gatewayManager = PaymentGatewayFactory.initGatewayByVerification(request)
    if gatewayManager:
        isVerified = gatewayManager.verify_gateway_response()
        if isVerified:
            # email new donation notification to admin list
            # only when the donation is brand new, not counting in recurring renewals
            if not gatewayManager.donation.parent_donation:
                sendDonationNotifToAdmins(request, gatewayManager.donation)

            # set language for donation_receipt.html
            user = gatewayManager.donation.user
            if user.language_preference:
                translation.activate(user.language_preference)

            # email thank you receipt to user
            sendDonationReceipt(request, gatewayManager.donation)

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=409)
    else:
        return HttpResponse(status=400)


def return_from_gateway(request):
    gatewayManager = PaymentGatewayFactory.initGatewayByVerification(request)
    if gatewayManager:
        isVerified = gatewayManager.verify_gateway_response()
        if isVerified:
            request.session['thankyou-donation-id'] = gatewayManager.donation.id
        else:
            request.session['thankyou-error'] = _(
                "Results returned from gateway is invalid.")
    else:
        request.session['thankyou-error'] = _(
            "Could not determine payment gateway from request")
    return redirect('donations:thank-you')


def thank_you(request):
    if 'thankyou-donation-id' in request.session:
        donation = Donation.objects.get(
            pk=request.session['thankyou-donation-id'])
        # logs user in
        if donation.user:
            login(request, donation.user,
                  backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'donations/thankyou.html', {'isValid': True, 'isFirstTime': donation.is_user_first_donation, 'donation': donation})
    if 'thankyou-error' in request.session:
        return render(request, 'donations/thankyou.html', {'isValid': False, 'error_message': request.session['thankyou-error']})
    return render(request, 'donations/thankyou.html', {'isValid': False, 'error_message': _('No Payment Data is received.')})


def donate(request):
    if request.user.is_authenticated:
        # skip step 1 (personal info) and go to step 2 (donation details)
        return redirect('donations:donation-details')
    else:
        # show login or sign-up options page
        return render(request, 'donations/signin_method.html')


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
                is_user_first_donation=request.session[
                    'first_time_registration'] if 'first_time_registration' in request.session else False,
                donation_amount=form.cleaned_data['donation_amount'],
                currency=form.cleaned_data['currency'],
                payment_status=STATUS_PENDING,
                metas=donation_metas
            )
            try:
                donation.save()
            except Exception as e:
                # Should rarely happen, but in case some bugs or order id repeats itself
                print(str(e), flush=True)
                form.add_error(None, 'Server error, please retry.')
                return render(request, form_template, {'form': form, 'donation_details_fields': DONATION_DETAILS_FIELDS})

            # redirect to payment_gateway
            gatewayManager = PaymentGatewayFactory.initGateway(
                request, donation)
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
def my_donations(request):
    # todo: handle updating/cancelling recurring payments
    donations = Donation.objects.filter(
        user=request.user).order_by('-created_at')
    return render(request, 'donations/my_donations.html', {'donations': donations})
