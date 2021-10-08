import datetime

from django.contrib import messages
from django.utils.timezone import get_default_timezone
from django.views.generic import TemplateView

from constance import config


class HomeView(TemplateView):
    template_name = "webcore/home.html"

    def dispatch(self, request, *args, **kwargs):
        if config.ENABLE_TEST_NOTIFICATIONS and self.request.user.is_superuser:
            for level, tag in messages.constants.DEFAULT_TAGS.items():
                if level != messages.DEBUG:
                    messages.add_message(request, level, f"Test {tag.lower()} message.")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "hide_title": True,
            "title": "jew.pizza - David Cooper",
            "default_tz_abbrev": get_default_timezone().localize(datetime.datetime.now()).tzname(),
            "js_data": {"test_tz": self.request.GET.get("testtz")},
        }
