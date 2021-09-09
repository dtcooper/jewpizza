import datetime

from pytz import timezone

from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView


class PlaceholderView(TemplateView):
    template_name = "webcore/placeholder.html"
    extra_context = {"title": "jew.pizza - David Cooper", "hide_header": True}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["eastern_tz_abbrev"] = timezone("US/Eastern").localize(datetime.datetime.now()).tzname()
        test_tz = self.request.GET.get("testtz")
        if "testtz" in self.request.GET:
            context["js_data"] = {"test_tz": test_tz}
        return context


class IndexView(TemplateView):
    template_name = "webcore/index.html"
    extra_context = {"title": "jew.pizza - David Cooper"}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and not settings.DEBUG:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
