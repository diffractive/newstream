# define Python custom-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class WebhookNotProcessedError(Error):
    """Raised when a certain webhook is not processed by newstream"""
    pass
