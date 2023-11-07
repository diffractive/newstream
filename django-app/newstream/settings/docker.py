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
DEBUG = int(os.environ.get("DEBUG", "0"))

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mailhog'
EMAIL_PORT = '1025'

# used by allauth
DEFAULT_FROM_EMAIL = site_settings_envvars('NEWSTREAM_DEFAULT_FROM_EMAIL')

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

try:
    from .local import *
except ImportError:
    pass


