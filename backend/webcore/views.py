import datetime

from pytz import timezone

from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView
from django.utils.timezone import get_default_timezone


class IndexView(TemplateView):
    template_name = "webcore/index.html"

    def get_context_data(self, **kwargs):
        return {
            "hide_title": True,
            "title": "jew.pizza - David Cooper",
            "default_tz_abbrev": get_default_timezone().localize(datetime.datetime.now()).tzname(),
            "js_data": {"test_tz": self.request.GET.get("testtz")}, **super().get_context_data(**kwargs),
        }
