from django.conf import settings
from django.utils import translation
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from newstream.functions import printvars
from donations.models import STATUS_COMPLETE, STATUS_CANCELLED, STATUS_REVOKED
from donations.payment_gateways._2c2p.factory import Factory_2C2P
from donations.email_functions import sendDonationNotifToAdmins, sendDonationReceiptToDonor
from .functions import map2C2PPaymentStatus


@csrf_exempt
def verify_2c2p_response(request):
    gatewayManager = Factory_2C2P.initGatewayByVerification(request)
    if gatewayManager:
        return gatewayManager.process_webhook_response()
    return HttpResponse(status=400)


@csrf_exempt
def return_from_2c2p(request):
    gatewayManager = Factory_2C2P.initGatewayByReturn(request)
    if gatewayManager:
        request.session['return-donation-id'] = gatewayManager.donation.id
    else:
        request.session['return-error'] = str(_(
            "Could not determine payment gateway returning from 2C2P"))
    if map2C2PPaymentStatus(gatewayManager.data['payment_status']) == STATUS_COMPLETE:
        return redirect('donations:thank-you')
    elif map2C2PPaymentStatus(gatewayManager.data['payment_status']) == STATUS_CANCELLED:
        return redirect('donations:cancelled')
    elif map2C2PPaymentStatus(gatewayManager.data['payment_status']) == STATUS_REVOKED:
        return redirect('donations:revoked')
    else:
        request.session['return-error'] = str(_(
            "Could not determine how to treat payment status: "+map2C2PPaymentStatus(gatewayManager.data['payment_status'])))
        return redirect('donations:thank-you')

