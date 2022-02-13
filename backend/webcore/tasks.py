from huey.contrib import djhuey

from jew_pizza.utils import send_sse_message


@djhuey.task()
def send_sse_message_async(message_type, message):
    send_sse_message(message_type, message)
