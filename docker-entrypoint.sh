#!/bin/sh

set -e

: "${NEWSTREAM_RUN_MIGRATIONS:=1}"
: "${NEWSTREAM_COLLECT_STATIC:=1}"
: "${DJANGO_SUPERUSER_EMAIL:=""}"
: "${DJANGO_SUPERUSER_PASSWORD:=""}"

if [ "$NEWSTREAM_COLLECT_STATIC" -eq 1 ]; then
    python manage.py collectstatic --noinput
fi

if [ "$NEWSTREAM_RUN_MIGRATIONS" -eq 1 ]; then
    python manage.py migrate --noinput
fi

if [ "x$DJANGO_SUPERUSER_EMAIL" != x ]; then
    python manage.py createsuperuser --noinput || true
fi

# gunicorn --log-level DEBUG newstream.wsgi:application
gunicorn --bind 0.0.0.0:8000 --log-level DEBUG newstream.wsgi:application
