"""
Django settings for newstream project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import django
import django.conf.locale
from django.utils.translation import gettext_lazy as _
from django.conf import global_settings
from newstream.logging_utils import CustomJsonFormatter

import environ
from google.oauth2 import service_account

# load "NEWSTREAM" prefixed env vars for site_settings
from .site_settings import *

env = environ.Env(
    LOG_FORMAT_JSON=(bool, True),
    STRIPE_JS_URL=(str, 'https://js.stripe.com/v3/'),
    STRIPE_API_BASE=(str, ""),
    STRIPE_API_VERSION=(str, ""),
    INIT_LOCALSTRIPE=(bool, False),
    # comma separated list of resource ids to be ignored from webhooks
    STRIPE_WEBHOOK_IGNORABLE_RESOURCES=(str, ''),

    PAYPAL_API_BASE=(str, ""),
    PAYPAL_PAYMENT_FAILURE_THRESHOLD=(int, 3),
    # comma separated list of resource ids to be ignored from webhooks
    PAYPAL_WEBHOOK_IGNORABLE_RESOURCES=(str, ''),

    DATADOG_APPID=(str, None),
    DATADOG_TOKEN=(str, None),
    DATADOG_ENV=(str, None),
    DATADOG_SERVICE=(str, None),

    GS_FAKE_CREDENTIALS=(bool, False),
    GS_BUCKET_NAME=(str, 'newstream-test-bucket'),
    GS_STORAGE_ENDPOINT=(str, ""),
    GS_CUSTOM_ENDPOINT=(str, ""),
)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# for processing paypal legacy ipns (12M)
DATA_UPLOAD_MAX_MEMORY_SIZE = 12582912

# for editing home page which could break the default limit of 1000
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000

# django needs this to redirects user correctly when he stumbles upon a logn_required route
LOGIN_URL = "/accounts/login"
# hardcode fix for the redirected to other languages issue
LOGIN_REDIRECT_URL = "/en"
LOGOUT_REDIRECT_URL = "/en"

# django-allauth
ACCOUNT_ADAPTER = 'newstream.adapters.NewstreamAccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_SUBJECT_PREFIX = None # for removing site prefix in password reset and email verification subject lines
# this extra signup form class is shared by both account and socialaccount
ACCOUNT_SIGNUP_FORM_CLASS = 'newstream.forms_signup.BaseSignupForm'
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_ADAPTER = 'newstream.forms.NewstreamSAAdapter'
# a rate limit that allows for one confirmation mail to be sent per the specified cooldown period (in seconds).
# with current allauth implementation, it would only silently fail if user sends confirmation email again within cooldown period,
# so better have this stay at 0 as it always have been
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 0

DEFAULT_FROM_EMAIL = 'donations@domain.example'

# Custom User Model
AUTH_USER_MODEL = 'newstream_user.User'
WAGTAIL_USER_CUSTOM_FIELDS = ['opt_in_mailing_list', 'language_preference']


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    # custom_user
    'newstream_user.apps.NewstreamUserConfig',

    'whitenoise.runserver_nostatic',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    "wagtail_modeladmin",
    'wagtail',
    'wagtail.contrib.styleguide',
    'wagtail.contrib.simple_translation',
    'wagtail.locales',

    'django_recaptcha',
    'modelcluster',
    'taggit',
    'wagtailautocomplete',
    'wagtailmodelchooser',
    'widget_tweaks',
    'wagtailmetadata',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',

    'wagtail_2fa',

    'django_otp',
    'django_otp.plugins.otp_totp',

    'storages',

    # newstream apps
    'pages',
    # 'search',
    'site_settings',
    'donations',
    'email_campaigns',
]

MIDDLEWARE = [
    # Recommended order from https://www.accordbox.com/blog/how-support-multi-language-wagtail-cms/
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'wagtail.contrib.legacy.sitemiddleware.SiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

    'newstream.view_middleware.DisableSocialLoginMiddleware',

    'wagtail_2fa.middleware.VerifyUserMiddleware',
    'middleware.NewstreamCurrentRequestUserMiddleware',
    'middleware.RequestLoggerMiddleware',
]

ROOT_URLCONF = 'newstream.urls'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
            django.__path__[0] + '/forms/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django_settings_export.settings_export',
                'pages.context_processors.homepage',
            ],
            'libraries': {
                'common_tags': 'newstream.templatetags.common_tags',
            },
        },
    },
]

WSGI_APPLICATION = 'newstream.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

# Using secure cookies, see https://docs.djangoproject.com/en/3.0/topics/security/#ssl-https
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

LOG_FORMAT_JSON = env('LOG_FORMAT_JSON')

# Log evenrything to the console. Google cloud expects logging to the console
# and will capture and display these in the logs panel

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'human': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        "json": {
            "()": CustomJsonFormatter,
            "format": "",
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            "formatter": 'json' if env('LOG_FORMAT_JSON') else 'human',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'newstream.request': {
            'handlers': ['console'],
            'propagate': False,
        },
        'newstream': {
            'handlers': ['console'],
            'propagate': False,
        }
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('zh-hant', _('Traditional Chinese')),
    ('en', _('English')),
]

# add in the additional newstream directory
LOCALE_PATHS = [os.path.join(PROJECT_DIR, 'locale'),]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

WAGTAIL_I18N_ENABLED = True

# django-recaptcha
# enable no captcha
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']
NOCAPTCHA = True
RECAPTCHA_REQUIRED_SCORE = 0.85

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

################################################
#
# Google Cloud Storage

GS_BUCKET_NAME = env('GS_BUCKET_NAME')

# Direct media file serving from the backend
#
# We should be using signed urls and serving media files from the GCS bucket directly
# This isn't working well at the moment though, because the generate_signed_url method
# is horrendously slow. See https://github.com/googleapis/google-cloud-python/issues/3696
#
# We've resorted to serving the files directly from the backend

# Our custom class which prevents use of signed urls
DEFAULT_FILE_STORAGE = 'newstream.storage.NewstreamCloudStorage'

# Custom endpoint is just served from the local serivce
if env('GS_CUSTOM_ENDPOINT'):
    GS_CUSTOM_ENDPOINT=env('GS_CUSTOM_ENDPOINT')

if env('GS_FAKE_CREDENTIALS'):
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.abspath(os.path.join(BASE_DIR, 'newstream/fake-gcs-credentials.json'))
    )

# Internal variable for our own use, not supported by storages
GS_STORAGE_ENDPOINT=env('GS_STORAGE_ENDPOINT')

################################################

# Wagtail settings
# todo: might need to be dynamically set by admin?
WAGTAIL_SITE_NAME = "Newstream"

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': ['h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'superscript', 'subscript', 'strikethrough', 'blockquote']
        }
    },
    'legacy': {
        'WIDGET': 'wagtail.admin.rich_text.HalloRichTextArea',
    }
}

# allauth-related settings

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Add a ``Site`` for your domain, matching ``settings.SITE_ID`` (``django.contrib.sites`` app).
SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'VERIFIED_EMAIL': True
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': [
            'email',
            'public_profile',
        ],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'EXCHANGE_TOKEN': True,
        # comment this param to enforce email verification signing up any emails from facebook
        'VERIFIED_EMAIL': True,
    },
    'twitter': {
        # comment this param to enforce email verification signing up any emails from twitter
        'VERIFIED_EMAIL': True,
    }
}

#########################################################################################
#
# Stripe settings
#

STRIPE_JS_URL = env('STRIPE_JS_URL')
STRIPE_API_BASE = env('STRIPE_API_BASE')
STRIPE_API_VERSION = env('STRIPE_API_VERSION')
INIT_LOCALSTRIPE = env('INIT_LOCALSTRIPE')
STRIPE_WEBHOOK_IGNORABLE_RESOURCES=env('STRIPE_WEBHOOK_IGNORABLE_RESOURCES')

#########################################################################################
#
# PayPal settings
#

PAYPAL_API_BASE = env('PAYPAL_API_BASE')
# tweaking payment_failure_threshold when creating plans,
# mainly for testing on dev/staging
PAYPAL_PAYMENT_FAILURE_THRESHOLD = env('PAYPAL_PAYMENT_FAILURE_THRESHOLD')
PAYPAL_WEBHOOK_IGNORABLE_RESOURCES=env('PAYPAL_WEBHOOK_IGNORABLE_RESOURCES')

################################################
#
# Datadog
#

DATADOG_APPID = env('DATADOG_APPID')
DATADOG_TOKEN = env('DATADOG_TOKEN')
DATADOG_ENV = env('DATADOG_ENV')
DATADOG_SERVICE = env('DATADOG_SERVICE')


SETTINGS_EXPORT = [
    'STRIPE_JS_URL',
    'DATADOG_APPID', 'DATADOG_TOKEN', 'DATADOG_ENV', 'DATADOG_SERVICE',
]
