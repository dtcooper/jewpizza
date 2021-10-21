#
# Dead simple server-sent event (SSE) server. No authentication, no frills.
# Server is protected by nginx's "internal" flag and authenticated by Django
# and an X-Accel-Redirect
#
# GET:/ -- subscribes to messages
# GET:/test -- test page
#
# Publish valid JSON strings to redis channel sse::messages
# They must have the keys {"type": "<type", "message": ...} with an optional "delay" int key
#

import asyncio
import datetime
import json
from weakref import WeakSet

from aiohttp import web
from aiohttp_sse import sse_response
import aioredis


MAX_DELAY = 2 * 60  # Sane default
REDIS_PUBSUB_CHANNEL = "sse::messages"  # Duplicated in backend/jew_pizza/constants.py
DISCONNECT = object()
TEST_HTML = open("/app/test.html", "rb").read()
DEBUG = False


def debug(s):
    if DEBUG:
        print(f"{datetime.datetime.now()} - {s}")


async def publish_message_delayed(app, message, delay):
    await asyncio.sleep(delay)
    publish_message(app, message)


def publish_message(app, message):
    raw_message = json.dumps(message)
    app["last_messages"][message["type"]] = raw_message

    num_written = 0
    for num_written, queue in enumerate(app["client_queues"], 1):
        queue.put_nowait(raw_message)
    if DEBUG:  # Avoid a json.dumps() in prod
        debug(f"Sent to {num_written} subscriber(s): {json.dumps(message, indent=2)}")


def process_raw_message(app, raw_message):
    # Decode
    try:
        message = json.loads(raw_message)
    except json.JSONDecodeError:
        debug(f"Invalid message JSON: {raw_message!r}")
        return

    # Make sure it has a type
    if not isinstance(message_type := message.get("type"), str):
        debug(f"Invalid message type: {message_type!r}")
        return

    # Make sure it has a body
    if (message_body := message.get("message")) is None:
        debug(f"Invalid message body: {message_body!r}")
        return

    # Make sure it has an optional int/float delay within buonds
    delay = message.pop("delay", None)  # Remove delay
    if (delay is not None) and (not isinstance(delay, (int, float)) or delay > MAX_DELAY):
        debug(f"Invalid message delay: {delay!r}")
        return

    # Send message immediately ot delay it
    if delay is None or delay <= 0:
        publish_message(app, message)
    else:
        debug(f"Delay {message_type!r} for {delay} second(s)")
        asyncio.create_task(publish_message_delayed(app, message, delay))


async def redis_subscriber(app):
    try:
        redis = await aioredis.from_url("redis://redis")
        pubsub = redis.pubsub()
        await pubsub.subscribe(REDIS_PUBSUB_CHANNEL)

        while True:
            async for message in pubsub.listen():
                if message["type"] == "message" and message["data"]:
                    process_raw_message(app, message["data"].decode())

    except asyncio.CancelledError:
        pass


async def subscribe(request):
    request.app["client_queues"].add(queue := asyncio.Queue())
    recap = request.query.get("recap", "1") != "0"

    async with sse_response(request, headers={"Access-Control-Allow-Origin": "*"}) as resp:
        if recap:
            for message in request.app["last_messages"].values():
                await resp.send(message)
        while message := await queue.get():
            if message is DISCONNECT:
                break
            await resp.send(message)
    return resp


async def test(response):
    if DEBUG:
        return web.FileResponse("/app/test.html")
    else:
        return web.Response(body=TEST_HTML, content_type="text/html")


async def on_startup(app):
    app["client_queues"] = WeakSet()
    app["last_messages"] = {}
    app["redis_subscriber"] = asyncio.create_task(redis_subscriber(app))


async def on_shutdown(app):
    app["redis_subscriber"].cancel()
    await app["redis_subscriber"]
    for queue in app["client_queues"]:
        await queue.put(DISCONNECT)


app = web.Application()
app.router.add_route("GET", "/", subscribe)
app.router.add_route("GET", "/test", test)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    DEBUG = True
    web.run_app(app, host="0.0.0.0", port=8001)
