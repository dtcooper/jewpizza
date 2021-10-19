from django.urls import path

from .views import ScriptView


app_name = "radio"
urlpatterns = [
    path("script/radio/", ScriptView.as_view(template_name="radio/scripts/radio.liq"), name="script-radio"),
    path("script/uplink/", ScriptView.as_view(template_name="radio/scripts/uplink.liq"), name="script-uplink"),
]
