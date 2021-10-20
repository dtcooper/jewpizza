import logging

import requests

from django.utils.formats import date_format as django_date_format
from django.utils.timezone import localtime


CONTROLLER_URL = "http://controller:8080/"
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


def restart_container(container, fail_silently=False):
    try:
        response = requests.get(f"{CONTROLLER_URL}/containers/restart", params={"container": container})
        response.raise_for_status()
    except Exception:
        if not fail_silently:
            raise
        logger.exception(f"Ignoring exception restart_container({container!r})")
        return False
    return True


def list_containers(fail_silently=False):
    try:
        response = requests.get(f"{CONTROLLER_URL}/containers/list")
        response.raise_for_status()
        containers, running = map(lambda s: s.strip().splitlines(), response.text.split("== UP =="))
    except Exception:
        if not fail_silently:
            logger.exception("Ignoring exception list_containers()")
            raise
        return []

    running = set(running)
    return sorted((container, container in running) for container in containers if container != "controller")
