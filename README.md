# [jew.pizza][jewpizza-url] Website ✡️🍕

[![][jewpizza-badge]][jewpizza-url]
[![][license-badge]][license-url]
[![][hurd-badge]][hurd-url]

[![][build-badge]][build-url]
[![][last-commit-badge]][last-commit-url]
[![][stars-badge]][stars-url]

[![][app-container-badge]][app-container-url]
[![][radio-container-badge]][radio-container-url]
[![][nginx-container-badge]][nginx-container-url]
[![][icecast-container-badge]][icecast-container-url]

Here's the code for the website that powers [jew.pizza][jewpizza-url], my
personal website.


## Preface

I can't imagine in a million years _why on earth_ you'd want to run this code.
So, these instructions are mostly for me &mdash; in case of sudden amnesia or
coming back to this project after a year or so of neglect.


## Stack &mdash; **_DJ DRENCH AND SPLINT_**

It's built using the _wildly_ popular and _extremely_ common
**_DJ DRENCH AND SPLINT_** stack, ie,

* [**D**jango][django-url], a back-end web framework;
* [**J**inja][jinja-url] for templating. Like Django's, but less sucky;
* [**D**ocker][docker-url] to run all this crap in containers;
* [**R**edis][redis-url], a data store and message broker;
* [**e**sbuild][esbuild-url], a fast JavaScript bundler;
* [**N**avigo][navigo-url] for a simple [SPA][spa-url] router;
* [**C**ompose][docker-compose-url], ie Docker Compose, for multi-container
    orchestration;
* [**h**uey][huey-url], a lightweight asynchronous task queue for Python;
* [**A**lpineJS][alpinejs-url], a lightweight, reactive front-end framework;
* [**n**ginx][nginx-url] as a web server and reverse proxy using the
    [jonasal/nginx-certbot][nginx-certbot-url] container as its base (for
    [HTTPS][https-url]);
* [**d**aisyUI][daisyui-url], a lightweight UI component framework on
    top of Tailwind CSS;
* [**S**erver-Sent Events (SSE)][sse-url], to send realtime messages to the
    browser;
* [**P**ostgresSQL][postgres-url], a SQL database;
* [**L**iquidsoap][liquidsoap-url], a fantastic scripting language for
    declaratively describing audio streams;
