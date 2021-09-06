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

# Run shell in app container
docker-compose-run --rm app bash

# Rebuild CSS (should happen automatically)
docker-compose run --rm tailwind-dev npm run build
```


### Production Mode (`DEBUG=0`)

Build containers and start in daemon mode.

```bash
docker-compose build
docker-compose up -d
```

NOTE: gunicorn will listen on `127.0.0.1:${LISTEN_PORT}` (default `8000` in your `.env` file).
You will have to reverse proxy into the service using `nginx` (or similar) and serve the
static + media assets (deployed to the `static/` and `media/` folders, respectively).

A sample nginx config might be,

```nginx
server {
    listen 80;
    server_name sample.domain.com;

    location /static {
        alias /home/user/jew.pizza/static;
    }

    location /media {
        alias /home/user/jew.pizza/media;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```
