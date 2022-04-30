import datetime
import json
import logging

import pytz

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.utils.timezone import get_default_timezone
from django.views.generic import TemplateView, View

from constance import config

from jew_pizza.utils import get_client_ip


logger = logging.getLogger(f"jewpizza.{__file__}")


class PlaceholderView(TemplateView):
    template_name = "webcore/placeholder.html"
    extra_context = {"title": "jew.pizza - David Cooper"}

    def get_context_data(self, **kwargs):
        return {
            "eastern_tz_abbrev": pytz.timezone("US/Eastern").localize(datetime.datetime.now()).tzname(),
            "js_data": {"test_tz": self.request.GET.get("testtz")},
            **super().get_context_data(**kwargs),
        }


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

        ip_address = get_client_ip(request)
        logger.warning(f"Got JS error from IP {ip_address}: {message}")

        if not settings.DEBUG:
            send_mail(
                subject=f"jew.pizza JS Error from IP {ip_address}: {error['title']}",
                message=message,
                from_email=None,
                recipient_list=[settings.EMAIL_ADDRESS],
            )

        return HttpResponse(status=204)


class PodcastRedirectView(View):
    DEFAULT_PODCAST = "showgram"
    PODCASTS = {
        "showgram": {
            "default": "https://www.iheart.com/podcast/962-showgram-59146123/",
            "apple": "https://podcasts.apple.com/us/podcast/the-showgram-with-david-cooper/id1502619425",
            "google": (
                "https://podcasts.google.com/feed/aHR0cHM6Ly93d3cub21ueWNvbnRlbnQuY29tL2QvcGxheWxpc3QvNDgwOWJjOGEtZTQxY"
                "S00MDVjLTkzZGEtYThjZjAxMWRmMmY0LzhhY2RmZjg0LWJjMjAtNDlmMy04N2I3LWFiN2MwMTM0YTNhOC8yOGEzMDY0ZC0yZGZmLTR"
                "jZGQtOTUyOC1hYjdjMDEzNjM5NjkvcG9kY2FzdC5yc3M"
            ),
        },
        "tigwit": {
            "default": "https://soundcloud.com/tigwit",
            "apple": "https://podcasts.apple.com/us/podcast/this-is-going-well-i-think-with-david-cooper/id1168275879",
            "google": (
                "https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5zb3VuZGNsb3VkLmNvbS91c2Vycy9zb3VuZGNsb3VkOnVzZXJzO"
                "jI2MzIwOTQxOC9zb3VuZHMucnNz"
            ),
        },
    }

    def get(self, request, podcast):
        podcast = self.PODCASTS.get(podcast)
        if podcast is None:
            podcast = self.PODCASTS[self.DEFAULT_PODCAST]

        forced_redirect = request.GET.get("force")
        if forced_redirect is not None and forced_redirect in podcast:
            redirect = forced_redirect

        else:
            redirect = "default"
            os_family = request.user_agent.os.family
            if os_family in ("Mac OS X", "iOS"):
                redirect = "apple"
            elif os_family == "Android":
                redirect = "google"

        return HttpResponseRedirect(podcast[redirect])
