import logging

import requests

from django.contrib import messages

from constance import config


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81"
    " Safari/537.36"
)

logger = logging.getLogger(f"jewpizza.{__name__}")


def sign_up_for_substack(email, request=None):
    substack_host = f"{config.SUBSTACK_NAME}.substack.com"
    substack_url = f"https://{substack_host}"
    substack_url_embed = f"{substack_url}/embed"
    substack_url_api = f"{substack_url}/api/v1/free"

    # Sketchy, brittle, but returns False if we encountered an error for graceful downgrade
    try:
        response = requests.post(
            substack_url_api,
            headers={
                "user-agent": request.headers.get("User-Agent", DEFAULT_USER_AGENT) if request else DEFAULT_USER_AGENT,
                "authority": substack_host,
                "origin": substack_url,
                "referer": substack_url_embed,
                "content-type": "application/json",
            },
            json={
                "email": email,
                "first_url": substack_url_embed,
                "first_referrer": "",
                "current_url": substack_url_embed,
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

    logger.info(f"Got payload from Substack submitting {email!r}: {data!r}")

    if request:
        if data["didSignup"] or data["requires_confirmation"]:
            messages.success(request, "You were successfully signed up for the newsletter. Please check your inbox.")
        else:
            messages.info(request, "You were already signed up for the newsletter.")

    return True
