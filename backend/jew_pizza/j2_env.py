from collections import namedtuple
import hashlib
import os
import random

from jinja2 import Environment

from django.conf import settings
from django.core.cache import cache
from django.templatetags.static import static as django_static
from django.urls import reverse

from webcore.constants import CACHE_KEY_PREFIX_STATIC_ASSET_MD5SUM, NAVIGATION_LINKS

Link = namedtuple("Link", ("name", "url", "icon", "is_subnav", "is_active"))


def shuffle(items):
    try:
        random.shuffle(items)
        return items
    except Exception:
        return items


def static(path, *args, **kwargs):
    path_hash = None

    for ext in (".js", ".css"):
        if path.endswith(ext):
            if settings.DEBUG:
                # In DEBUG, use a simple random fake md5 hash
                path_hash = "{:032x}".format(random.randrange(16 ** 32))
            elif not path.endswith(f".min{ext}"):
                # If we're not requesting the minified version in prod, swap it out
                path = f"{path.removesuffix(ext)}.min{ext}"

            if not path_hash:
                cache_key = f"{CACHE_KEY_PREFIX_STATIC_ASSET_MD5SUM}{path}"
                # Now compute (or get from cache) md5 sum of file
                path_hash = cache.get(cache_key)
                if path_hash is None:
                    local_path = os.path.join(settings.STATIC_ROOT, path)
                    if os.path.exists(local_path):
                        with open(local_path, "rb") as file_to_check:
                            path_hash = hashlib.md5(file_to_check.read()).hexdigest()
                    else:
                        path_hash = False  # File not found, cache that fact using False
                    cache.set(cache_key, path_hash)

    static_path = django_static(path, *args, **kwargs)
    if path_hash:
        static_path = f"{static_path}?v={path_hash}"
    return static_path


def navigation_links(request):
    navigation_links = []
    for name, url_name, icon, is_subnav in NAVIGATION_LINKS:
        is_active = request.resolver_match.view_name == url_name
        url = reverse(url_name) if url_name else "#"  # XXX allow stubs as empty string
        navigation_links.append(Link(name=name, url=url, icon=icon, is_subnav=is_subnav, is_active=is_active))

    return {"navigation_links": navigation_links}


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "randint": random.randint,
            "settings": settings,
            "shuffle": shuffle,
            "static": static,
            "url_for": lambda name, *args, **kwargs: reverse(name, args=args, kwargs=kwargs),
        }
    )
    env.filters.update(
        {
            "bool": bool,
        }
    )
    return env
