from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse
from .models import *
from .forms import *
from .functions import *
from .payment_gateways.gateway_factory import PaymentGatewayFactory
from pprint import pprint
import secrets
import re


def verify_gateway_response(request):
    gatewayManager = PaymentGatewayFactory.initGatewayByVerification(request)
    isVerified = gatewayManager.verify_gateway_response()
    return HttpResponse(status=200) if isVerified else HttpResponse(status=400)


def thank_you(request):
    gatewayManager = PaymentGatewayFactory.initGatewayByVerification(request)
    if gatewayManager:
        isVerified = gatewayManager.verify_gateway_response()
        context = {'isVerified': isVerified,
                   'donation': gatewayManager.donation}
    else:
        isVerified = False
        context = {'isVerified': isVerified}
    return render(request, 'donations/thankyou.html',
                  context)


def onetime_form(request):
    form_blueprint = DonationForm.objects.filter(is_recurring__exact=False)[0]
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
                currency='HARDCODE',  # todo: find a way to save currency values
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
                return render(request, 'donations/onetime_form.html', {'form': form})

            # redirect to payment_gateway
            gatewayManager = PaymentGatewayFactory.initGateway(
                request, donation)
            return gatewayManager.redirect_to_gateway_url()
        else:
            pprint(form.errors)
    else:
        form = DonationWebForm(blueprint=form_blueprint)
        form.is_recurring = False

    return render(request, 'donations/onetime_form.html', {'form': form})


def recurring_form(request):
    return 'HI'
