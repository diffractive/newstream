from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.views import PasswordResetView
from .models import *
from .forms import *
from .functions import *
from newstream.functions import getFullReverseUrl
from .payment_gateways.gateway_factory import PaymentGatewayFactory
from pprint import pprint
import secrets
import re
User = get_user_model()


class CustomPasswordResetView(PasswordResetView):
    def __init__(self, *args, **kwargs):
        self.from_email = getSuperUserEmail()
        super().__init__(*args, **kwargs)


def verify_gateway_response(request):
    gatewayManager = PaymentGatewayFactory.initGatewayByVerification(request)
    if gatewayManager:
        isVerified = gatewayManager.verify_gateway_response()
        if isVerified:
            # email new donation notification to admin list
            # only when the donation is brand new, not counting in recurring renewals
            if not gatewayManager.donation.parent_donation:
                sendDonationNotifToAdmins(request, gatewayManager.donation)

            # email thank you receipt to donor
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
            request.session['thankyou-error'] = "Results returned from gateway is invalid."
    else:
        request.session['thankyou-error'] = "Could not determine payment gateway from request"
    return redirect('donations:thank-you')


def thank_you(request):
    if 'thankyou-donation-id' in request.session:
        donation = Donation.objects.get(
            pk=request.session['thankyou-donation-id'])
        # logs donor in
        if donation.donor.linked_user:
            login(request, donation.donor.linked_user)
        return render(request, 'donations/thankyou.html', {'isValid': True, 'isFirstTime': donation.is_user_first_donation, 'donation': donation})
    if 'thankyou-error' in request.session:
        return render(request, 'donations/thankyou.html', {'isValid': False, 'error_message': request.session['thankyou-error']})
    return render(request, 'donations/thankyou.html', {'isValid': False, 'error_message': 'No Payment Data is received.'})


def donate(request):
    if request.user.is_authenticated:
        # skip step 1 (personal info) and go to step 2 (donation details)
        return redirect('donations:donation-details')
    else:
        # show login or sign-up options page
        return render(request, 'donations/signin_method.html')


def personal_info(request):
    form_template = 'donations/personal_info_form.html'
    try:
        form_blueprint = DonationForm.objects.get(
            is_active__exact=True)
    except Exception as e:
        print("There should be exactly one active DonationForm.", flush=True)
        raise e
    if request.method == 'POST':
        form = PersonalInfoForm(
            request.POST, request=request, blueprint=form_blueprint, label_suffix='')
        # if form is valid, this should mean the email is brand new in the system
        if form.is_valid():
            # process meta data
            donor_metas = []
            for key, val in request.POST.items():
                donormeta_key = re.match("^donormeta_([a-z_]+)$", key)
                if donormeta_key:
                    donor_metas.append(DonorMeta(
                        field_key=donormeta_key.group(1), field_value=val))

            # creates a new donor
            donor = Donor(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                opt_in_mailing_list=form.cleaned_data['opt_in_mailing_list'],
                metas=donor_metas
            )
            donor.save()

            # proceed to create account
            try:
                generated_pwd = secrets.token_hex(10)
                donor_user = User.objects.create_user(
                    email=donor.email, password=generated_pwd)
                donor_user.first_name = donor.first_name
                donor_user.last_name = donor.last_name
                donor_user.opt_in_mailing_list = donor.opt_in_mailing_list
                donor_user.save()
                # link donor to user
                donor.linked_user = donor_user
                donor.save()
                # save to session to remember user's registration
                request.session['first_time_registration'] = True
            except Exception as e:
                print("Cannot Create new Django user: " +
                      str(e), flush=True)
                # Should have been checked against duplication in form validation
                # double check again for safety
                form.add_error(None, str(e))
                return render(request, form_template, {'form': form, 'personal_info_fields': PERSONAL_INFO_FIELDS, 'other_fields': OTHER_FIELDS})

            # logs new user in
            login(request, donor_user)

            # email verification to user
            sendVerificationEmail(
                request, donor_user)

            # redirects to donation-details (step 2)
            return redirect('donations:donation-details')
        else:
            pprint(form.errors)
    else:
        form = PersonalInfoForm(
            request=request, blueprint=form_blueprint, label_suffix='')

    return render(request, form_template, {'form': form, 'personal_info_fields': PERSONAL_INFO_FIELDS, 'other_fields': OTHER_FIELDS})


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
            donation_metas = []
            for key, val in request.POST.items():
                donationmeta_key = re.match("^donationmeta_([a-z_]+)$", key)
                if donationmeta_key:
                    donation_metas.append(DonationMeta(
                        field_key=donationmeta_key.group(1), field_value=val))

            # get user's current donor record
            try:
                donor = Donor.objects.get(email__exact=request.user.email)
            except Exception as e:
                print("Cannot find user's linked donor: " +
                      str(e), flush=True)
                form.add_error(None, str(e))
                return render(request, form_template, {'form': form, 'donation_details_fields': DONATION_DETAILS_FIELDS})

            # create pending donation
            payment_gateway = PaymentGateway.objects.get(
                pk=form.cleaned_data['payment_gateway'])
            order_id = gen_order_id(gateway=payment_gateway)
            donation = Donation(
                order_number=order_id,
                donor=donor,
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
        donor__linked_user=request.user).order_by('-created_at')
    return render(request, 'donations/my_donations.html', {'donations': donations})
