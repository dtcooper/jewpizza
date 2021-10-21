from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView

from jew_pizza.constants import REDIS_PUBSUB_CHANNEL


class ScriptView(TemplateView):
    content_type = "text/plain"
    extra_context = {"REDIS_PUBSUB_CHANNEL": REDIS_PUBSUB_CHANNEL}

    def dispatch(self, request, *args, **kwargs):
        secret_key = request.headers.get("X-Secret-Key")
        if secret_key == settings.SECRET_KEY or settings.DEBUG:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
