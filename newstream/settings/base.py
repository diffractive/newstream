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

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# django needs this to redirects user correctly when he stumbles upon a logn_required route
LOGIN_URL = "/accounts/login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# django-allauth
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
# this extra signup form class is shared by both account and socialaccount
ACCOUNT_SIGNUP_FORM_CLASS = 'newstream.forms_signup.BaseSignupForm'
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_ADAPTER = 'newstream.forms.NewstreamSAAdapter'

DEFAULT_FROM_EMAIL = 'franky@arkon.digital'

# Custom User Model
AUTH_USER_MODEL = 'newstream_user.User'
WAGTAIL_USER_EDIT_FORM = 'newstream_user.forms.NewstreamUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'newstream_user.forms.NewstreamUserCreationForm'
WAGTAIL_USER_CUSTOM_FIELDS = ['opt_in_mailing_list', 'language_preference']


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    # custom_user
    'newstream_user.apps.NewstreamUserConfig',

    # make sure them before all apps that you want to translate
    'wagtail_modeltranslation',
    'wagtail_modeltranslation.makemigrations',
    'wagtail_modeltranslation.migrate',

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
    'wagtail.core',
    'wagtail.contrib.styleguide',

    'captcha',
    'wagtailstreamforms',
    'modelcluster',
    'taggit',
    'wagtailautocomplete',
    'wagtailmodelchooser',
    'widget_tweaks',
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

    # newstream apps
    'pages',
    'search',
    'site_settings',
    'donations',
    'email_campaigns',
]

MIDDLEWARE = [
    # Recommended order from https://www.accordbox.com/blog/how-support-multi-language-wagtail-cms/
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

    'newstream.view_middleware.DisableSocialLoginMiddleware',
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
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'ns-debug.log'),
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'newstream': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Wagtail ModelTranslation Settings
# This setting is essential for the displaying of translated fields in site_settings,
# if not specified, the translated fields in panels under SubObjectList will not be displayed
WAGTAILMODELTRANSLATION_CUSTOM_COMPOSED_PANELS = [
    'site_settings.models.SubObjectList']

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('zh-hant', _('Traditional Chinese')),
    ('ms', _('Malay')),
    ('id-id', _('Indonesian')),
    ('tl', _('Tagalog')),
]

EXTRA_LANG_INFO = {
    'ms': {
        'bidi': True,  # bi-directional
        'code': 'ms',
        'name': 'Bahasa Melayu',
        'name_local': u'Bahasa Melayu',  # unicode codepoints here
    },
    'tl': {
        'bidi': False,
        'code': 'tl',
        'name': 'Tagalog',
        'name_local': u'Tagalog',  # unicode codepoints here
    },
    'id-id': {
        'bidi': False,
        'code': 'id-id',
        'name': 'Indonesian',
        'name_local': u'Bahasa Indonesia',
    },
}

# Add custom languages not provided by Django
LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO

# Languages using BiDi (right-to-left) layout
LANGUAGES_BIDI = global_settings.LANGUAGES_BIDI + ["ms"]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# wagtailstreamforms
WAGTAILSTREAMFORMS_FORM_TEMPLATES = (
    ('streamforms/form_block.html', 'Default Form Template'),  # default
    ('pages/streamforms/custom_template.html', 'Newstream Form Template'),
)

# django-recaptcha
# enable no captcha
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
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
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


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

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
# todo: might need to be dynamically set by admin?
BASE_URL = 'https://newstream.hongkongfp.com'

# allauth-related settings

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

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
