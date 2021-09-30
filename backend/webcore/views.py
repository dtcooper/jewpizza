import datetime
from django.http.response import JsonResponse

from django.utils.timezone import get_default_timezone
from django.views.generic import TemplateView



class TemplateOrJSONView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        self.is_json = request.headers.get('Content-Type') == 'application/json'
        response = super().dispatch(request, *args, **kwargs)

        if self.is_json:
            response.render()
            response = JsonResponse({'content': response.content.decode()})

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.is_json:
            context['content_only'] = True
        return context


class HomeView(TemplateOrJSONView):
    template_name = "webcore/home.html"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "hide_title": True,
            "title": "jew.pizza - David Cooper",
            "default_tz_abbrev": get_default_timezone().localize(datetime.datetime.now()).tzname(),
            "js_data": {"test_tz": self.request.GET.get("testtz")},
        }
