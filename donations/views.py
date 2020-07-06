from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
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

            # email verification if is_create_account
            if gatewayManager.donation.is_create_account:
                sendVerificationEmail(
                    request, gatewayManager.donation.donor.linked_user)

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
        # logs donor in if is_create_account
        if donation.donor.linked_user:
            login(request, donation.donor.linked_user)
        return render(request, 'donations/thankyou.html', {'isValid': True, 'donation': donation})
    if 'thankyou-error' in request.session:
        return render(request, 'donations/thankyou.html', {'isValid': False, 'error_message': request.session['thankyou-error']})
    return render(request, 'donations/thankyou.html', {'isValid': False, 'error_message': 'No Payment Data is received.'})


def donate(request):
    # todo: need to display the currency symbol in template
    # todo: allow custom value in fixed_steps payment option
    form_template = 'donations/donation_form.html'
    try:
        form_blueprint = DonationForm.objects.get(
            is_active__exact=True)
    except Exception as e:
        print("There should be exactly one active DonationForm.", flush=True)
        raise e
    if request.method == 'POST':
        form = DonationWebForm(
            request.POST, request=request, blueprint=form_blueprint, label_suffix='')
        if form.is_valid():
            # process meta data
            donation_metas = []
            donor_metas = []
            for key, val in request.POST.items():
                donationmeta_key = re.match("^donationmeta_([a-z_]+)$", key)
                donormeta_key = re.match("^donormeta_([a-z_]+)$", key)
                if donationmeta_key:
                    donation_metas.append(DonationMeta(
                        field_key=donationmeta_key.group(1), field_value=val))
                if donormeta_key:
                    donor_metas.append(DonorMeta(
                        field_key=donormeta_key.group(1), field_value=val))

            # uses existing donor record if user logged in
            if request.user.is_authenticated:
                try:
                    donor = Donor.objects.get(
                        linked_user=request.user, email=request.user.email)
                except Donor.DoesNotExist as e:
                    # Should rarely happens, a registered user must have a linked donor record
                    print('Server logic error: '+str(e), flush=True)
                    form.add_error(
                        None, 'Server Error, cannot find previous donor records. Please contact site administrator.')
                    return render(request, form_template, {'form': form, 'donation_details_fields': DONATION_DETAILS_FIELDS, 'personal_info_fields': PERSONAL_INFO_FIELDS, 'other_fields': OTHER_FIELDS})
            else:
                # Finds if there's an existing email in donors
                try:
                    donor = Donor.objects.get(email=form.cleaned_data['email'])
                    # update donor metas from form inputs, has to do it by field, will lead to loss of Other Names if overwrite on the whole
                    for dm in donor_metas:
                        dmObj = DonorMeta.objects.get(
                            donor=donor, field_key=dm.field_key)
                        dmObj.field_value = dm.field_value
                        dmObj.save()
                    if form.cleaned_data['first_name'] != donor.first_name or form.cleaned_data['last_name'] != donor.last_name:
                        # Save form inputs as "Other Name" at original donor record
                        donorMeta = DonorMeta(donor=donor,
                                              field_key="Other Name", field_value=form.cleaned_data['first_name']+" "+form.cleaned_data['last_name'])
                        donorMeta.save()
                    donor.save()
                except Donor.DoesNotExist as e:
                    # creates a new donor
                    donor = Donor(
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        email=form.cleaned_data['email'],
                        opt_in_mailing_list=form.cleaned_data['opt_in_mailing_list'],
                        metas=donor_metas
                    )
                    donor.save()

                # check if need to create account
                if form.cleaned_data['is_create_account']:
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
                    except Exception as e:
                        print("Cannot Create new Django user: " +
                              str(e), flush=True)
                        # Should have been checked against duplication in form validation
                        # double check again for safety
                        form.add_error(None, str(e))
                        return render(request, form_template, {'form': form, 'donation_details_fields': DONATION_DETAILS_FIELDS, 'personal_info_fields': PERSONAL_INFO_FIELDS, 'other_fields': OTHER_FIELDS})

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
                donation_amount=form.cleaned_data['donation_amount'],
                currency=form.cleaned_data['currency'],
                is_create_account=form.cleaned_data['is_create_account'] if 'is_create_account' in form.cleaned_data else False,
                payment_status=STATUS_PENDING,
                metas=donation_metas
            )
            try:
                donation.save()
            except Exception as e:
                # Should rarely happen, but in case some bugs or order id repeats itself
                print(str(e), flush=True)
                form.add_error(None, 'Server error, please retry.')
                return render(request, form_template, {'form': form, 'donation_details_fields': DONATION_DETAILS_FIELDS, 'personal_info_fields': PERSONAL_INFO_FIELDS, 'other_fields': OTHER_FIELDS})

            # redirect to payment_gateway
            gatewayManager = PaymentGatewayFactory.initGateway(
                request, donation)
            return gatewayManager.redirect_to_gateway_url()
        else:
            pprint(form.errors)
    else:
        form = DonationWebForm(
            request=request, blueprint=form_blueprint, label_suffix='')

    # see: https://docs.djangoproject.com/en/3.0/ref/forms/api/#django.forms.Form.field_order
    form.order_fields(
        ['donation_amount', 'donation_frequency', 'payment_gateway'])
    return render(request, form_template, {'form': form, 'donation_details_fields': DONATION_DETAILS_FIELDS, 'personal_info_fields': PERSONAL_INFO_FIELDS, 'other_fields': OTHER_FIELDS})


@login_required
def my_donations(request):
    # todo: handle updating/cancelling recurring payments
    donations = Donation.objects.filter(
        donor__linked_user=request.user).order_by('-created_at')
    return render(request, 'donations/my_donations.html', {'donations': donations})
