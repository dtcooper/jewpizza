import datetime
import json
import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.timezone import get_default_timezone
from django.views.generic import TemplateView, View

from constance import config


logger = logging.getLogger(f"jewpizza.{__file__}")


class LogJSErrorView(View):
    def post(self, request, *args, **kwargs):
        try:
            error = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest()

        message = ""
        if settings.DEBUG:
            message = "[not sending due to DEBUG = True] "
        message += f"{error['title']} occurred at {error['url']}"
        if filename := error.get("filename"):
            message += f" ({filename})"
        message += f":\n\n{error.get('detail', '[none]')}"

        logger.warning(f"Got JS error: {message}")

        if not settings.DEBUG:
            send_mail(
                subject=f"jew.pizza JS Error: {error['title']}",
                message=message,
                from_email=None,
                recipient_list=[settings.EMAIL_ADDRESS],
            )

        return HttpResponse(status=204)


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
        }
