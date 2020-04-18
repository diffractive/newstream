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


def process_donation_submission(request, is_recurring):
    # todo: need to display the currency symbol in template
    form_template = 'donations/recurring_form.html' if is_recurring else 'donations/onetime_form.html'
    form_blueprint = DonationForm.objects.filter(
        is_recurring__exact=is_recurring)[0]
    if request.method == 'POST':
        form = DonationWebForm(request.POST, blueprint=form_blueprint)
        if form.is_valid():
            # create a donor
            donor = Donor(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                opt_in_mailing_list=form.cleaned_data['opt_in_mailing_list']
            )
            try:
                donor.save()
            except IntegrityError:
                # get previous donor in db
                donor = Donor.objects.filter(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email']
                )[0]

            # check if need to create account
            if form.cleaned_data['is_create_account']:
                try:
                    # use email as the username
                    generated_pwd = secrets.token_hex(10)
                    donor_user = User.objects.create_user(
                        username=donor.email, email=donor.email, password=generated_pwd)
                except Exception as e:
                    print("Cannot Create new Django user: "+str(e), flush=True)
                    # very likely duplicate username (this email has previously been registered as user)
                    donor_user = User.objects.get(username=donor.email)
                # link donor to user
                donor.linked_user = donor_user
                donor.save()
            else:
                try:
                    donor_user = User.objects.get(username=donor.email)
                except Exception as e:
                    print("No previous accounts registered for " +
                          donor.email+". "+str(e), flush=True)
                else:
                    donor.linked_user = donor_user
                    donor.save()

            # create pending donation
            payment_gateway = PaymentGateway.objects.get(
                pk=form.cleaned_data['payment_gateway'])
            order_id = gen_order_id(gateway=payment_gateway)
            donation_metas = []
            for key, val in request.POST.items():
                more_field_key = re.match("^omp_more_([a-z_]+)$", key)
                if more_field_key:
                    donation_metas.append(DonationMeta(
                        field_key=more_field_key.group(1), field_value=val))
            donation = Donation(
                order_number=order_id,
                donor=donor,
                form=form_blueprint,
                gateway=payment_gateway,
                is_recurring=form.cleaned_data['is_recurring'],
                donation_amount=form.cleaned_data['donation_amount'],
                currency=getGlobalSettings(request).currency,
                is_create_account=form.cleaned_data['is_create_account'],
                payment_status=STATUS_PENDING,
                metas=donation_metas
            )
            try:
                donation.save()
            except Exception as e:
                # Should rarely happen, but in case some bugs or order id repeats itself
                print(str(e))
                form.add_error(None, 'Server error, please retry.')
                return render(request, form_template, {'form': form})

            # redirect to payment_gateway
            gatewayManager = PaymentGatewayFactory.initGateway(
                request, donation)
            return gatewayManager.redirect_to_gateway_url()
        else:
            pprint(form.errors)
    else:
        form = DonationWebForm(blueprint=form_blueprint)
        form.is_recurring = True

    return render(request, form_template, {'form': form})


def onetime_form(request):
    return process_donation_submission(request, False)


def recurring_form(request):
    return process_donation_submission(request, True)


@login_required
def manage_donations(request):
    donations = Donation.objects.filter(
        donor__linked_user=request.user).order_by('-created_at')
    return render(request, 'donations/manage-donations.html', {'donations': donations})
