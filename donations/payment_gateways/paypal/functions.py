import json
from paypalcheckoutsdk.core import PayPalHttpClient
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalhttp import HttpError

from donations.payment_gateways.setting_classes import getPayPalSettings
from newstream.functions import printvars, _debug, _error


def capture_paypal_order(request, order_id):
    """Method to capture order using order_id"""
    paypalSettings = getPayPalSettings(request)
    client = PayPalHttpClient(paypalSettings.environment)

    req = OrdersCaptureRequest(order_id)
    # The following line is for mocking negative responses
    # req.headers['PayPal-Mock-Response'] = '{"mock_application_codes":"INTERNAL_SERVER_ERROR"}'
    _debug('PayPal: Capture Order')
    try:
        response = client.execute(req)
    except IOError as ioe:
        fail_reason = str(ioe)
        if isinstance(ioe, HttpError):
            # Something went wrong server-side
            httpError = json.loads(ioe.message)
            if 'details' in httpError and len(httpError['details']) > 0:
                fail_reason = "{}: {}".format(httpError['details'][0]['issue'], httpError['details'][0]['description'])
        raise IOError(fail_reason)
    return response.result.status
