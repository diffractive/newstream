from .base import *

ALLOWED_HOSTS = [
    "*"
]

SECRET_KEY = os.environ.get("SECERT_KEY", "dummykey")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "newstream")
DATABASE_USER = os.environ.get("DATABASE_USER", "newstream")
DATABASE_HOST = os.environ.get("DATABASE_HOST", "")
DATABASE_PORT = os.environ.get("DATABASE_PORT", "")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "")
DEBUG = int(os.environ.get("NEWSTREAM_DEBUG", "0"))

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'mailhog'
EMAIL_PORT = '1025'

DEFAULT_FROM_EMAIL = 'newstream@diffractive.io'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
        'PASSWORD': DATABASE_PASSWORD,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[DJANGO] %(levelname)s %(asctime)s %(module)s '
                      '%(name)s.%(funcName)s:%(lineno)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'loggers': {
        '*': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}

try:
    from .local import *
except ImportError:
    pass


