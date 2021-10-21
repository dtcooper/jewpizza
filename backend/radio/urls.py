from django.urls import path

from .views import LiquidsoapScriptView


app_name = "radio"
urlpatterns = [
    path("liquidsoap/script/", LiquidsoapScriptView.as_view(), name="liquidsoap-script"),
]
