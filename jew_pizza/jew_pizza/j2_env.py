import random

from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse

from jinja2 import contextfilter, Environment


def shuffle(items):
    try:
        random.shuffle(items)
        return items
    except:
        return items


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'randint': random.randint,
        'settings': settings,
        'shuffle': shuffle,
        'static': static,
        'url': reverse,
    })
    return env
