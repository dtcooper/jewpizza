from django.contrib import admin
from django.urls import path

from jew_pizza import views


urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
]
