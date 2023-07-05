#!/bin/sh

set -e

: "${RUN_MIGRATIONS:=1}"
: "${COLLECT_STATIC:=1}"
: "${DJANGO_SUPERUSER_EMAIL:=""}"
: "${DJANGO_SUPERUSER_PASSWORD:=""}"
: "${PY_AUTORELOAD:=0}"
: "${WIPE_DB:=0}"
: "${TEST_DATA:=0}"
: "${RESET_NULLABLE_SITESETTINGS:=0}"

init() {
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

    # temp fix for passing tests with the PR making sitesettings fields nullable: https://github.com/diffractive/newstream/pull/196
    if [ "$RESET_NULLABLE_SITESETTINGS" -eq 1 ]; then
        python manage.py reset_nullable_site_settings
    fi
}

run_django() {
    AUTORELOAD=""
    if [ "$PY_AUTORELOAD" -eq 1 ]; then
        AUTORELOAD="--py-autoreload=1"
    fi

    uwsgi ${AUTORELOAD} --ini /uwsgi.ini
}

case "$1" in
  init)
    echo "Initializing"
    init
    ;;
  init_and_run)
    echo "Initializing"
    init
    echo "Backend starting"
    run_django
    ;;
  run)
    echo "Backend starting"
    run_django
    ;;
  run_tests)
    echo "Running tests"
    cd /app && DJANGO_SETTINGS_MODULE=newstream.settings.dev PYTHONPATH=. python -m pytest --junitxml=/tmp/${SHORT_SHA}_test_log.xml --ignore=jupyter
    cat /tmp/${SHORT_SHA}_test_log.xml
    ;;
  *)
    echo "Please choose a command to run (init|run|init_and_run|run_tests)"
    ;;
esac
