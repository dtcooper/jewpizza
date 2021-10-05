import os

from django.conf import settings
from django.http import HttpResponse


class TailwindFunctioningRunserverMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.stylesheet_path = settings.BASE_DIR / "webcore" / "static" / "css" / "styles.css"

    def __call__(self, request):
        if os.path.exists(self.stylesheet_path):
            response = self.get_response(request)
            return response
        else:
            return HttpResponse(
                "Tailwind did NOT generate stylesheet, see command output.",
                content_type="text/plain",
            )
