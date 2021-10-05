from django.urls import path

import webcore.views as views

app_name = "webcore"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "bio/",
        views.TemplateOrJSONView.as_view(template_name="webcore/bio.html", extra_context={"title": "Bio"}),
        name="bio",
    ),
    path(
        "testimonials/",
        views.TemplateOrJSONView.as_view(
            template_name="webcore/placeholder.html",
            extra_context={"title": "Testimonials"},
        ),
        name="testimonials",
    ),
    path(
        "social/",
        views.TemplateOrJSONView.as_view(template_name="webcore/placeholder.html", extra_context={"title": "Social"}),
        name="social",
    ),
    path(
        "contact/",
        views.TemplateOrJSONView.as_view(template_name="webcore/placeholder.html", extra_context={"title": "Contact"}),
        name="contact",
    ),
]
