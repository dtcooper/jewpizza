from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("webcore.urls")),
    path("cmsadmin/", admin.site.urls),
    path("markdownx/", include("markdownx.urls")),
]
