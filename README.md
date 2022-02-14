# [jew.pizza](https://jew.pizza) Website ✡️🍕

[![GNU Hurd Incompatible](https://img.shields.io/badge/GNU%20Hurd-incompatible-red?logo=gnu&style=for-the-badge)](https://github.com/dtcooper/jewpizza/issues/1)

Here's the code for the website that powers [jew.pizza](https://jew.pizza), my
personal website.


## Preface

I can't imagine in a million years _why on earth_ you'd want to run this code.
So, these instructions are mostly for me &mdash; in case of sudden amnesia or
coming back to this project after a year or so of neglect.


## Stack &mdash; **_DJ DRENCH AND SPLINT_**

It's built using the _wildly_ popular and _extremely_ common
**_DJ DRENCH AND SPLINT_** stack, ie,

* [**D**jango](https://www.djangoproject.com/), a back-end web framework;
* [**J**inja](https://jinja.palletsprojects.com/) for templating. Like django,
    but less sucky;
* [**D**ocker](https://www.docker.com/) to run all this crap in containers;
* [**R**edis](https://redis.io/), a data store and message broker;
* [**e**sbuild](https://esbuild.github.io/), a fast JavaScript bundler;
* [**N**avigo](https://github.com/krasimir/navigo) for a simple
    [SPA](https://en.wikipedia.org/wiki/Single-page_application) router;
* [**C**ompose](https://docs.docker.com/compose/), ie Docker Compose, for
    multi-container orchestration;
* [**h**uey](https://huey.readthedocs.io/), a lightweight asynchronous task
    queue for Python;
* [**A**lpineJS](https://alpinejs.dev/), a lightweight, reactive front-end
    framework;
* [**n**ginx](https://www.nginx.com/) as a web server and reverse proxy with
    [jonasal/nginx-certbot](https://github.com/JonasAlfredsson/docker-nginx-certbot/)
    container as its base for [HTTPS](https://en.wikipedia.org/wiki/HTTPS);
* [**d**aisyUI](https://daisyui.com/) as lightweight UI component framework on
    top of Tailwind CSS;
* [**S**erver-Sent Events (SSE)](https://en.wikipedia.org/wiki/Server-sent_events),
    to send realtime messages to the browser (using the nginx module
    [Nchan](https://nchan.io/) as described below);
* [**P**ostgresSQL](https://www.postgresql.org/), a database;
* [**L**iquidsoap](https://www.liquidsoap.info/), a fantastic scripting language
    for describing audio streams;
* [**I**cecast](https://icecast.org/), a streaming media server for listeners to
    connect (Karl Heyes's [fork](https://github.com/karlheyes/icecast-kh));
* [**N**chan](https://nchan.io/), an nginx module managing EventSource (SSE)
    clients; and
* [**T**ailwind CSS](https://tailwindcss.com/), a utility-first CSS framework.

**_DJ DRENCH AND SPLINT_**. A very well-known acronym in the engineering world,
_probably._ I definitely didn't just make this up as a joke.


## Prerequisites

Everything runs with [Docker](https://www.docker.com/) and
[Docker Compose](https://docs.docker.com/compose/), including
[nginx](https://www.nginx.com/). This can be deployed on any Linux machine.

To install on Debian/Ubuntu,

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Install latest Compose
sudo mkdir -p /usr/local/lib/docker/cli-plugins/
sudo curl -fsSL -o /usr/local/lib/docker/cli-plugins/docker-compose \
    "$(curl -fsSL https://api.github.com/repos/docker/compose/releases/latest | grep browser_download_url | cut -d '"' -f 4 | grep -i "$(uname -s)-$(arch)$")"
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
```


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
root certificate located at `<project-dir>/local-certificate-authority/caCert.pem`.
It expires every 30 days.


## Running

### Development Mode (`DEBUG=1` with `docker-compose.dev.yml` symlinked)

Build and start containers,

```bash
docker compose build
docker compose up
```

The development `app` server will run at <http://localhost:8000/>, or if you've
set a `DOMAIN_NAME` and your `/etc/hosts` to work properly with it, navigate to
that. For example <https://local.jew.pizza/>. You'll need to install the phony
certificate authority's root certificate (see above).


#### Miscellaneous Development Operations

```bash
# Django management command
docker compose run --rm app ./manage.py

# Run shell in app container (make shell)
docker compose run --rm app bash

# Pre commit checks + reformatting (not required)
make pre-commit
```

#### Faster Start Time (SSL Certificate Generation)

The entropy daemon [haveged](https://www.issihosts.com/haveged/) is a
nice-to-have to provide your system with randomness to speed up SSL certificate
generation. On Debian/Ubuntu, it can be installed via the following,

```bash
sudo apt-get install haveged
```


### Production Mode (`DEBUG=0`)

Pull (or build) containers and run `docker compose up` in daemon mode (`-d`).
Set all appropriate variables in the `.env` file, making note to properly
configure the following,

* An SMTP server &mdash; works with [SendGrid](https://sendgrid.com/)
* Twilio account SID and auth token
* DigitalOcean Spaces, along with an API key, taking note to run the domain
    name's DNS off of DigitalOcean. This is necessary for wildcard certificates
    from [Certbot](https://certbot.eff.org/)/[Lets Encrypt](https://letsencrypt.org/).

```bash
docker compose pull
# Or optionally build the containers via: docker compose build
docker compose up -d
```

#### Change Passwords

Make sure to change these insecure passwords not sent in the `.env` file,

* Django: `dave:cooper`
* Umami: `dave:cooper`


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
