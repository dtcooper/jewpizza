import datetime

from pytz import timezone

from django.shortcuts import render


def index(request):

    return render(request, 'webcore/index.html', {
        'title': 'jew.pizza - David Cooper',
        'eastern_tz_abbrev': timezone('US/Eastern').localize(datetime.datetime.now()).tzname()
    })
