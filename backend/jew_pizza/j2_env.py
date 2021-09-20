import hashlib
import os
import random

from jinja2 import Environment

from django.conf import settings
from django.core.cache import cache
from django.templatetags.static import static as django_static
from django.urls import reverse

from webcore.constants import CACHE_KEY_PREFIX_STATIC_ASSET_MD5SUM


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
            # If we're not requesting the minified version
            if not path.endswith(f".min{ext}"):
                if settings.DEBUG:
                    # In DEBUG, use a simple random fake md5 hash
                    path_hash = "{:032x}".format(random.randrange(16 ** 32))
                else:
                    # In prod, swap out to request the minified version
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


def environment(**options):
    from webcore.models import ContentBlock

    env = Environment(**options)
    env.globals.update(
        {
            "content_block": ContentBlock.render_content_block,
            "settings": settings,
            "shuffle": shuffle,
            "static": static,
            "url_for": lambda name, *args, **kwargs: reverse(name, args=args, kwargs=kwargs),
        }
    )
    return env
