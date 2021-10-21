import logging

from django.contrib import messages
from django.dispatch import receiver

from jew_pizza.signals import config_updated_in_admin
from jew_pizza.utils import restart_container


logger = logging.getLogger(f"jewpizza.{__name__}")


@receiver(config_updated_in_admin)
def constance_updated(changes, request=None, **kwargs):
    if any(change.startswith("ICECAST_") and change != "ICECAST_URL" for change in changes):
        status = restart_container("radio", fail_silently=True)
        if request:
            if status:
                messages.info(request, "radio container restarted")
            else:
                messages.error(request, "There was an error restarting the radio container. See server logs.")
