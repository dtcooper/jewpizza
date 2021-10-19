import logging

import requests
from requests.exceptions import RequestException

from django.contrib import messages
from django.dispatch import receiver

from webcore.signals import config_updated_in_admin


logger = logging.getLogger(f"jewpizza.{__name__}")


@receiver(config_updated_in_admin)
def constance_updated(changes, **kwargs):
    if any(change.startswith("ICECAST_") and change != "ICECAST_URL" for change in changes):
        try:
            response = requests.get("http://radio-controller:8080/restart/uplink/")
            response.raise_for_status()
            logger.info("Restarted radio-uplink")
        except RequestException:
            logger.exception("Failed to restart radio-uplink")
