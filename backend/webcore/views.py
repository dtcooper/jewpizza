import datetime

from pytz import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class PlaceholderView(TemplateView):
    template_name = "webcore/placeholder.html"
    extra_context = {"title": "jew.pizza - David Cooper"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eastern_tz_abbrev'] = timezone("US/Eastern").localize(datetime.datetime.now()).tzname()
        test_tz = self.request.GET.get('testtz')
        if 'testtz' in self.request.GET:
            context['js_data'] = {'test_tz': test_tz}
        return context


class IndexView(LoginRequiredMixin, TemplateView):
    raise_exception = True  # XXX Delete me when LoginRequiredMixin removed
    template_name = "webcore/index.html"
    extra_context = {"title": "jew.pizza - David Cooper"}
