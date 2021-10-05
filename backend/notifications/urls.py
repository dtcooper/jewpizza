from django.urls import path

from .views import SignUpConfirmationView, SignUpView, incoming_sms_view

app_name = "notifications"
urlpatterns = [
    path("notify/", SignUpView.as_view(), name="sign-up"),
    path("notify/<path:token>/", SignUpConfirmationView.as_view(), name="sign-up-confirm"),
    path("incoming-sms/", incoming_sms_view, name="incoming-sms"),
]
