from django.contrib import admin
from django.urls import include, path


admin.site.index_title = admin.site.site_header = "jew.pizza administration"
admin.site.site_title = "jew.pizza site admin"

urlpatterns = [
    path("", include("webcore.urls")),
    path("", include("notifications.urls")),
    path("", include("shows.urls")),
    path("internal/radio/", include("radio.urls")),
    path("cmsadmin/tools/", include("admin_tools.urls")),
    path("cmsadmin/", admin.site.urls),
    path("js_error_hook/", include("django_js_error_hook.urls")),
]
