from collections import namedtuple
import json
import logging

import requests

from django.conf import settings
from django.utils.formats import date_format as django_date_format
from django.utils.timezone import localtime

from constance import config
from django_redis import get_redis_connection

from jew_pizza.constants import REDIS_PUBSUB_CHANNEL


ContainerInfo = namedtuple("ContainerInfo", "name state ports logs_url cpu_info mem_info")
logger = logging.getLogger("jewpizza.{__name__}")


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip or "[unknown]"


def format_datetime(dt, format="N j, Y g:i A"):
    return django_date_format(localtime(dt), format)


def format_datetime_short(dt):
    return format_datetime(localtime(dt), format="n/j/y g:i A")


def format_date_short(date):
    return django_date_format(date, format="n/j/y")


def _call_controller(cmd, fail_silently=False, params=None, json=False):
    try:
        response = requests.get(f"http://controller:8080/{cmd}", params=params)
        response.raise_for_status()
    except Exception:
        if not fail_silently:
            raise
        logger.exception(f"_call_controller() failed with cmd {cmd!r}")
        return None
    else:
        return response.json() if json else response.text.strip()


def restart_container(container, fail_silently=False):
    return _call_controller("restart", fail_silently=True, params={"container": container}) is not None


def list_containers(fail_silently=False):
    if not (response := _call_controller("list", fail_silently=fail_silently)):
        return []

    containers_names = response.splitlines()

    containers_ps = {}
    if response := _call_controller("ps", fail_silently=fail_silently, json=True):
        containers_ps = {c["Service"]: c for c in response}

    containers_stats = {}
    if response := _call_controller("stats", fail_silently=fail_silently):
        containers_stats = {s.split("\t")[0]: s.split("\t")[1:] for s in response.splitlines()}

    containers = []
    for container in containers_names:
        ps = containers_ps.get(container, {})
        state = ps.get("State", "destroyed")
        ports = []
        for p in ps.get("Publishers") or []:
            port = p["PublishedPort"]
            if port != 0:
                addr = ""
                if p["URL"] == "127.0.0.1":
                    addr = "localhost:"
                elif p["URL"] != "0.0.0.0":
                    addr = f"{p['URL']}:"
                ports.append(f"{addr}{port}/{p['Protocol']}")

        mem_info = cpu_info = logs_url = None
        if container_id := ps.get("ID"):
            # dozzle specific logs URL
            logs_url = f'{config.LOGS_URL.removesuffix("/")}/container/{container_id[:12]}'
            if stats := containers_stats.get(container_id):
                cpu_info, mem_info = stats
        containers.append(ContainerInfo(container, state, ports, logs_url, cpu_info, mem_info))
    return containers


def send_sse_message(message_type, message, delay=None):
    message = json.dumps({"type": message_type, "message": message, "delay": delay})
    redis = get_redis_connection()
    redis.publish(REDIS_PUBSUB_CHANNEL, message)


def settings_template_context(request):
    # Template context processor for Django templates
    return {"settings": settings}
