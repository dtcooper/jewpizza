from django.http import Http404
from django.views.generic import DetailView, ListView, TemplateView

from .constants import SHOW_CODES_TO_SHOW, SHOWS
from .models import Episode


class ShowsMasterListView(TemplateView):
    template_name = "shows/show_master_list.html"
    extra_context = {"title": "Shows", "shows": SHOWS}
    MAX_EPISODES_PER_SHOW = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["episodes_for_shows"] = {
            show.code: list(Episode.objects.filter(show=show.code).order_by("-start")[: self.MAX_EPISODES_PER_SHOW])
            for show in SHOWS
        }
        return context


class ShowContextMixin:
    def get_context_data(self, **kwargs):
        show = SHOW_CODES_TO_SHOW.get(self.kwargs["show"])
        if not show:
            raise Http404

        return {**super().get_context_data(**kwargs), "show": show}


class ShowListView(ShowContextMixin, ListView):
    template_name = "shows/show_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show = context["show"]
        return {**context, "title": show.name, "hide_title": True}

    def get_queryset(self):
        return Episode.objects.filter(show=self.kwargs["show"])


class ShowDetailView(ShowContextMixin, DetailView):
    template_name = "shows/show_detail.html"


class PodcastRSSView(ShowContextMixin, TemplateView):
    template_name = "shows/podcast_rss.xml"
    content_type = "application/xml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, "podcast": context["show"].podcast}
