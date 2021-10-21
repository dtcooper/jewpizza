import random

from huey import crontab

from huey.contrib import djhuey

from jew_pizza.utils import send_sse_message


@djhuey.periodic_task(crontab())
def test_metadata():
    send_sse_message("metadata", {"title": f"test metadata from backend [{random.randint(100000, 999999)}]"})
