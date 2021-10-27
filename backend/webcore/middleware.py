import os

from django.conf import settings
from django.http import HttpResponse, JsonResponse

from jew_pizza.jinja2 import get_messages


class TailwindFunctioningRunserverMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.stylesheet_path = settings.BASE_DIR / "webcore" / "static" / "webcore" / "css" / "styles.css"

    def __call__(self, request):
        if os.path.exists(self.stylesheet_path):
            response = self.get_response(request)
            return response
        else:
            return HttpResponse(
                "Tailwind did NOT generate stylesheet, see command output.",
                content_type="text/plain",
            )


class JSONResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def is_json(request):
        return request.headers.get("Accept") == "application/json"

    def __call__(self, request):
        response = self.get_response(request)

        if self.is_json(request):
            headers = {"Vary": "Accept"}  # https://stackoverflow.com/a/60118781
            json_data = {'status': response.status_code}

            if redirect_to := response.headers.get("Location"):
                json_data['redirect'] = redirect_to
            else:
                json_data.update({
                    "content": response.content.decode().strip(),
                    "messages": get_messages(request),
                    "title": 'jew.pizza',
                })
                if hasattr(response, 'context_data') and (title := response.context_data.get('title')):
                    json_data['title'] = title
            response = JsonResponse(json_data, headers=headers)

        return response

    def process_template_response(self, request, response):
        if self.is_json(request):
            response.context_data["content_only"] = True
        return response
