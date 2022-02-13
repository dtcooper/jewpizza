from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView


class LiquidsoapScriptView(TemplateView):
    content_type = "text/plain"
    template_name = "radio/radio.liq"

    def dispatch(self, request, *args, **kwargs):
        secret_key = request.headers.get("X-Secret-Key")
        if secret_key == settings.SECRET_KEY or settings.DEBUG:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
