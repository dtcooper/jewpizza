#
# Dead simple server-sent event (SSE) server. No authentication, no frills.
# Server is protected by nginx's "internal" flag and authenticated by Django
# and an X-Accel-Redirect
#
# GET:/ -- subscribes to messages
# GET:/test -- test page
#
# Publish valid JSON strings to redis channel sse::messages
# They must have the keys {"type": "<type>", "message": ...} with an optional "delay" int/float key
#

import asyncio
import datetime
import json
from weakref import WeakSet

from aiohttp import web
from aiohttp_sse import sse_response
import aioredis
from schema import And, Optional, Or, Schema, SchemaError


MAX_DELAY = 2 * 60  # Sane default
REDIS_PUBSUB_CHANNEL = "sse::messages"  # Duplicated in backend/jew_pizza/constants.py
REDIS_URL = "redis://redis"
DISCONNECT = object()
DEBUG = False


message_schema = Schema(
    {
        Optional("delay", default=None): And(Or(int, float, None), lambda d: d is None or 0 <= d <= MAX_DELAY),
        "type": str,
        "message": dict,
    }
)


def debug(s):
    if DEBUG:
        print(f"{datetime.datetime.now()} - {s}")


async def process_delayed_message(app, message, delay):
    await asyncio.sleep(delay)
    process_message(app, message)


def process_message(app, message):
    if isinstance(message, (bytes, str)):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            debug(f"Invalid message JSON: {message.decode()!r}")
            return

        try:
            message = message_schema.validate(message)
        except SchemaError as e:
            debug(f"Message schema failed validation - {e}: {message!r}")
            return

    delay = message.pop("delay", None)  # remove delay
    if delay is not None and delay >= 0:
        debug(f"Delaying message {message['type']!r} for {delay} second(s)")
        asyncio.create_task(process_delayed_message(app, message, delay))
    else:
        raw_message = app["last_messages"][message["type"]] = json.dumps(message)

        num_written = 0
        for num_written, queue in enumerate(app["client_queues"], 1):
            queue.put_nowait(raw_message)
        if DEBUG:  # Avoid a json.dumps() in prod
            debug(f"Sent to {num_written} subscriber(s): {json.dumps(message, indent=2)}")


async def redis_subscriber(app):
    try:
        redis = await aioredis.from_url(REDIS_URL)
        pubsub = redis.pubsub()
        await pubsub.subscribe(REDIS_PUBSUB_CHANNEL)

        while True:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    process_message(app, message["data"])

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


async def on_startup(app):
    app["client_queues"] = WeakSet()
    app["last_messages"] = {}
    app["redis_subscriber"] = asyncio.create_task(redis_subscriber(app))


async def on_shutdown(app):
    app["redis_subscriber"].cancel()
    await app["redis_subscriber"]
    debug(f"Exiting. Disconnecting {len(app['client_queues'])} client(s).")
    for queue in app["client_queues"]:
        await queue.put(DISCONNECT)


app = web.Application()
app.router.add_route("GET", "/", subscribe)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    DEBUG = True

    async def test(response):
        return web.FileResponse("/app/test.html")

    app.router.add_route("GET", "/test", test)
    web.run_app(app, host="0.0.0.0", port=8001)
