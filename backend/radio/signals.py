import logging

from django.dispatch import receiver

from jew_pizza.signals import config_updated_in_admin
from jew_pizza.utils import restart_container


logger = logging.getLogger(f"jewpizza.{__name__}")


@receiver(config_updated_in_admin)
def constance_updated(changes, **kwargs):
    if any(change.startswith("ICECAST_") and change != "ICECAST_URL" for change in changes):
        restart_container("radio-uplink", fail_silently=True)
