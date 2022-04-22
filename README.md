# [jew.pizza][jewpizza-url] Website ✡️🍕

[![][jewpizza-badge]][jewpizza-url]
[![][stack-badge]][stack-url]
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
personal website. Built using the
[CLANG! THUD! IT'S A DARN JEW'S PANDA!][stack-url] stack.


## Preface

I can't imagine _why on earth_ in a million years you'd want to run this code.
So, these instructions are mostly for me &mdash; in case of sudden amnesia or
coming back to this project after a period of neglect.


## Stack &mdash; **CLANG! THUD! IT'S A DARN JEW'S PANDA!**

It's built using the _wildly_ popular and _extremely_ common **CLANG! THUD! IT'S
A DARN JEW'S PANDA!** stack, ie,

* **C** is for [Compose][docker-compose-url], ie Docker Compose, a
    multi-container orchestration tool;
* **L** is for [Liquidsoap][liquidsoap-url], a fantastic scripting language for
    declaratively describing audio streams;
* **A** is for [Alpine Linux][alpine-linux-url], a lightweight
    [Linux][linux-url] distribution perfect for containers, based on
    [musl libc][musl-url] and [BusyBox][busybox-url];
* **N** is for [nginx][nginx-url], a web server and
    [reverse proxy][reverse-proxy-url] using the
    [jonasal/nginx-certbot][nginx-certbot-url] container as its base (for
    [HTTPS][https-url]), using [embedded Lua][nginx-lua-url];
* **G** is for [Gunicorn][gunicorn-url] to run the web app via
    [Python][python-url]'s [Web Server Gateway Interface][wsgi-url];
* **T** is for [Tailwind CSS][tailwind-url], a utility-first CSS framework;
* **H** is for [huey][huey-url], a lightweight asynchronous task queue for
    [Python][python-url];
