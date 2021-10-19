from collections import namedtuple
import hashlib
import os
import random
import string

from jinja2 import BytecodeCache, Environment, pass_context, pass_eval_context
from jinja2.filters import do_forceescape, do_tojson

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.templatetags.static import static as django_static
from django.urls import reverse

from constance import config as constance_config
from widget_tweaks.templatetags.widget_tweaks import add_class, add_error_class, set_attr

from webcore import constants

from .utils import format_datetime, format_datetime_short


NavLink = namedtuple("NavLink", "name url url_name icon is_subnav is_active")


def get_messages(request):
    return [{"level": msg.level_tag, "message": msg.message} for msg in messages.get_messages(request)]


@pass_context
def _get_messages_jinja2(ctx):
    return get_messages(ctx["request"])


def shuffle(items):
    random.shuffle(items)
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
                cache_key = f"{constants.CACHE_KEY_PREFIX_STATIC_ASSET_MD5SUM}{path}"
                # Now compute (or get from cache) md5 sum of file
                path_hash = cache.get(cache_key)
                if path_hash is None:
                    local_path = os.path.join(settings.STATIC_ROOT, path)
                    if os.path.exists(local_path):
                        with open(local_path, "rb") as file_to_check:
                            path_hash = hashlib.md5(file_to_check.read()).hexdigest()
                    else:
                        path_hash = False  # File not found, cache that fact using False
                    cache.set(cache_key, path_hash, timeout=None)

    static_path = django_static(path, *args, **kwargs)
    if path_hash:
        static_path = f"{static_path}?v={path_hash}"
    return static_path


def url_for(name, *args, **kwargs):
    return reverse(name, args=args, kwargs=kwargs)


@pass_eval_context
def attrjs(eval_ctx, value):
    return do_forceescape(do_tojson(eval_ctx, value))


def smart_title(s):
    return " ".join(f"{w[0:1].upper()}{w[1:]}" for w in s.split())


def nav_links(request):
    nav_links = []
    active_link = None

    for name, url_name, icon, is_subnav in constants.NAVIGATION_LINKS:
        url = reverse(url_name)
        is_active = request.resolver_match.view_name == url_name
        nav_links.append(NavLink(name, url, url_name, icon, is_subnav, is_active))
        if is_active:
            active_link = url

    return {"nav_links": nav_links, "active_link": active_link}


def __encoded_email():
    printable = string.ascii_letters + string.digits + string.printable + ".....@@@@@"

    encoded = ""
    for i, c in enumerate(settings.EMAIL_ADDRESS, 1):
        encoded += f'{c}{"".join(random.choice(printable) for _ in range(i))}'
    return encoded


# https://gist.github.com/rtt/5029885
class RedisBytecodeCache(BytecodeCache):
    CACHE_KEY_PREFIX = "jinja2:cache:"

    def load_bytecode(self, bucket):
        bytecode = cache.get(f"{self.CACHE_KEY_PREFIX}{bucket.key}")
        if bytecode:
            bucket.bytecode_from_string(bytecode)

    def dump_bytecode(self, bucket):
        cache.set(f"{self.CACHE_KEY_PREFIX}{bucket.key}", bucket.bytecode_to_string(), timeout=None)


def autoescape(filename):
    return any(filename.endswith(ext) for ext in (".xml", ".html"))


def create_environment(**options):
    options.update(
        {
            "autoescape": autoescape,
            "bytecode_cache": RedisBytecodeCache(),
            "extensions": [
                "jinja2.ext.debug",
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                "jinja_markdown.MarkdownExtension",
            ],
            "keep_trailing_newline": True,
        }
    )

    env = Environment(**options)
    env.globals.update(
        {
            "choice": random.choice,
            "config": constance_config,
            "encoded_email": __encoded_email(),
            "get_messages": _get_messages_jinja2,
            "jewippy_gifs": [{**img, "url": static(img["url"])} for img in constants.JEWIPPY_GIFS],
            "randint": random.randint,
            "settings": settings,
            "shuffle": shuffle,
            "static": static,
            "url_for": url_for,
        }
    )
    env.filters.update(
        {
            "add_attr": set_attr,
            "add_class": add_class,
            "add_error_class": add_error_class,
            "attrjs": attrjs,
            "bool": bool,
            "date": format_datetime,
            "dateshort": format_datetime_short,
            "smart_title": smart_title,
        }
    )
    return env
