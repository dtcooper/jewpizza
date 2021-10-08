import datetime

from django.utils.timezone import get_default_timezone
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "webcore/home.html"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "hide_title": True,
            "title": "jew.pizza - David Cooper",
            "default_tz_abbrev": get_default_timezone().localize(datetime.datetime.now()).tzname(),
            "js_data": {"test_tz": self.request.GET.get("testtz")},
        }
