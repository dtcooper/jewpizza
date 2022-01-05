from collections import namedtuple
import datetime
import hashlib
import json
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
from django.utils.timezone import get_default_timezone

from constance import config as constance_config
from widget_tweaks.templatetags.widget_tweaks import add_class, add_error_class, set_attr

from webcore import constants

from .utils import format_date, format_date_short, format_datetime, format_datetime_short, format_time


NavLink = namedtuple("NavLink", "name url url_name icon is_subnav is_active")


def get_messages(request):
    return [{"level": msg.level_tag, "message": msg.message} for msg in messages.get_messages(request)]


@pass_context
def get_messages_jinja2(ctx):
    return get_messages(ctx["request"])


def shuffle(items):
    random.shuffle(items)
    return items


def get_cached_file_hash(path):
    file_hash = None

    if settings.DEBUG:
        if any(path.endswith(ext) and not path.endswith(f".min{ext}") for ext in (".js", ".css")):
            # Reload all JS and CSS in DEBUG
            file_hash = "{:032x}".format(random.randrange(16 ** 32))
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


@pass_context
def static(ctx, path, *args, **kwargs):
    no_hash = kwargs.pop("_no_hash", False)
    file_hash = None

    if not no_hash:
        for ext in (".js", ".css"):
            if path.endswith(ext) and not path.endswith(f".min{ext}") and not settings.DEBUG:
                # If we're not requesting the minified version in prod, swap it out
                path = f"{path.removesuffix(ext)}.min{ext}"
        file_hash = get_cached_file_hash(path)

    absolute = kwargs.pop("_external", False)
    static_path = django_static(path, *args, **kwargs)
    if file_hash:
        static_path = f"{static_path}?v={file_hash}"
    if absolute:
        static_path = ctx["request"].build_absolute_uri(static_path)
    return static_path


@pass_context
def url_for(ctx, name, *args, **kwargs):
    absolute = kwargs.pop("_external", False)
    path = reverse(name, args=args, kwargs=kwargs)
    if absolute:
        path = ctx["request"].build_absolute_uri(path)
    return path


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

        #  #{ => #"^"{ to skip interpolation
        encoded = json.dumps(value).replace("#{", '#"^"{')

    return encoded


def nav_links(request):
    nav_links = []
    active_url = None
    active_url_name = request.resolver_match.view_name if request.resolver_match else None

    for name, url_name, icon, is_subnav in constants.NAVIGATION_LINKS:
        url = reverse(url_name)
        is_active = active_url_name == url_name if request.resolver_match else False
        nav_links.append(NavLink(name, url, url_name, icon, is_subnav, is_active))
        if is_active:
            active_url = url

    return {"nav_links": nav_links, "active_url": active_url, "active_url_name": active_url_name}


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
    return any(filename.endswith(ext) for ext in (".xml", ".html")) if isinstance(filename, str) else True


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
            "get_messages": get_messages_jinja2,
            "jewippy_gifs": [
                {**i, "webp": static(path=i["webp"], ctx=None), "gif": static(path=i["gif"], ctx=None)}
                for i in constants.JEWIPPY_GIFS
            ],
            "now": lambda: datetime.datetime.now(get_default_timezone()),
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
            "datetime": format_datetime,
            "date": format_date,
            "dateshort": format_date_short,
            "datetimeshort": format_datetime_short,
            "time": format_time,
            "liqval": liqval,
            "smart_title": smart_title,
        }
    )
    return env
