import hashlib
import os
import random

from jinja2 import Environment

from django.conf import settings
from django.templatetags.static import static as django_static
from django.urls import reverse

STATIC_FILES_SUM_CACHE = {}


def shuffle(items):
    try:
        random.shuffle(items)
        return items
    except Exception:
        return items


def static(path, *args, **kwargs):
    path_hash = None

    if not settings.DEBUG:
        for ext in (".js", ".css"):
            if path.endswith(ext):
                if not path.endswith(f".min{ext}"):
                    path = f"{path.removesuffix(ext)}.min{ext}"

                path_hash = STATIC_FILES_SUM_CACHE.get(path)
                if path_hash is None:
                    local_path = os.path.join(settings.STATIC_ROOT, path)
                    if os.path.exists(local_path):
                        with open(local_path, "rb") as file_to_check:
                            path_hash = hashlib.md5(file_to_check.read()).hexdigest()
                    else:
                        path_hash = False
                    STATIC_FILES_SUM_CACHE[path] = path_hash

    static_path = django_static(path, *args, **kwargs)
    if path_hash:
        static_path = f"{static_path}?v={path_hash}"
    return static_path


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "settings": settings,
            "shuffle": shuffle,
            "static": static,
            "url": reverse,
        }
    )
    return env
