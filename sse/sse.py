#!/usr/bin/env python

#
# Dead simple server-sent event (SSE) server. No authentication, no frills.
# Server is protected by nginx's "internal" flag and authenticated by Django
# and an X-Accel-Redirect
#
# GET:/ -- subscribes to messages
# GET:/test -- test page
#
# Publish valid JSON strings to redis channel sse::messages
#

import asyncio
from weakref import WeakSet

from aiohttp import web
from aiohttp_sse import sse_response
import aioredis


REDIS_PUBSUB_CHANNEL = "sse::messages"
DISCONNECT = object()
TEST_HTML = open("/app/test.html", "rb").read()


async def redis_subscriber(app):
    try:
        redis = await aioredis.from_url("redis://redis")
        pubsub = redis.pubsub()
        await pubsub.subscribe(REDIS_PUBSUB_CHANNEL)

        while True:
            async for message in pubsub.listen():
                if message["type"] == "message" and message["data"]:
                    data = app["messages"]["last"] = message["data"].decode()

                    num_written = 0
                    for num_written, queue in enumerate(app["messages"]["queues"], 1):
                        queue.put_nowait(data)
                    queue = None  # Make sure WeakSet looses a reference

                    if app["DEBUG"]:
                        print(f"Sent message to {num_written} subscribers: {data}")

    except asyncio.CancelledError:
        pass


async def subscribe(request):
    request.app["messages"]["queues"].add(queue := asyncio.Queue())

    async with sse_response(request) as resp:
        await resp.send(request.app["messages"]["last"])
        while message := await queue.get():
            if message is DISCONNECT:
                break
            await resp.send(message)
    return resp


async def test(response):
    if response.app["DEBUG"]:
        return web.FileResponse("/app/test.html")
    else:
        return web.Response(body=TEST_HTML, content_type="text/html")


async def on_startup(app):
    app["messages"] = {"queues": WeakSet(), "last": "{}"}
    app["redis_subscriber"] = asyncio.create_task(redis_subscriber(app))


async def on_shutdown(app):
    app["redis_subscriber"].cancel()
    await app["redis_subscriber"]
    for queue in app["messages"]["queues"]:
        await queue.put(DISCONNECT)


app = web.Application()
app.router.add_route("GET", "/", subscribe)
app.router.add_route("GET", "/test", test)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
app["DEBUG"] = False

if __name__ == "__main__":
    app["DEBUG"] = True
    web.run_app(app, host="0.0.0.0", port=8001)
