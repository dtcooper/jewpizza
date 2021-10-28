from django.http import Http404
from django.views.generic import DetailView, ListView, TemplateView

from .constants import SHOW_CODES_TO_SHOW, SHOWS
from .models import Episode


class ShowsMasterListView(TemplateView):
    template_name = "shows/show_master_list.html"
    extra_context = {"title": "Shows"}
    MAX_EPISODES_PER_SHOW = 3

    def get_context_data(self, **kwargs):
        shows_and_episodes = tuple(
            (show, list(Episode.objects.filter(show_code=show.code).order_by("-date")[: self.MAX_EPISODES_PER_SHOW]))
            for show in SHOWS
        )
        return {**super().get_context_data(**kwargs), 'shows_and_episodes': shows_and_episodes}


class ShowListView(ListView):
    template_name = "shows/show_list.html"
    model = Episode

    def get_context_data(self, **kwargs):
        show = self.kwargs['show']
        return {**super().get_context_data(**kwargs), "show": show, "title": show.name, "hide_title": True}

    def get_queryset(self):
        return Episode.objects.filter(show_code=self.kwargs['show'].code)


class ShowDetailView(DetailView):
    template_name = "shows/show_detail.html"
    model = Episode

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show = self.kwargs['show']
        episode = context['episode']
        return {**context, "show": show, "title": episode.name}


class PodcastRSSView(TemplateView):
    template_name = "shows/podcast_rss.xml"
    content_type = "application/xml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, "podcast": context["show"].podcast}
