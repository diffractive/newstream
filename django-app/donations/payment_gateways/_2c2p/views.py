from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from newstream.functions import _exception
from donations.models import STATUS_COMPLETE, STATUS_CANCELLED, STATUS_REVOKED
from donations.payment_gateways._2c2p.factory import Factory_2C2P
from .functions import map2C2PPaymentStatus


@csrf_exempt
def verify_2c2p_response(request):
    try:
        gatewayManager = Factory_2C2P.initGatewayByVerification(request)
        return gatewayManager.process_webhook_response()
    except ValueError as e:
        _exception(str(e))
        return HttpResponse(status=400)
    except RuntimeError as e:
        _exception(str(e))
        return HttpResponse(status=500)
    except Exception as e:
        _exception(str(e))
        return HttpResponse(status=500)


@csrf_exempt
def return_from_2c2p(request):
    try:
        gatewayManager = Factory_2C2P.initGatewayByReturn(request)
        request.session['return-donation-id'] = gatewayManager.donation.id
    
        if map2C2PPaymentStatus(gatewayManager.data['payment_status']) == STATUS_COMPLETE:
            return redirect('donations:thank-you')
        elif map2C2PPaymentStatus(gatewayManager.data['payment_status']) == STATUS_CANCELLED:
            return redirect('donations:cancelled')
        elif map2C2PPaymentStatus(gatewayManager.data['payment_status']) == STATUS_REVOKED:
            return redirect('donations:revoked')
        else:
            request.session['error-title'] = str(_("Unknown Error"))
            request.session['error-message'] = str(_(
                "Could not determine how to treat payment status: "+map2C2PPaymentStatus(gatewayManager.data['payment_status'])))
    except ValueError as e:
        _exception(str(e))
        request.session['error-title'] = str(_("ValueError"))
        request.session['error-message'] = str(e)
    except Exception as e:
        _exception(str(e))
        request.session['error-title'] = str(_("Unknown Error"))
        request.session['error-message'] = str(e)
    return redirect('donations:thank-you')

