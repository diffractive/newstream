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


class Localstripe:
    def __init__(self):
        test_key = 'sk_TEST_SECRET_KEY'
        self.auth = requests.auth.HTTPBasicAuth(test_key, '')
        self.api_url = 'http://localstripe.newstream.local:8420/v1/'
        
    def update_to_failing_card(self, sub_id):
        """
        Takes a subscription and creates a new payment method that will fail payment and attaches to user of provided subscription
        """
        # We get subscription to get customer_id 
        sub = requests.get(self.api_url + f'subscriptions/{sub_id}', auth=self.auth).json()
        
        # We get customer data to create the payment method
        cus_id = sub['customer']
        customer = requests.get(self.api_url + f'customers/{cus_id}', auth=self.auth).json()
        
        # Create payment method
        pm_data = {
            "type": "card",
            "billing_details": {
                "name": customer['name'],
                "email": customer['email']
            },
            "card": {
                "number": '4000000000000341', # This is a test card that fails
                "cvc": "123",
                "exp_month": "01",
                "exp_year": "33" # Needs to be in the future
            }
        }
        pm = requests.post(self.api_url + 'payment_methods', auth=self.auth, json=pm_data).json()
        pm_id = pm['id']
        
        # Attach new payment method to customer
        requests.post(self.api_url + f'payment_methods/{pm_id}', auth=self.auth, json={"customer": cus_id})
        requests.post(self.api_url + f'customers/{cus_id}', auth=self.auth, json={"invoice_settings": {'default_payment_method': pm_id}})
    
    def update_to_working_card(self, sub_id):
        """
        Takes a subscription and creates a new payment method that will succeed and attaches to user of provided subscription
        """
        """
        Takes a subscription and creates a new payment method that will fail payment and attaches to user of provided subscription
        """
        # We get subscription to get customer_id 
        sub = requests.get(self.api_url + f'subscriptions/{sub_id}', auth=self.auth).json()
        
        # We get customer data to create the payment method
        cus_id = sub['customer']
        customer = requests.get(self.api_url + f'customers/{cus_id}', auth=self.auth).json()
        
        # Create payment method
        pm_data = {
            "type": "card",
            "billing_details": {
                "name": customer['name'],
                "email": customer['email']
            },
            "card": {
                "number": '4242424242424242', # This is a card that will succeed
                "cvc": "123",
                "exp_month": "01",
                "exp_year": "33" # Needs to be in the future
            }
        }
        pm = requests.post(self.api_url + 'payment_methods', auth=self.auth, json=pm_data).json()
        pm_id = pm['id']
        
        # Attach new payment method to customer
        requests.post(self.api_url + f'payment_methods/{pm_id}', auth=self.auth, json={"customer": cus_id})
        requests.post(self.api_url + f'customers/{cus_id}', auth=self.auth, json={"invoice_settings": {'default_payment_method': pm_id}})


