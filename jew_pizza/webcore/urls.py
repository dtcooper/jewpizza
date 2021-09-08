from django.urls import path

import webcore.views as views

app_name = "webcore"
urlpatterns = [
    path("", views.PlaceholderView.as_view(), name="placeholder"),
    path("index/", views.IndexView.as_view(), name="index"),
]
