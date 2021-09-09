import random

from jinja2 import Environment

from django.conf import settings
from django.templatetags.static import static as django_static
from django.urls import reverse


def shuffle(items):
    try:
        random.shuffle(items)
        return items
    except Exception:
        return items


def static(path, *args, **kwargs):
    if not settings.DEBUG:
        for ext in ('.js', '.css'):
            if path.endswith(ext) and not path.endswith(f'.min{ext}'):
                path = f"{path.removesuffix(ext)}.min{ext}"
    return django_static(path, *args, **kwargs)


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "randint": random.randint,
            "settings": settings,
            "shuffle": shuffle,
            "static": static,
            "url": reverse,
        }
    )
    return env
