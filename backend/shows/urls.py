from django.urls import path
from django.views.generic import TemplateView

app_name = "shows"
urlpatterns = [
    path(
        "shows/",
        TemplateView.as_view(template_name="webcore/placeholder.html", extra_context={"title": "Shows"}),
        name="shows",
    ),
    path(
        "listen/",
        TemplateView.as_view(template_name="webcore/placeholder.html", extra_context={"title": "Listen"}),
        name="listen",
    ),
]
