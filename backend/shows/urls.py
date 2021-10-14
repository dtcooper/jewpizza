from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "shows"
urlpatterns = [
    path("shows/", views.ShowsMasterListView.as_view(), name="master-list"),
    path(
        "listen/",
        # TODO: delete placeholder.html after this view is swapped out
        TemplateView.as_view(template_name="webcore/placeholder.html", extra_context={"title": "Listen"}),
        name="listen",
    ),
]
