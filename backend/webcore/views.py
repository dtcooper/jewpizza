import datetime

from django.http.response import JsonResponse
from django.utils.timezone import get_default_timezone
from django.views.generic import TemplateView

from jew_pizza.jinja2 import get_messages


class TemplateOrJSONViewMixin:
    def dispatch(self, request, *args, **kwargs):
        self.is_json = request.headers.get("Accept") == "application/json"
        response = super().dispatch(request, *args, **kwargs)

        if self.is_json:
            redirect_to = response.headers.get("Location")
            if redirect_to:
                json_data = {"redirect": redirect_to}
            else:
                if hasattr(response, "render"):
                    response.render()
                json_data = {
                    "content": response.content.decode(),
                    "messages": get_messages(request),
                    "title": response.context_data.get("title") or "jew.pizza",
                }
            response = JsonResponse(json_data)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.is_json:
            context["content_only"] = True
        return context


class TemplateOrJSONView(TemplateOrJSONViewMixin, TemplateView):
    pass


class HomeView(TemplateOrJSONViewMixin, TemplateView):
    template_name = "webcore/home.html"

    def get_context_data(self, **kwargs):
        import random

        from django.contrib import messages

        level = random.choice([messages.INFO, messages.SUCCESS, messages.ERROR, messages.WARNING])
        messages.add_message(
            self.request,
            level,
            f'Test "{messages.constants.DEFAULT_TAGS.get(level)}" message!',
        )

        return {
            **super().get_context_data(**kwargs),
            "hide_title": True,
            "title": "jew.pizza - David Cooper",
            "default_tz_abbrev": get_default_timezone().localize(datetime.datetime.now()).tzname(),
            "js_data": {"test_tz": self.request.GET.get("testtz")},
        }
