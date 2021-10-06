from django.urls import path

from . import views

app_name = "notifications"
urlpatterns = [
    path("notify/", views.SignUpView.as_view(), name="sign-up"),
    path("notify/<path:token>/", views.SignUpConfirmationView.as_view(), name="sign-up-confirm"),
    path("incoming-sms/", views.incoming_sms_view, name="incoming-sms"),
    path("cmsadmin/notifications/send/", views.SendNotificationAdminView.as_view(), name='send-notification'),
]
