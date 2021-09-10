# jew.pizza Website

Here's the code for the website that powers [`jew.pizza`](https://jew.pizza), my
personal website.


## Initial Setup

Create an edit `.env`, and optionally copy over docker-compose dev overrides.

```bash
# Edit me, you'll probably want to be in development mode (DEBUG=1)
cp .env.sample .env

# For development only, ie if in development mode
ln -s docker-compose.dev.yml docker-compose.override.yml
```


## Running

### Development Mode (`DEBUG=1`)

Build and start containers,

```bash
docker-compose build
docker-compose up
```

The development server will run at <http://localhost:8000/>.


#### Miscellaneous Development Operations

```bash
# Django management command
docker-compose-run --rm app ./manage.py

# Run shell in app container (make shell)
docker-compose-run --rm app bash

# Rebuild CSS + JS - should happen automatically (make frontend-build)
docker-compose run --rm frontend-dev npm run build

# Pre commit checks (not required)
make pre-commit
```


### Production Mode (`DEBUG=0`)

Build containers and start in daemon mode.

```bash
docker-compose build
docker-compose up -d
```

NOTE: [Gunicorn](https://gunicorn.org/) will listen on `127.0.0.1:${LISTEN_PORT}`
(default `8000` in your `.env` file). You will have to reverse proxy into the service
using `nginx` (or similar) and serve the static and media assets (deployed to the
`serve/static/` and `serve/media/` folders, respectively).

A sample nginx config might be,

```nginx
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
```

Or if you want to **TEST** with `DEBUG=0` without running nginx and have Gunicorn
serve your static assets using [Whitenoise](http://whitenoise.evans.io/en/stable/),
add the following to your `.env` file,

```
SERVE_ASSETS_FROM_DJANGO=1
```
