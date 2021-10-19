from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView


class ScriptView(TemplateView):
    content_type = "text/plain"

    def dispatch(self, request, *args, **kwargs):
        secret_key = request.headers.get("X-Secret-Key")
        if secret_key == settings.SECRET_KEY or settings.DEBUG:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
