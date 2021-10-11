# jew.pizza Website ✡️🍕🥸

Here's the code for the website that powers [`jew.pizza`](https://jew.pizza), my
personal website.


## Initial Setup

Clone, then copy and edit the `.env` file, and optionally copy over the docker compose dev
overrides.

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

Build containers and start in daemon mode.

```bash
docker compose build
docker compose up -d
```

NOTE: [Gunicorn](https://gunicorn.org/) will listen on `127.0.0.1:${LISTEN_PORT}`
(default `8000` in your `.env` file). You will have to reverse proxy into the service
using `nginx` (or similar) and serve the static and media assets (deployed to the
`serve/static/` and `serve/media/` folders, respectively).

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

Or if you want to **TEST** with `DEBUG=0` without running nginx and have Gunicorn
serve your static assets using [Whitenoise](http://whitenoise.evans.io/en/stable/),
add the following to your `.env` file,

```
SERVE_ASSETS_FROM_DJANGO=1
```

#### Change Passwords

Change passwords,
* Django: `dave:cooper`
* Umami: `dave:cooper`

#### Icecast 2 in Production

TODO needs documenting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
