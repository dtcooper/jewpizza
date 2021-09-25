from django.urls import path
from django.views.generic import TemplateView

import webcore.views as views

app_name = "webcore"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("bio/", TemplateView.as_view(template_name="webcore/bio.html", extra_context={"title": "Bio"}), name="bio"),
]
