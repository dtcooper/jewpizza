from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "admin-tools"
urlpatterns = [
    path("", views.AdminTemplateView.as_view(title='Tools Index'), name='index'),
    path("send-text-message/", views.SendTextMessageView.as_view(), name='send-text-message'),
]
