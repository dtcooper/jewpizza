from collections import namedtuple
import hashlib
import os
import random
import textwrap

from jinja2 import BytecodeCache, Environment, pass_context, pass_eval_context
from jinja2.filters import do_forceescape, do_tojson

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.templatetags.static import static as django_static
from django.urls import reverse

from widget_tweaks.templatetags.widget_tweaks import add_class, add_error_class, set_attr
from django_redis import get_redis_connection

from webcore.constants import CACHE_KEY_PREFIX_STATIC_ASSET_MD5SUM, NAVIGATION_LINKS

NavLink = namedtuple("NavLink", "name url url_name icon is_subnav is_active")


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


def nav_links(request):
    nav_links = []
    active_link = None

    for name, url_name, icon, is_subnav in NAVIGATION_LINKS:
        url = reverse(url_name)
        is_active = request.resolver_match.view_name == url_name
        nav_links.append(NavLink(name, url, url_name, icon, is_subnav, is_active))
        if is_active:
            active_link = url

    return {"nav_links": nav_links, "active_link": active_link}


def get_messages(request):
    return [{"level": msg.level_tag, "message": msg.message} for msg in messages.get_messages(request)]


# https://gist.github.com/rtt/5029885
class RedisBytecodeCache(BytecodeCache):
    CACHE_KEY_PREFIX = "jinja2:cache:"

    def __init__(self):
        self.redis = get_redis_connection()

    def load_bytecode(self, bucket):
        bytecode = self.redis.get(f"{self.CACHE_KEY_PREFIX}{bucket.key}")
        if bytecode:
            bucket.bytecode_from_string(bytecode)

    def dump_bytecode(self, bucket):
        self.redis.set(f"{self.CACHE_KEY_PREFIX}{bucket.key}", bucket.bytecode_to_string())


def environment(**options):
    env = Environment(bytecode_cache=RedisBytecodeCache(), **options)
    env.globals.update(
        {
            "randint": random.randint,
            "settings": settings,
            "shuffle": lambda items: random.shuffle(items) or items,  # Hack since shuffle returns None
            "static": static,
            "url_for": lambda name, *args, **kwargs: reverse(name, args=args, kwargs=kwargs),
            "get_messages": pass_context(lambda ctx: get_messages(ctx["request"])),
        }
    )
    env.filters.update(
        {
            "add_class": add_class,
            "add_error_class": add_error_class,
            "attr": set_attr,
            "attrjs": pass_eval_context(lambda eval_ctx, value: do_forceescape(do_tojson(eval_ctx, value))),
            "bool": bool,
            "smart_title": lambda s: " ".join(f"{w[0].upper()}{w[1:]}" for w in s.split()),
        }
    )
    return env
