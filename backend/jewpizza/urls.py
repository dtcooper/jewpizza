from django.contrib import admin
from django.urls import path, re_path

from api.views import server_logs

urlpatterns = [
    re_path("cmsadmin/tools/logs/.*", server_logs),
    path("cmsadmin/", admin.site.urls),
]
