import datetime

from pythonjsonlogger import jsonlogger
from django.conf import settings
from crum import get_current_request

# customer log formatter
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        for field in self._required_fields:
            if field in self.rename_fields:
                log_record[self.rename_fields[field]] = record.__dict__.get(field)
            else:
                log_record[field] = record.__dict__.get(field)
        log_record.update(self.static_fields)
        log_record.update(message_dict)

        request = get_current_request()

        if request:
            if hasattr(request, 'user') and hasattr(request.user, 'id'):
                log_record['usr'] = {'id': request.user.id}

                # We don't want to record end user's e-mails only admins.
                if request.user.is_staff:
                    log_record['usr']['email'] = request.user.email
            log_record['http'] = {
                'url': request.build_absolute_uri(),
                'method': request.method,
                # 'request_id':         string  The ID of the HTTP request.
            }

            if request.META.get('SERVER_PROTOCOL'):
                log_record['http']['version'] = request.META['SERVER_PROTOCOL']

            if request.META.get('HTTP_REFERER'):
                log_record['http']['referer'] = request.META['HTTP_REFERER']

            if request.META.get('HTTP_USER_AGENT'):
                log_record['http']['useragent'] = request.META['HTTP_USER_AGENT']

            if hasattr(record, 'status_code'):
                log_record['http']['status_code'] = record.status_code

        log_record['timestamp'] = datetime.datetime.utcfromtimestamp(record.created)
        log_record['level'] = record.levelname
        log_record['name'] = record.name
        if hasattr(settings, 'APP_VERSION'):
            log_record['version'] = settings.APP_VERSION
