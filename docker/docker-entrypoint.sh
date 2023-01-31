#!/bin/sh

set -e

: "${RUN_MIGRATIONS:=1}"
: "${COLLECT_STATIC:=1}"
: "${DJANGO_SUPERUSER_EMAIL:=""}"
: "${DJANGO_SUPERUSER_EMAIL:=""}"
: "${DJANGO_SUPERUSER_PASSWORD:=""}"
: "${PY_AUTORELOAD:=0}"
: "${WIPE_DB:=0}"
: "${TEST_DATA:=0}"

if [ "$WIPE_DB" -eq 1 ]; then
    echo "WARNING: Wiping Database due to ENV setting!!"
    python manage.py reset_db --noinput -c
fi

if [ "$COLLECT_STATIC" -eq 1 ]; then
    python manage.py collectstatic --noinput
fi

if [ "$RUN_MIGRATIONS" -eq 1 ]; then
    python manage.py migrate --noinput
fi

if [ "x$DJANGO_SUPERUSER_EMAIL" != x ]; then
    python manage.py createsuperuser --noinput || true
fi

if [ "$TEST_DATA" -eq 1 ]; then
    python manage.py test_data
fi

AUTORELOAD=""
if [ "$PY_AUTORELOAD" -eq 1 ]; then
    AUTORELOAD="--py-autoreload=1"
fi

uwsgi ${AUTORELOAD} --ini /uwsgi.ini
