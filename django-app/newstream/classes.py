from importlib import import_module
from django.conf import settings
from django.test.client import Client


# define Python custom-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


# specific exception class for dealing with non-processed webhooks no matter what payment gateway it is
class WebhookNotProcessedError(Error):
    """Raised when a certain webhook is not processed by newstream"""
    pass


# specific exception class for webhook events missing newstream donation id
class WebhookMissingDonationIdError(Error):
    """Raised when a webhook event is missing a Newstream donation id
       pass the payment gateway subscription ID to the additional parameter "subscription_id" for logging and issue tracking
    """
    def __init__(self, message, subscription_id):
        self.message = message
        self.subscription_id = subscription_id


# specific exception class for webhook events of subscriptions not existing on Newstream
class SubscriptionNotExistError(Error):
    """Raised when a webhook event is from a subscription not existing on Newstream
       pass the payment gateway subscription ID to the additional parameter "subscription_id" for logging and issue tracking
    """
    def __init__(self, message, subscription_id):
        self.message = message
        self.subscription_id = subscription_id


# For persisting session in testing clients
# https://gist.github.com/stephenmcd/1702592
class PersistentSessionClient(Client):
    @property
    def session(self):
        if not hasattr(self, "_persisted_session"):
            engine = import_module(settings.SESSION_ENGINE)
            self._persisted_session = engine.SessionStore("persistent")
        return self._persisted_session