"""
ASGI config for jewpizza project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.conf import settings


application = get_asgi_application()

if settings.DEBUG:
    application = ASGIStaticFilesHandler(application)
