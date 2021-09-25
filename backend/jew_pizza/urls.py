from django.contrib import admin
from django.urls import include, path

admin.site.index_title = admin.site.site_header = "jew.pizza administration"
admin.site.site_title = "jew.pizza site admin"

urlpatterns = [
    path("", include("webcore.urls")),
    path("shows/", include("shows.urls")),
    path("cmsadmin/", admin.site.urls),
]
