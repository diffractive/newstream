from django.conf import settings
from django.utils import translation
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from donations.payment_gateways._2c2p.factory import Factory_2C2P
from donations.functions import sendDonationNotifToAdmins, sendDonationReceipt


@csrf_exempt
def verify_2c2p_response(request):
    gatewayManager = Factory_2C2P.initGatewayByVerification(request)
    if gatewayManager:
        isVerified = gatewayManager.process_webhook_response()
        if isVerified:
            # set default language for admins' emails
            translation.activate(settings.LANGUAGE_CODE)

            # todo: should make this an option toggle in site_settings
            # email new donation notification to admin list
            # only when the donation is brand new, not counting in recurring renewals
            # if not gatewayManager.donation.parent_donation:
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


@csrf_exempt
def return_from_2c2p(request):
    gatewayManager = Factory_2C2P.initGatewayByVerification(request)
    if gatewayManager:
        isVerified = gatewayManager.process_webhook_response()
        if isVerified:
            request.session['return-donation-id'] = gatewayManager.donation.id
        else:
            request.session['return-error'] = str(_(
                "Results returned from gateway is invalid."))
    else:
        request.session['return-error'] = str(_(
            "Could not determine payment gateway from request"))
    # todo: should distinguish response like cancelled or errored from thankyou
    return redirect('donations:thank-you')