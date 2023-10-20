import logging
from crum import CurrentRequestUserMiddleware

logger = logging.getLogger("newstream.middleware")

class RequestLoggerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.request_logger = logging.getLogger("newstream.request")

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # We only log the status code, the request of the http request information
        # is added by our custom log formatter

        extra = {
            'http': {
                'status_code': response.status_code,
            }
        }

        log_level = logging.INFO
        if response.status_code >= 500:
            log_level = logging.ERROR
        elif response.status_code >= 400:
            log_level = logging.WARNING

        self.request_logger.log(
            log_level,
            f"{request.method} {request.get_full_path()} [{response.status_code}]",
            extra=extra)

        return response


class NewstreamCurrentRequestUserMiddleware(CurrentRequestUserMiddleware):
    """ We override crum.CurrentRequestUserMiddleware to leave the
        request object set when there is an exception. This means that the
        django exception handler / logger can access request.user, for
        adding debug context
    """

    def process_exception(self, request, exception):
        pass
