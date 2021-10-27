import re

from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views
from .constants import SHOWS


app_name = "shows"
urlpatterns = [
    path("shows/", views.ShowsMasterListView.as_view(), name="show-master-list"),
    path(
        "listen/",
        # TODO: delete placeholder.html after this view is swapped out
        TemplateView.as_view(template_name="webcore/placeholder.html", extra_context={"title": "Listen"}),
        name="listen",
    ),
    re_path(
        r"^(?P<show>{})/$".format("|".join(re.escape(s.code) for s in SHOWS)),
        views.ShowListView.as_view(),
        name="show-list",
    ),
    re_path(
        r"^(?P<show>{})/(?P<episode>.+)$".format("|".join(re.escape(s.code) for s in SHOWS)),
        views.ShowDetailView.as_view(),
        name="show-detail",
    ),
    re_path(
        r"^podcasts/(?P<show>{})\.rss$".format("|".join(re.escape(s.code) for s in SHOWS if s.podcast)),
        views.PodcastRSSView.as_view(),
        name="podcast-rss",
    ),
]
