from django.urls import path
from django.views.generic import TemplateView

from .views import HomeView

app_name = "webcore"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("bio/", TemplateView.as_view(template_name="webcore/bio.html", extra_context={"title": "Bio"}), name="bio"),
    path(
        "testimonials/",
        TemplateView.as_view(template_name="webcore/placeholder.html", extra_context={"title": "Testimonials"}),
        name="testimonials",
    ),
    path(
        "social/",
        TemplateView.as_view(template_name="webcore/placeholder.html", extra_context={"title": "Social"}),
        name="social",
    ),
]
