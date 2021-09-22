from django.urls import path

import webcore.views as views

app_name = "webcore"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]
