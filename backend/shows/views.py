from django.views.generic import TemplateView

from .constants import SHOWS


class ShowsMasterListView(TemplateView):
    template_name = "shows/shows_master_list.html"
    extra_context = {"title": "Shows", "shows": SHOWS}
