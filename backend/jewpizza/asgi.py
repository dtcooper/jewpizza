from django.conf import settings
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.core.asgi import get_asgi_application

application = get_asgi_application()

if settings.DEBUG:
    application = ASGIStaticFilesHandler(application)
