from django.urls import path, re_path

from . import views


app_name = "admin-tools"
urlpatterns = [
    path("", views.AdminTemplateView.as_view(title="Tools Index"), name="index"),
    path("send-text-message/", views.SendTextMessageView.as_view(), name="send-text-message"),
    path("send-email/", views.SendEmailView.as_view(), name="send-email"),
    path(
        "sse-status/",
        views.AdminTemplateView.as_view(title="SSE Status", template_name="admin_tools/sse_status.html"),
        name="sse-status",
    ),
    re_path("^(?P<module>logs|nchan|nginx)/.*", views.NginxInternalView.as_view(), name="nginx-internal"),
]
