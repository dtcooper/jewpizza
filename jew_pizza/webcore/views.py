import datetime

from pytz import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class PlaceholderView(TemplateView):
    template_name = 'webcore/placeholder.html'
    extra_context = {'title': 'jew.pizza - David Cooper'}

    def get_context_data(self, **kwargs):
        return {
            'eastern_tz_abbrev': timezone('US/Eastern').localize(datetime.datetime.now()).tzname(),
            **super().get_context_data(**kwargs),
        }

class IndexView(LoginRequiredMixin, TemplateView):
    raise_exception = True  # XXX Delete me when LoginRequiredMixin removed
    template_name = 'webcore/index.html'
    extra_context = {'title': 'jew.pizza - David Cooper'}
