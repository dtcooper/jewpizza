import re

from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path, register_converter

from shows.constants import SHOW_CODES_TO_SHOW, Show
from webcore.middleware import JSONResponseMiddleware


admin.site.index_title = admin.site.site_header = "jew.pizza administration"
admin.site.site_title = "jew.pizza site admin"


class ShowConverter:
    regex = "|".join(re.escape(code) for code in SHOW_CODES_TO_SHOW.keys())

    def to_python(self, value):
        return SHOW_CODES_TO_SHOW[value]

    def to_url(self, value):
        if isinstance(value, Show):
            value = value.code
        return value


class PodcastConverter(ShowConverter):
    regex = "|".join(re.escape(code) for code, show in SHOW_CODES_TO_SHOW.items() if show.podcast)


register_converter(ShowConverter, "show")
register_converter(PodcastConverter, "podcast")


urlpatterns = [
    path("", include("webcore.urls")),
    path("", include("notifications.urls")),
    path("", include("shows.urls")),
    path("internal/radio/", include("radio.urls")),
    path("cmsadmin/tools/", include("admin_tools.urls")),
    path("cmsadmin/", admin.site.urls),
    path("s3direct/", include("s3direct.urls")),
]


def error_handler(request, status, title, description, *args, **kwargs):
    context = {"title": title, "description": description, "status_code": status}
    # JSONResponseMiddleware.process_template_response() seems to be ignored
    if JSONResponseMiddleware.is_json(request):
        context["content_only"] = True
    return render(request, "webcore/error.html", context, status=status, *args, **kwargs)


def handler500(request, *args, **kwargs):
    return error_handler(
        request, 500, "Server Error", "A server error occurred. That's bad. Probably a mistake with the site."
    )


def handler404(request, exception, *args, **kwargs):
    return error_handler(request, 404, "Not Found", "I couldn't find what you were looking for.")


def handler403(request, exception, *args, **kwargs):
    return error_handler(request, 403, "Permission Denied", "Hey! You're not allowed to see that.")
