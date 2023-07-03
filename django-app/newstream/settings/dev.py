from .base import *

ALLOWED_HOSTS = [
    "*"
]

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

try:
    from .local import *
except ImportError:
    pass


