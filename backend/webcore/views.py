import datetime

from django.utils.timezone import get_default_timezone
from django.views.generic import TemplateView

from jew_pizza.jinja2 import get_messages


class HomeView(TemplateView):
    template_name = "webcore/home.html"

    def get_context_data(self, **kwargs):
        import random
        from django.conf import settings
        from django.contrib import messages

        if settings.DEBUG:
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
