from collections import namedtuple
import logging

import requests

from django.utils.formats import date_format as django_date_format
from django.utils.timezone import localtime

from constance import config


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


def _call_controller(cmd, fail_silently=False, params=None, json=False):
    try:
        response = requests.get(f"http://controller:8080/{cmd}", params=params)
        response.raise_for_status()
    except Exception:
        if not fail_silently:
            raise
        return None
    else:
        return response.json() if json else response.text.strip()


def restart_container(container, fail_silently=False):
    return _call_controller("restart", fail_silently=True, params={"container": container}) is not None


ContainerInfo = namedtuple("ContainerInfo", "name state ports logs_url")


def list_containers(fail_silently=False):
    response = _call_controller("list", fail_silently=fail_silently)
    if not response:
        return []

    containers_names = response.splitlines()
    containers_ps = {c["Service"]: c for c in _call_controller("ps", fail_silently=fail_silently, json=True)}
    import pprint

    pprint.pprint(containers_ps)
    containers = []
    for container in containers_names:
        ps = containers_ps.get(container, {})
        state = ps.get("State", "destroyed")
        ports = sorted(
            f"{p['URL']}:{p['PublishedPort']}/{p['Protocol']}"
            for p in (ps.get("Publishers") or [])
            if p["PublishedPort"] > 0
        )
        logs_url = None
        container_id = ps.get("ID")
        if container_id:
            # dozzle specific
            logs_url = f'{config.LOGS_URL.removesuffix("/")}/container/{container_id[:12]}'
        containers.append(ContainerInfo(container, state, ports, logs_url))
    return containers