* **U** is for [Umami][umami-url] to get insights via web analytics;
* **D** is for [Docker][docker-url] to run all this crap in containers;
* **I** for [Icecast][icecast-url], a streaming media server for listeners to
    connect (using [Karl Heyes's fork][icecast-kh-url]);
* **T** for [Twilio][twilio-url], an API to send programmable communications —
    in this case, [text messages (SMS)][sms-url];
* **S** for [S3][amazon-s3-url], ie Amazon S3 Cloud Object Storage, to store
    large audio files (I use the compatible
    [DigitalOcean Spaces][digitalocean-spaces-url]);
* **A** is for [AlpineJS][alpinejs-url], a lightweight, reactive front-end
    [JavaScript][javascript-url] framework;
* **D** is for [Django][django-url], a [Python][python-url] back-end web
    framework;
* **A** is for Actions, ie [GitHub Actions][github-actions-url], to continuously
    and automatically build, test and deploy this code;
* **R** is for [Redis][redis-url], a data store and message broker;
* **N** is for [Navigo][navigo-url] that provides a simple [SPA][spa-url]
    router;
* **J** is for [Jinja][jinja-url] templating — like [Django][django-url]'s,
    but less sucky;
* **E** is for [esbuild][esbuild-url], a fast [JavaScript][javascript-url]
    bundler;
* **W** is for [WaveSurfer.js][wavesurfer-url], a front-end audio player with
    waveform visualizations;
* **S** is for [Server-Sent Events (SSE)][sse-url], to send realtime messages to
    the browser;
* **P** is for [PostgresSQL][postgres-url], a [SQL][sql-url] database;
* **A** for [autoheal][autoheal-url], ie Docker Autoheal, a tool to monitor and
    restart unhealthy docker containers;
* **N** is for [Nchan][nchan-url], an [nginx][nginx-url] module managing
    [EventSource][eventsource-url] ([SSE][sse-url]) clients;
* **D** is for [daisyUI][daisyui-url], a lightweight UI component framework on
    top of [Tailwind CSS][tailwind-url]; and
* **A** is for [audiowaveform][audiowaveform-url], The [BBC][bbc-url]'s offline
    rendering tool for generating waveforms for [WaveSurfer.js][wavesurfer-url].

**CLANG! THUD! IT'S A DARN JEW'S PANDA!** A very well-known acronym in the
engineering world, _probably._ I definitely didn't just make this up as a joke.


## Prerequisites

Everything runs with [Docker][docker-url] and
[Docker Compose][docker-compose-url], including [nginx][nginx-url]. This can be
deployed on any [Linux][linux-url] machine.

Installing, compiling, running, and maintaining the motley crew of technologies
that make up the [**CLANG! THUD! IT'S A DARN JEW'S PANDA!**][stack-url] stack in
both prod and dev environments would be an absolute nightmare. With
[Docker][docker-url] and [Docker Compose][docker-compose-url], that can be done
in just a couple of commands. It even works with
[Docker Desktop on macOS][docker-for-mac-url]!

To install these on [Debian][debian-url]/[Ubuntu][ubuntu-url],

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
Clone, then copy and edit the `.env` file, and optionally copy over the
[Docker Compose][docker-compose-url] dev overrides.

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
127.0.0.1 radio.local.jew.pizza play.local.jew.pizza listen.local.jew.pizza
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
system with randomness to speed up SSL certificate generation. On
[Debian][debian-url]/[Ubuntu][ubuntu-url], it can be installed via the
following,

```bash
sudo apt-get install haveged
```


### Production Mode (`DEBUG=0`)

Pull (or build) containers and run `docker compose up` in daemon mode (`-d`).
Set all appropriate variables in the `.env` file, making note to properly
configure the following,

* An SMTP server &mdash; works with [SendGrid][sendgrid-url]
* [Twilio][twilio-url] account SID and auth token
* [DigitalOcean][digitalocean-url] [Spaces][digitalocean-spaces-url], along with
    an API key, taking note to run the domain name's DNS off of
    [DigitalOcean][digitalocean-url]. This is necessary for wildcard certificates
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


## Automatic Deploying

You can automatically deploy the code one of two ways via
[GitHub Actions][github-actions-url],

1. Include the string `[deploy]` (or `🚀`) in your HEAD commit message and push;
    or
2. Trigger the [Deploy Workflow][deploy-workflow-url] manually.


## License

This project is licensed under the [MIT License][mit-license-url] &mdash; see
the [LICENSE][license-url] file for details.

## Final Note

**_...and remember kids, have fun!_**

[app-container-badge]: https://img.shields.io/docker/image-size/jewpizza/app/latest?label=app&logo=docker&logoColor=ffffff&style=flat-square
[app-container-url]: https://hub.docker.com/r/jewdotpizza/app
[icecast-container-badge]: https://img.shields.io/docker/image-size/jewdotpizza/icecast/latest?label=icecast&logo=docker&logoColor=ffffff&style=flat-square
[icecast-container-url]: https://hub.docker.com/r/jewdotpizza/icecast
[nginx-container-badge]: https://img.shields.io/docker/image-size/jewdotpizza/nginx/latest?label=nginx&logo=docker&logoColor=ffffff&style=flat-square
[nginx-container-url]: https://hub.docker.com/r/jewdotpizza/nginx
[radio-container-badge]: https://img.shields.io/docker/image-size/jewdotpizza/radio/latest?label=radio&logo=docker&logoColor=ffffff&style=flat-square
[radio-container-url]: https://hub.docker.com/r/jewdotpizza/radio

[build-badge]: https://img.shields.io/github/workflow/status/dtcooper/jewpizza/Build%20and%20Deploy?label=build%20%26%20deploy&logo=github&style=flat-square
[build-url]: https://github.com/dtcooper/jewpizza/actions/workflows/docker-build.yml
[hurd-badge]: https://img.shields.io/badge/GNU%20hurd-incompatable-critical?logo=gnu&logoColor=white&style=flat-square
[hurd-url]: https://github.com/dtcooper/jewpizza/issues/1
[jewpizza-badge]: https://img.shields.io/badge/website-jew.pizza-informational?style=flat-square
[jewpizza-url]: https://jew.pizza/
[stack-badge]: https://img.shields.io/badge/stack-CLANG%21%20THUD%21%20IT%27S%20A%20DARN%20JEW%27S%20PANDA%21-informational?style=flat-square
[stack-url]: https://github.com/dtcooper/jewpizza#stack--clang-thud-its-a-darn-jews-panda
[last-commit-badge]: https://img.shields.io/github/last-commit/dtcooper/jewpizza/main?logo=github&style=flat-square
[last-commit-url]: https://github.com/dtcooper/jewpizza/commits/main
[license-badge]: https://img.shields.io/github/license/dtcooper/jewpizza?style=flat-square&color=success
[license-url]: https://github.com/dtcooper/jewpizza/blob/main/LICENSE
[stars-badge]: https://img.shields.io/github/stars/dtcooper/jewpizza?logo=github&style=flat-square
[stars-url]: https://github.com/dtcooper/jewpizza/stargazers

[alpine-linux-url]: https://alpinelinux.org/
[alpinejs-url]: https://alpinejs.dev/
[amazon-s3-url]: https://aws.amazon.com/s3/
[audiowaveform-url]: https://github.com/bbc/audiowaveform
[autoheal-url]: https://github.com/willfarrell/docker-autoheal
[bbc-url]: https://www.bbc.com/
[busybox-url]: https://busybox.net/
[certbot-url]: https://certbot.eff.org/
[daisyui-url]: https://daisyui.com/
[debian-url]: https://www.debian.org/
[digitalocean-spaces-url]: https://www.digitalocean.com/products/spaces
[digitalocean-url]: https://www.digitalocean.com/
[django-url]: https://www.djangoproject.com/
[docker-compose-url]: https://docs.docker.com/compose/
[docker-for-mac-url]: https://docs.docker.com/desktop/mac/install/
[docker-url]: https://www.docker.com/
[deploy-workflow-url]: https://github.com/dtcooper/jewpizza/actions/workflows/deploy.yml
[esbuild-url]: https://esbuild.github.io/
[eventsource-url]: https://developer.mozilla.org/en-US/docs/Web/API/EventSource
[github-actions-url]: https://docs.github.com/en/actions
[gunicorn-url]: https://gunicorn.org/
[haveged-url]: https://www.issihosts.com/haveged/
[https-url]: https://en.wikipedia.org/wiki/HTTPS
[huey-url]: https://huey.readthedocs.io/
[icecast-kh-url]: https://github.com/karlheyes/icecast-kh
[icecast-url]: https://icecast.org/
[javascript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[jinja-url]: https://jinja.palletsprojects.com/
[letsencrypt-url]: https://letsencrypt.org/
[linux-url]: https://www.kernel.org/
[liquidsoap-url]: https://www.liquidsoap.info/
[mit-license-url]: https://en.wikipedia.org/wiki/MIT_License
[musl-url]: https://musl.libc.org/
[navigo-url]: https://github.com/krasimir/navigo
[nchan-url]: https://nchan.io/
[nginx-certbot-url]: https://github.com/JonasAlfredsson/docker-nginx-certbot/
[nginx-lua-url]: https://github.com/openresty/lua-nginx-module
[nginx-url]: https://www.nginx.com/
[postgres-url]: https://www.postgresql.org/
[python-url]: https://www.python.org/
[redis-url]: https://redis.io/
[reverse-proxy-url]: https://en.wikipedia.org/wiki/Reverse_proxy
[sendgrid-url]: https://sendgrid.com/
[sms-url]: https://en.wikipedia.org/wiki/SMS
[spa-url]: https://en.wikipedia.org/wiki/Single-page_application
[sql-url]: https://en.wikipedia.org/wiki/SQL
[sse-url]: https://en.wikipedia.org/wiki/Server-sent_events
[tailwind-url]: https://tailwindcss.com/
[twilio-url]: https://www.twilio.com/
[ubuntu-url]: https://ubuntu.com/
[umami-url]: https://umami.is/
[wavesurfer-url]: https://wavesurfer-js.org/
[web-app-url]: https://en.wikipedia.org/wiki/Web_application
[wsgi-url]: https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface
