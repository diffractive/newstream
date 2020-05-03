from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$c(sq#fb1n!rkimu3dk$!x6p6t9_)7(@2a&fb_u(yc2%c=^aiy'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'AKIAYPKUY36QQ2EBDYOM'
EMAIL_HOST_PASSWORD = os.environ.get('OMPSMTP_PWD')

ADMINS = [
    ('franky@Diffractive', 'franky@diffractive.io'),
]

try:
    from .local import *
except ImportError:
    pass
