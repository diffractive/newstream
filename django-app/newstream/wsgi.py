"""
WSGI config for newstream project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
application = WhiteNoise(application, root="/app/static")
