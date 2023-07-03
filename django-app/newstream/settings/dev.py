from .base import *

ALLOWED_HOSTS = [
    "*"
]

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SECRET_KEY = os.environ.get("SECERT_KEY", "dummykey")
DEBUG = True

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + '/db.sqlite3',
    }
}

try:
    from .local import *
except ImportError:
    pass


