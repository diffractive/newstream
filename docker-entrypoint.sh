#!/bin/sh

set -e

: "${RUN_MIGRATIONS:=1}"
: "${COLLECT_STATIC:=1}"
: "${SUPERUSER_EMAIL:=""}"
: "${SUPERUSER_PASSWORD:=""}"

if [ "$COLLECT_STATIC" -eq 1 ]; then
    python manage.py collectstatic --noinput
fi

if [ "$RUN_MIGRATIONS" -eq 1 ]; then
    python manage.py migrate --noinput
fi

if [ "x$DJANGO_SUPERUSER_EMAIL" != x ]; then
    python manage.py createsuperuser --noinput || true
fi

uwsgi --ini uwsgi.ini
