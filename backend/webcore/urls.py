from django.http import HttpResponse
from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = "webcore"
urlpatterns = [
    path("", views.PlaceholderView.as_view(), name="placeholder"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("bio/", TemplateView.as_view(template_name="webcore/bio.html", extra_context={"title": "Bio"}), name="bio"),
    path(
        "testimonials/",
        TemplateView.as_view(template_name="webcore/testimonials.html", extra_context={"title": "Testimonials"}),
        name="testimonials",
    ),
    path(
        "social/",
        TemplateView.as_view(template_name="webcore/social.html", extra_context={"title": "Social"}),
        name="social",
    ),
    path("internal/log-js-error/", views.LogJSErrorView.as_view(), name="log-js-error"),
    path("protected/store-sse-in-cache/", views.LogSSEToCacheView.as_view(), name="store-sse-in-cache"),
]
