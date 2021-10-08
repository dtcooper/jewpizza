from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "shows"
urlpatterns = [
    path("shows/", views.ShowsMasterListView.as_view(), name="shows-master-list"),
    path(
        "listen/",
        TemplateView.as_view(template_name="webcore/placeholder.html", extra_context={"title": "Listen"}),
        name="listen",
    ),
]
