import base64
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


def get_cached_file_hash(path):
    if settings.DEBUG:
        return "{:032x}".format(random.randrange(16 ** 32))
    else:
        cache_key = f"{constants.CACHE_KEY_PREFIX_STATIC_ASSET_HASH}{path}"
        file_hash = cache.get(cache_key)

        if file_hash is None:
            full_path = os.path.join(settings.STATIC_ROOT, path)
            if os.path.exists(full_path):
                hash = hashlib.md5()
                with open(full_path, "rb") as file:
                    while chunk := file.read(32 * 1024):
                        hash.update(chunk)
                file_hash = hash.hexdigest()
            else:
                file_hash = False
            cache.set(cache_key, file_hash, timeout=None)
        return file_hash


def static(path, no_hash=False, *args, **kwargs):
    file_hash = None

    if not no_hash:
        for ext in (".js", ".css"):
            if path.endswith(ext) and not path.endswith(f".min{ext}") and not settings.DEBUG:
                # If we're not requesting the minified version in prod, swap it out
                path = f"{path.removesuffix(ext)}.min{ext}"
        file_hash = get_cached_file_hash(path)

    static_path = django_static(path, *args, **kwargs)
    if file_hash:
        static_path = f"{static_path}?v={file_hash}"
    return static_path


def url_for(name, *args, **kwargs):
    return reverse(name, args=args, kwargs=kwargs)


@pass_eval_context
def attrjs(eval_ctx, value):
    return do_forceescape(do_tojson(eval_ctx, value))


def smart_title(s):
    return " ".join(f"{w[0:1].upper()}{w[1:]}" for w in s.split())


def liqval(value, comment_string=True):
    if isinstance(value, bool):
        encoded = str(value).lower()

    elif isinstance(value, float):
        encoded = f"{value:.5g}"  # 5 decimal places
        if "." not in encoded:
            encoded += "."

    elif isinstance(value, int):
        encoded = value

    else:
        if not isinstance(value, str):
            value = str(value)

        # Best way to encode a string, since it's not exactly documented escape
        # characters properly for liquidsoap.
        # TODO: look at liquidsoap v2 docs to see if there's a better way
        encoded = base64.b64encode(value.encode("utf-8")).decode("utf-8")
        encoded = f'string.base64.decode("{encoded}")'
        if comment_string:
            encoded += f"  # {value!r}"

    return encoded


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
            "jewippy_gifs": [{**i, "webp": static(i["webp"]), "gif": static(i["gif"])} for i in constants.JEWIPPY_GIFS],
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
            "liqval": liqval,
            "smart_title": smart_title,
        }
    )
    return env
