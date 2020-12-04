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


# For persisting session in testing clients
# https://gist.github.com/stephenmcd/1702592
class PersistentSessionClient(Client):
    @property
    def session(self):
        if not hasattr(self, "_persisted_session"):
            engine = import_module(settings.SESSION_ENGINE)
            self._persisted_session = engine.SessionStore("persistent")
        return self._persisted_session