# [jew.pizza](https://jew.pizza) Website ✡️🍕

[![GNU Hurd Incompatible](https://img.shields.io/badge/GNU%20Hurd-incompatible-red?logo=gnu&style=for-the-badge)](https://github.com/dtcooper/jewpizza/issues/1)

Here's the code for the website that powers [jew.pizza](https://jew.pizza), my
personal website.


## Preface

I can't imagine in a million years _why on earth_ you'd want to run this code.
So, these instructions are mostly for me &mdash; in case of sudden amnesia or
coming back to this project after a year or so of neglect.


## Stack &mdash; **_DR. DJ PLACENTA HINDS_**

It's built using the _wildly_ popular and _extremely_ common
**_DR. DJ PLACENTA HINDS_** stack, ie,

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
* [**C**ompose](https://docs.docker.com/compose/), ie Docker Compose, for
    multi-container orchestration;
* [**e**sbuild](https://esbuild.github.io/), a fast JavaScript bundler;
* [**N**avigo](https://github.com/krasimir/navigo) for a simple
    [SPA](https://en.wikipedia.org/wiki/Single-page_application) router;
* [**T**ailwind CSS](https://tailwindcss.com/), a utility-first CSS framework;
* [**a**iohttp](https://docs.aiohttp.org/) for the SSE service. Django's bad at
    persistent connections and aiohttp isn't;
* [**h**uey](https://huey.readthedocs.io/), a lightweight asynchronous task
    queue for Python;
* [**I**cecast](https://icecast.org/), a streaming media server for listeners to
    connect;
* [**n**ginx](https://www.nginx.com/) as a web server and reverse proxy with
    [jonasal/nginx-certbot](https://github.com/JonasAlfredsson/docker-nginx-certbot/)
    container as its base for [HTTPS](https://en.wikipedia.org/wiki/HTTPS);
* [**d**aisyUI](https://daisyui.com/) as lightweight UI component framework on
    top of Tailwind CSS; and
* [**S**erver-Sent Events (SSE)](https://en.wikipedia.org/wiki/Server-sent_events),
    to send realtime messages to the browser (using
    [aoihttp-sse](https://github.com/aio-libs/aiohttp-sse)).


**_DR. DJ PLACENTA HINDS_**. A very well-known acronym in the engineering world,
_probably._


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

Assuming you set `DOMAIN_NAME=local.jew.pizza` for local development, you'll
want to properly point your system's DNS that way, for example add the following
to `/etc/hosts`.

```
# jew.pizza local development
127.0.0.1 local.jew.pizza
127.0.0.1 analytics.local.jew.pizza umami.local.jew.pizza
127.0.0.1 etc.local.jew.pizza
127.0.0.1 priv.local.jew.pizza
127.0.0.1 radio.local.jew.pizza
127.0.0.1 www.local.jew.pizza
```

If you set `NGINX_USE_LOCAL_CERTIFICATE_AUTHORITY=1` (and you **should** for
local development), you'll want to install the phony certificate authority's
root certificate located at `local-certificate-authority/caCert.pem`. It expires
every 30 days.


## Running

### Development Mode (`DEBUG=1` with `docker-compose.dev.yml` symlinked)

Build and start containers,

```bash
docker compose build
docker compose up
```

The development server will run at <http://localhost:8000/>.


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

Build containers and start in daemon mode. Set all appropriate variables in the
`.env` file, making note to properly configure the following,

* An SMTP server &mdash; works with [SendGrid](https://sendgrid.com/)
* Twilio account SID and auth token
* DigitalOcean Spaces, along with an API key, taking note to run the domain
    name's DNS off of DigitalOcean

```bash
docker compose pull
# Or optionally build the containers via: docker compose build
docker compose up -d
```

#### Change Passwords

Change passwords,

* Django: `dave:cooper`
* Umami: `dave:cooper`


#### Icecast 2 in Production

TODO


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