* [**I**cecast][icecast-url], a streaming media server for listeners to connect
    (using [Karl Heyes's fork][icecast-kh-url]);
* [**N**chan][nchan-url], an nginx module managing EventSource ([SSE][sse-url])
    clients; and
* [**T**ailwind CSS][tailwind-url], a utility-first CSS framework.

**_DJ DRENCH AND SPLINT_**. A very well-known acronym in the engineering world,
_probably._ I definitely didn't just make this up as a joke.


## Prerequisites

Everything runs with [Docker][docker-url] and
[Docker Compose][docker-compose-url], including [nginx][nginx-url]. This can be
deployed on any Linux machine.

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
want to properly point your system's DNS that way. For example, add the following
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
make build
docker compose up
```

The development `app` server will run at <http://localhost:8000/>, or if you've
set a `DOMAIN_NAME` and your `/etc/hosts` to work properly with it, navigate to
that. For example, <https://local.jew.pizza/>. You'll need to install the phony
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

The entropy daemon [haveged][haveged-url] is a nice-to-have to provide your
system with randomness to speed up SSL certificate generation. On Debian/Ubuntu,
it can be installed via the following,

```bash
sudo apt-get install haveged
```


### Production Mode (`DEBUG=0`)

Pull (or build) containers and run `docker compose up` in daemon mode (`-d`).
Set all appropriate variables in the `.env` file, making note to properly
configure the following,

* An SMTP server &mdash; works with [SendGrid][sendgrid-url]
* [Twilio][twilio-url] account SID and auth token
* DigitalOcean Spaces, along with an API key, taking note to run the domain
    name's DNS off of DigitalOcean. This is necessary for wildcard certificates
    from [Certbot][certbot-url]/[Lets Encrypt][letsencrypt-url].

```bash
docker compose pull
# Or optionally build the containers via: make build
docker compose up -d
```

#### Change Passwords

Make sure to change these insecure passwords not sent in the `.env` file,

* Django: `dave:cooper`
* Umami: `dave:cooper`


## License

This project is licensed under the MIT License - see the [LICENSE][license-url] file
for details.


[app-container-badge]: https://img.shields.io/docker/image-size/dtcooper/jewpizza-app/latest?label=app&logo=docker&logoColor=ffffff&style=flat-square
[app-container-url]: https://hub.docker.com/r/dtcooper/jewpizza-app
[icecast-container-badge]: https://img.shields.io/docker/image-size/dtcooper/jewpizza-icecast/latest?label=icecast&logo=docker&logoColor=ffffff&style=flat-square
[icecast-container-url]: https://hub.docker.com/r/dtcooper/jewpizza-icecast
[nginx-container-badge]: https://img.shields.io/docker/image-size/dtcooper/jewpizza-nginx/latest?label=nginx&logo=docker&logoColor=ffffff&style=flat-square
[nginx-container-url]: https://hub.docker.com/r/dtcooper/jewpizza-nginx
[radio-container-badge]: https://img.shields.io/docker/image-size/dtcooper/jewpizza-radio/latest?label=radio&logo=docker&logoColor=ffffff&style=flat-square
[radio-container-url]: https://hub.docker.com/r/dtcooper/jewpizza-radio

[jewpizza-badge]: https://img.shields.io/badge/jew.pizza-website-informational?style=flat-square
[jewpizza-url]: https://jew.pizza/
[build-badge]: https://img.shields.io/github/workflow/status/dtcooper/jewpizza/Build%20and%20Deploy?label=build%20%26%20deploy&logo=github&style=flat-square
[build-url]: https://github.com/dtcooper/jewpizza/actions/workflows/docker-build.yml
[hurd-badge]: https://img.shields.io/badge/GNU%20hurd-incompatable-critical?logo=gnu&logoColor=white&style=flat-square
[hurd-url]: https://github.com/dtcooper/jewpizza/issues/1
[last-commit-badge]: https://img.shields.io/github/last-commit/dtcooper/jewpizza/main?logo=github&style=flat-square
[last-commit-url]: https://github.com/dtcooper/jewpizza/commits/main
[license-badge]: https://img.shields.io/github/license/dtcooper/jewpizza?style=flat-square&color=success
[license-url]: https://github.com/dtcooper/jewpizza/blob/main/LICENSE
[stars-badge]: https://img.shields.io/github/stars/dtcooper/jewpizza?logo=github&style=flat-square
[stars-url]: https://github.com/dtcooper/jewpizza/stargazers

[alpinejs-url]: https://alpinejs.dev/
[certbot-url]: https://certbot.eff.org/
[daisyui-url]: https://daisyui.com/
[django-url]: https://www.djangoproject.com/
[docker-compose-url]: https://docs.docker.com/compose/
[docker-url]: https://www.docker.com/
[esbuild-url]: https://esbuild.github.io/
[haveged-url]: https://www.issihosts.com/haveged/
[https-url]: https://en.wikipedia.org/wiki/HTTPS
[huey-url]: https://huey.readthedocs.io/
[icecast-kh-url]: https://github.com/karlheyes/icecast-kh
[icecast-url]: https://icecast.org/
[jinja-url]: https://jinja.palletsprojects.com/
[letsencrypt-url]: https://letsencrypt.org/
[liquidsoap-url]: https://www.liquidsoap.info/
[navigo-url]: https://github.com/krasimir/navigo
[nchan-url]: https://nchan.io/
[nginx-certbot-url]: https://github.com/JonasAlfredsson/docker-nginx-certbot/
[nginx-url]: https://www.nginx.com/
[postgres-url]: https://www.postgresql.org/
[redis-url]: https://redis.io/
[sendgrid-url]: https://sendgrid.com/
[spa-url]: https://en.wikipedia.org/wiki/Single-page_application
[sse-url]: https://en.wikipedia.org/wiki/Server-sent_events
[tailwind-url]: https://tailwindcss.com/
[twilio-url]: https://www.twilio.com/
