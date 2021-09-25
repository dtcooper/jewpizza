from django.urls import path
from django.views.generic import TemplateView

app_name = "shows"
urlpatterns = [
    path("", TemplateView.as_view(template_name="shows/shows.html", extra_context={"title": "Shows"}), name="shows"),
]
