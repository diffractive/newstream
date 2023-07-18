# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import requests
import os


class PayPal:
    def __init__(self):
        self.api_url = os.getenv('PAYPAL_API_BASE')

    def simulate_next_payment_cycle(self, sub_id, payment_result):
        """
        Simulate next payment cycle of a subscription, provided with a specified payment result
        payment_result is either "success" | "failure"
        """
        # We get subscription to get customer_id
        _ = requests.post(self.api_url + f'/advance-subscription-cycle/{sub_id}', json={"payment_result": payment_result})
