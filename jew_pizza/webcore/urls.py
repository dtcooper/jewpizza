from django.urls import path
from django.views.generic import TemplateView

import webcore.views as views


app_name = 'webcore'
urlpatterns = [
    path('', views.PlaceholderView.as_view(), name='placeholder'),
    path('index/', views.IndexView.as_view(), name='index'),
]
