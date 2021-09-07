import datetime

from pytz import timezone

from django.views.generic import TemplateView


class PlaceholderView(TemplateView):
    template_name = 'webcore/placeholder.html'
    extra_context = {'title': 'jew.pizza - David Cooper'}

    def get_context_data(self, **kwargs):
        return {
            'eastern_tz_abbrev': timezone('US/Eastern').localize(datetime.datetime.now()).tzname(),
            **super().get_context_data(**kwargs),
        }
