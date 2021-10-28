import re

from django.urls import path, re_path, register_converter
from django.views.generic import TemplateView

from . import views
from .constants import SHOW_CODES_TO_SHOW, Show


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


register_converter(ShowConverter, 'show')
register_converter(PodcastConverter, 'podcast')


app_name = "shows"
urlpatterns = [
    path("shows/", views.ShowsMasterListView.as_view(), name="show-master-list"),
    path(
        "listen/",
        # TODO: delete placeholder.html after this view is swapped out
        TemplateView.as_view(template_name="webcore/placeholder.html", extra_context={"title": "Listen"}),
        name="listen",
    ),
    path("<show:show>/", views.ShowListView.as_view(), name="show-list"),
    path("<show:show>/<slug:slug>/", views.ShowDetailView.as_view(), name="show-detail"),
    path("podcasts/<podcast:show>.rss", views.PodcastRSSView.as_view(), name="podcast-rss"),
]
