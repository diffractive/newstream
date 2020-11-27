import json
from django.test import TestCase

from newstream.functions import printvars

class PayPalApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        # cls.foo = Foo.objects.create(bar="Test")
        pass

    def testCreateProduct(self):
        # Some test using self.foo
        response = self.client.get('/en/donations/create-prod-during-transaction/')
        self.assertEqual(response.status_code, 200)

    def testGetProduct(self):
        response = self.client.get('/en/donations/get-prod-during-transaction/')
        self.assertEqual(response.status_code, 200)

    def testSubscriptionActions(self):
        # create subscription
        response = self.client.get('/en/donations/create-subscription-during-transaction/')
        result = json.loads(response.content.decode('utf-8'))
        self.assertTrue(result['approval_link'])