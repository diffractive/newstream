import datetime

from pythonjsonlogger import jsonlogger

# customer log formatter
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        # super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        for field in self._required_fields:
            if field in self.rename_fields:
                log_record[self.rename_fields[field]] = record.__dict__.get(field)
            else:
                log_record[field] = record.__dict__.get(field)
        log_record.update(self.static_fields)
        log_record.update(message_dict)

        if hasattr(record, 'request'):
            if hasattr(record.request, 'user') and hasattr(record.request.user, 'uuid'):
                log_record['usr'] = {'id': record.request.user.uuid.__str__()}
            log_record['http'] = {
                'url': record.request.build_absolute_uri(),
                'method': record.request.method,
                # 'request_id':         string  The ID of the HTTP request.
            }

            if record.request.META.get('SERVER_PROTOCOL'):
                log_record['http']['version'] = record.request.META['SERVER_PROTOCOL']

            if record.request.META.get('HTTP_REFERER'):
                log_record['http']['referer'] = record.request.META['HTTP_REFERER']

            if record.request.META.get('HTTP_USER_AGENT'):
                log_record['http']['useragent'] = record.request.META['HTTP_USER_AGENT']

            if hasattr(record, 'status_code'):
                log_record['http']['status_code'] = record.status_code

        log_record['timestamp'] = datetime.datetime.utcfromtimestamp(record.created)
        log_record['level'] = record.levelname
        log_record['name'] = record.name
