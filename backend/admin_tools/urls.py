from django.urls import path

from . import views


app_name = "admin-tools"
urlpatterns = [
    path("", views.AdminTemplateView.as_view(title="Tools Index"), name="index"),
    path("container-status/", views.ContainerStatusView.as_view(), name="container-status"),
    path("send-text-message/", views.SendTextMessageView.as_view(), name="send-text-message"),
    path("send-email/", views.SendEmailView.as_view(), name="send-email"),
]
