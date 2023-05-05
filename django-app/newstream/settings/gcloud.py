# 
# Django settings file for gcloud
# 
# This file has some custom env variables for google cloud. Please read the docs for
# details on these env variables and how to configure the system to run on google cloud.
#

from .base import *

import io
import os

import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(BASE_DIR, ".env")

# Load the env from os.environ and define known variables
# and default values
env = environ.Env(

    DEBUG=(bool, False),
    SECERT_KEY=(str, ""),
    ALLOWED_HOSTS=(str, "*"),

    GCLOUD_DATABASE_INSTANCE=(str, "newstream-db"),
    GCLOUD_DATABASE_NAME=(str, "newstream"),
    GCLOUD_DATABASE_USER=(str, "newstream"),
    GCLOUD_DATABASE_PASSWORD=(str, ""),

    GCLOUD_PROJECT_ID=(str, ""),
    GCLOUD_REGION=(str, ""),

    GCLOUD_BUCKET_NAME=(str, ""),

    EMAIL_BACKEND=(str, 'django.core.mail.backends.console.EmailBackend'),
    EMAIL_HOST=(str, ''),
    EMAIL_PORT=(int, 25),
    EMAIL_HOST_USER=(str, ''),
    EMAIL_HOST_PASSWORD=(str, ''), 
    EMAIL_USE_SSL=(bool, False),
    EMAIL_USE_TLS=(bool, False),

    DEFAULT_FROM_EMAIL=(str, ''),

    RUN_LOCALSTRIPE=(bool, False),

    WAGTAIL_2FA_REQUIRED=(str, False),
    WAGTAIL_2FA_OTP_TOTP_NAME=(str, "Newstream"),
)

# If a .env file exists, read from the .env file
if os.path.isfile(env_file):
    env.read_env(env_file)

DEBUG = env('DEBUG')

SECRET_KEY = env("SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("GCLOUD_DATABASE_NAME"),
        'USER': env("GCLOUD_DATABASE_USER"),
        'PASSWORD': env("GCLOUD_DATABASE_PASSWORD"),
        'HOST': '/cloudsql/%(project_id)s:%(region)s:%(instance)s' % {
            'project_id': env("GCLOUD_PROJECT_ID"),
            'region': env("GCLOUD_REGION"),
            'instance': env("GCLOUD_DATABASE_INSTANCE"),
        }
    }
}

# Email settings
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_USE_SSL = env('EMAIL_USE_SSL')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_PORT = env('EMAIL_PORT')
if env('EMAIL_HOST'): EMAIL_HOST = env('EMAIL_HOST')
if env('EMAIL_HOST_USER'): EMAIL_HOST_USER = env('EMAIL_HOST_USER')
if env('EMAIL_HOST_PASSWORD'): EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
# added temporary to fix cloud run job error
DEFAULT_ADMIN_EMAIL = DEFAULT_FROM_EMAIL

# Serve static files from google cloud storage if it is configured, otherwise
# will serve static files locally via uwsgi
if env("GCLOUD_BUCKET_NAME"):

    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

    GS_DEFAULT_ACL = "publicRead"
    GS_BUCKET_NAME = env("GCLOUD_BUCKET_NAME")

ALLOWED_HOSTS = [host.strip() for host in env('ALLOWED_HOSTS').split(',')]

# 2FA Config
WAGTAIL_2FA_REQUIRED=env('WAGTAIL_2FA_REQUIRED')
WAGTAIL_2FA_OTP_TOTP_NAME=env('WAGTAIL_2FA_OTP_TOTP_NAME')

# localstripe
RUN_LOCALSTRIPE = env('RUN_LOCALSTRIPE')

# Log evenrything to the console. Google cloud expects logging to the console
# and will capture and display these in the logs panel
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} [{module}] {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'newstream': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


try:
    from .local import *
except ImportError:
    pass
