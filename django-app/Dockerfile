FROM python:3.11-slim-bookworm AS build-image
LABEL maintainer="support@diffractive.io"

# Dockerfile parameters
ARG APP_USER=newstream

# Set environment varibles
ENV PYTHONUNBUFFERED 1

# Install postgres client and mariadb-client
# The mariadb-client is needed for givewp migration support
# libcurl4-gnutls-dev is needed for pycurl for gateway support
# gcc is required for building pycurl. We should split that as buildDepends (see puckel/docker airflow)
# mime-support is required for uwsgi to serve static files correctly
# Explicitly install postgresql version to fix vulnerability, we can remove it once postgresql-client is updated
# libpcre3 is needed for uwsgi routing support
RUN set -ex \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        postgresql-client \
        libmariadb-dev \
        libgnutls28-dev \
        libcurl4-gnutls-dev \
        gcc \
        mime-support \
        gettext \
        libpcre3 \
        libpcre3-dev \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app/
ADD . /app/

ARG APP_VERSION
RUN echo "APP_VERSION=$APP_VERSION" > .env

# Requirements files
# The requirements.txt file is requriements for newstream
# The requirements-docker.txt is additional requirements to run ths sytem via docker (ie: gunicorn)
COPY ./requirements.txt /tmp/
COPY ./requirements-docker.txt /tmp

ARG DEV_MODE=0

RUN if [ "$DEV_MODE" = "0" ] ; then \
    pip install --no-cache-dir --upgrade pip && \
    CFLAGS='-Os -g0 -Wl,--strip-all' pip install --no-cache-dir --compile -r /tmp/requirements.txt  && \
    CFLAGS='-Os -g0 -Wl,--strip-all' pip install --no-cache-dir --compile -r /tmp/requirements-docker.txt ;  \
    else \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt  && \
    pip install -r /tmp/requirements-docker.txt ;  \
    fi; \
    rm -rf /tmp/* ; \
    find /opt/venv/ -type d -name __pycache__ -exec rm -r -v {} + > /dev/null; \
    find /opt/venv/ -type f -name requirements.txt -exec rm -v {} + > /dev/null;

# Gunicorn will listen on this port
EXPOSE 8000

# Set django settings for docker
ENV DJANGO_SETTINGS_MODULE=newstream.settings.docker

# Create a group and user to run newstream
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# Create the static files dir and set to be owned by the application
RUN mkdir -p /app/static
RUN chown newstream:newstream /app/static

# We also need to be able to write to the locales folder for compilemessages
# TODO: This needs updated, as it does introduce more security risks
RUN chown -R newstream:newstream /app

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN DATABASE_URL='' python manage.py collectstatic --noinput

# Run compilemessages to build the mo files
RUN DATABASE_URL='' python manage.py compilemessages

COPY docker/uwsgi.ini /

# Entrypoint script
COPY docker/docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
