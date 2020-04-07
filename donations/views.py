from django.shortcuts import render
from django.db import IntegrityError
from .models import *
from .forms import *
from pprint import pprint
import secrets, re


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
            payment_gateway = PaymentGateway.objects.get(pk=form.cleaned_data['payment_gateway'])
            if payment_gateway.title == GATEWAY_2C2P:
                order_id = secrets.token_hex(10)
            elif payment_gateway.title == GATEWAY_PAYPAL:
                order_id = secrets.token_hex(16)
            elif payment_gateway.title == GATEWAY_STRIPE:
                order_id = secrets.token_hex(16)
            else:
                order_id = secrets.token_hex(16)
            donation_metas = []
            for key, val in request.POST.items():
                more_field_key = re.match("^omp_more_([a-z_]+)$", key)
                if more_field_key:
                    donation_metas.append(DonationMeta(field_key=more_field_key.group(1), field_value=val))
            donation = Donation(
                order_number=order_id,
                donor=donor,
                form=form_blueprint,
                gateway=payment_gateway,
                is_recurring=form.cleaned_data['is_recurring'],
                donation_amount=form.cleaned_data['donation_amount'],
                currency='HARDCODE', # todo: find a way to save currency values
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

            # todo: redirect to payment_gateway
            return render(request, 'donations/thankyou.html')
        else:
            pprint(form.errors)
    else:
        form = DonationWebForm(blueprint=form_blueprint)
        form.is_recurring = False

    return render(request, 'donations/onetime_form.html', {'form': form})


def recurring_form(request):
    return 'HI'
