from django.urls import path

from webcore.views import TemplateOrJSONView

app_name = "shows"
urlpatterns = [
    path(
        "shows/",
        TemplateOrJSONView.as_view(template_name="webcore/placeholder.html", extra_context={"title": "Shows"}),
        name="shows",
    ),
    path(
        "listen/",
        TemplateOrJSONView.as_view(template_name="webcore/placeholder.html", extra_context={"title": "Listen"}),
        name="listen",
    ),
]
