from donations.payment_gateways.gateway_manager import PaymentGatewayManager


class Gateway_Paypal(PaymentGatewayManager):
    def __init__(self, request, donation=None, subscription=None, **kwargs):
        super().__init__(request, donation, subscription)

    def redirect_to_gateway_url(self):
        pass

    def process_webhook_response(self):
        pass

    def update_recurring_payment(self):
        pass

    def cancel_recurring_payment(self):
        pass
