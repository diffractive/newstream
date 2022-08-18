#!/bin/sh

set -e

case "$1" in
  jupyter)
    DJANGO_SETTINGS_MODULE=settings.docker PYTHONPATH=/app DJANGO_ALLOW_ASYNC_UNSAFE=true jupyter notebook --ip 0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''
    ;;
  *)
    echo "Please choose a command to run (jupyter)"
    ;;
esac
