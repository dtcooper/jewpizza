from django.urls import path

from . import views


app_name = "shows"
urlpatterns = [
    path("shows/", views.ShowsMasterListView.as_view(), name="show-master-list"),
    path("listen/", views.ListenView.as_view(), name="listen"),
    path("shows/<show:show>/", views.ShowListView.as_view(), name="show-list"),
    path("shows/<show:show>/<slug:slug>/", views.ShowDetailView.as_view(), name="show-detail"),
    path("podcasts/<podcast:show>.rss", views.PodcastRSSView.as_view(), name="podcast-rss"),
]
