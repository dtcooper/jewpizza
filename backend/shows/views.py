from django.views.generic import TemplateView

from .constants import SHOWS
from .models import Episode


class ShowsMasterListView(TemplateView):
    template_name = "shows/shows_master_list.html"
    extra_context = {"title": "Shows", "shows": SHOWS}
    MAX_EPISODES_PER_SHOW = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['episodes_for_shows'] = {
            show.code: list(Episode.objects.filter(show=show.code).order_by('-start')[:self.MAX_EPISODES_PER_SHOW])
            for show in SHOWS
        }
        return context
