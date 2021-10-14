import logging

import requests

from django.conf import settings
from django.contrib import messages

SUBSTACK_HOST = f"{settings.SUBSTACK_NAME}.substack.com"
SUBSTACK_URL = f"https://{SUBSTACK_HOST}"
SUBSTACK_URL_EMBED = f"{SUBSTACK_URL}/embed"
SUBSTACK_URL_API = f"{SUBSTACK_URL}/api/v1/free"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81"
    " Safari/537.36"
)

logger = logging.getLogger(f"jewpizza.{__name__}")


def sign_up_for_substack(email, request=None):
    # Sketchy, brittle, but returns False if we encountered an error for graceful downgrade
    try:
        response = requests.post(
            SUBSTACK_URL_API,
            headers={
                "user-agent": request.headers.get("User-Agent", DEFAULT_USER_AGENT) if request else DEFAULT_USER_AGENT,
                "authority": SUBSTACK_HOST,
                "origin": SUBSTACK_URL,
                "referer": SUBSTACK_URL_EMBED,
                "content-type": "application/json",
            },
            json={
                "email": email,
                "first_url": SUBSTACK_URL_EMBED,
                "first_referrer": "",
                "current_url": SUBSTACK_URL_EMBED,
                "current_referrer": "",
                "referral_code": "",
                "source": "embed",
            },
        )
        response.raise_for_status()
        data = response.json()

        for key in ("email", "didSignup", "requires_confirmation", "subscription_id"):
            if key not in data:
                raise Exception(f'Expecting key "{key}" in data payload from Substack. Got: {data!r}')
    except Exception:
        django_logger = logging.getLogger("django.request")
        django_logger.exception("An error occurred while subscribing a user to Substack")
        if request:
            messages.error(request, "An error occurred while signing you up for the newsletter. Please try again.")
        return False

    logger.info(f"Got payload from Substack: {data!r}")

    if request:
        if data["didSignup"] or data["requires_confirmation"]:
            messages.success(request, "You were successfully signed up for the newsletter. Please check your inbox.")
        else:
            messages.info(request, "You were already signed up for the newsletter.")

    return True
