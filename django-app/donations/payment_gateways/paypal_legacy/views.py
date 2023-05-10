from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from newstream.functions import _exception
from donations.payment_gateways import Factory_Paypal_Legacy


@csrf_exempt
def verify_paypal_legacy_response(request):
    try:
        # Set up gateway manager object with its linking donation, session, etc...
        gatewayManager = Factory_Paypal_Legacy.initGatewayByVerification(request)

        if gatewayManager:
            return gatewayManager.process_webhook_response()
        else:
            raise Exception(_('gatewayManager for paypal-legacy not initialized.'))
    except ValueError as error:
        _exception(str(error))
        return HttpResponse(status=500)
    except Exception as error:
        _exception(str(error))
        return HttpResponse(status=500)
