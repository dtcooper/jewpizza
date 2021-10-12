# jew.pizza Website ✡️🍕

Here's the code for the website that powers [`jew.pizza`](https://jew.pizza), my
personal website.


## Preface

I can't imagine in a million years _why on earth_ you'd want to run this code.
So, these instructions are mostly for me &mdash; in case of sudden amnesia or
coming back to this project after a year or so of neglect.

You might also use this code as an example of a
[docker compose](https://docs.docker.com/compose/) project running
[Poetry](https://python-poetry.org/) and [Django](https://www.djangoproject.com/),
plus a _very_ minimal frontend build system for [Tailwind CSS](https://tailwindcss.com/)
and [daisyUI](https://daisyui.com/). It uses front-end packages managed by
[npm](https://www.npmjs.com/)/[django-npm](https://github.com/kevin1024/django-npm).
Most notably, [Alpine.js](https://alpinejs.dev/) is used for a reactive front-end
framework and a poor man's [SPA](https://en.wikipedia.org/wiki/Single-page_application)
with [Navigo](https://github.com/krasimir/navigo). The need for an SPA is due to
the 24/7 audio player embedded in the footer of the site.

If I ever run out of money and do tech consulting, I might just derive a starting
template from this repo.


## Initial Setup

Clone, then copy and edit the `.env` file, and optionally copy over the docker
compose dev overrides.

```bash
git clone https://github.com/dtcooper/jewpizza.git

# Edit me, you'll probably want to be in development mode (DEBUG=1)
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

You'll also have to reverse proxy into the [umami](https://umami.is/) analytics,
or set `UMAMI_BIND_ADDR=0.0.0.0:3000`.

A sample nginx config might be,

```nginx
# Main site
server {
    listen 80;
    server_name sample.domain.com;

    location /static {
        alias /home/user/jew.pizza/serve/static;
    }

    location /media {
        alias /home/user/jew.pizza/serve/media;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}

# Umami analytics
server {
    listen 80;
    server_name umami.domain.com;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:3000;
    }
}
```

If you want to **TEST** with `DEBUG=0` without running nginx and have Gunicorn
serve your static assets using [Whitenoise](http://whitenoise.evans.io/en/stable/),
set `SERVE_ASSETS_FROM_DJANGO=1` in your `.env` file,


#### Change Passwords

Change passwords,
* Django: `dave:cooper`
* Umami: `dave:cooper`


#### Icecast 2 in Production

TODO


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
