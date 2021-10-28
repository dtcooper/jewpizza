# [jew.pizza](https://jew.pizza) Website ✡️ ⚪ 🍕

Here's the code for the website that powers [jew.pizza](https://jew.pizza), my
personal website.


## Preface

I can't imagine in a million years _why on earth_ you'd want to run this code.
So, these instructions are mostly for me &mdash; in case of sudden amnesia or
coming back to this project after a year or so of neglect.


## Stack &mdash; **DR. DJ PLASTIC HAND**

It's built using the _wildly_ popular, _extremely_ common **DR. DJ PLASTIC HAND**
stack, ie,

* [**D**jango](https://www.djangoproject.com/), a back-end web framework;
* [**R**edis](https://redis.io/), a data store and message broker;
* [**D**ocker](https://www.docker.com/) to run all this crap in containers;
* [**J**inja](https://jinja.palletsprojects.com/) for templating. Like django,
    but less sucky;
* [**P**ostgresSQL](https://www.postgresql.org/), a database;
* [**L**iquidsoap](https://www.liquidsoap.info/), a fantastic scripting language
    for describing audio streams;
* [**A**lpineJS](https://alpinejs.dev/), a lightweight, reactive front-end
    framework;
* [**S**erver-Sent Events (SSE)](https://en.wikipedia.org/wiki/Server-sent_events),
    to send realtime messages to the browser, using
    [aoihttp-sse](https://github.com/aio-libs/aiohttp-sse);
* [**T**ailwind CSS](https://tailwindcss.com/), a utility-first CSS framework;
* [**I**cecast](https://icecast.org/), a streaming media server for listeners to
    connect;
* [**C**ompose](https://docs.docker.com/compose/), ie Docker Compose, for
    multi-container orchestration;
* [**h**uey](https://huey.readthedocs.io/), a lightweight asynchronous task
    queue for Python;
* [**a**iohttp](https://docs.aiohttp.org/) for the SSE service. Django's bad at
    persistent connections and aiohttp isn't;
* [**N**avigo](https://github.com/krasimir/navigo) for a simple
    [SPA](https://en.wikipedia.org/wiki/Single-page_application) router; and
* [**d**aisyUI](https://daisyui.com/) as lightweight UI component framework on
    top of Tailwind CSS.

**DR. DJ PLASTIC HAND**. A very well-known acronym in the engineering world, _probably._


## Initial Setup
Clone, then copy and edit the `.env` file, and optionally copy over the docker
compose dev overrides.

```bash
git clone https://github.com/dtcooper/jewpizza.git

# Edit me, make sure you set SECRET_KEY!
cp .env.sample .env

# Needed for development only (when DEBUG=1)
ln -s docker-compose.dev.yml docker-compose.override.yml
```


## Running

### Development Mode (`DEBUG=1`)

Build and start containers,

```bash
docker compose build
docker compose up
```

The development server will run at <http://localhost:8000/>. To make it publicly
accessible, set `BIND_ADDR=0.0.0.0:8000` in `.env`.


#### Miscellaneous Development Operations

```bash
# Django management command
docker compose run --rm app ./manage.py

# Run shell in app container (make shell)
docker compose run --rm app bash

# Pre commit checks + reformatting (not required)
make pre-commit
```


### Production Mode (`DEBUG=0`)

Build containers and start in daemon mode.

```bash
docker compose build
docker compose up -d
```

NOTE: [Gunicorn](https://gunicorn.org/) will listen on `127.0.0.1:8000`
(default of `BIND_ADDR` in your `.env` file). You will have to reverse proxy
into the service using `nginx` (or similar) and serve the static and media assets
(deployed to the `serve/static/` and `serve/media/` folders, respectively).

You'll also have to reverse proxy into the SSE service, [umami](https://umami.is/)
analytics, and [Dozzle](https://dozzle.dev/) logs containers on ports `8001`,
`3000`, and `8888`, respectively.

A sample nginx config might be,

```nginx
# Main site
server {
    listen 443 ssl http2;
    server_name jew.pizza;
    include ssl_params;

    location /static {
        alias /home/username/jew.pizza/serve/static;
    }

    location /media {
        alias /home/username/jew.pizza/serve/media;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}

# SSE service
server {
    listen 443 ssl http2;
    server_name sse.jew.pizza;
    include ssl_params;

    location / {
        include proxy_params;
        proxy_buffering off;
        proxy_cache off;
        proxy_pass http://127.0.0.1:8001;
    }
}

# Umami analytics
server {
    listen 443 ssl http2;
    server_name umami.jew.pizza;
    include ssl_params;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:3000;
    }
}

# Dozzle logs
server {
    listen 443 ssl http2;
    server_name logs.jew.pizza;
    include ssl_params;

    auth_basic "jew.pizza Logs";
    # Generate via: htpasswd -Bc /path.to/htpaswd username
    auth_basic_user_file /home/username/config/htpasswd;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8888;
    }

    location /api {
        include proxy_params;
        proxy_buffering off;
        proxy_cache off;
        proxy_pass http://127.0.0.1:8888;
    }
}
```

To <ins>test</ins> (and _only_ test) with `DEBUG=0` without running nginx and
have Gunicorn serve static assets using [Whitenoise](http://whitenoise.evans.io/en/stable/),
set `SERVE_ASSETS_FROM_DJANGO=1` in the `.env` file,


#### Change Passwords

Change passwords,

* Django: `dave:cooper`
* Umami: `dave:cooper`


#### Icecast 2 in Production

TODO


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
