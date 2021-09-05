# jew.pizza Website

Here's the code for the website that powers [`jew.pizz`](https://jew.pizza).


## Setup

Create an edit `.env`, and optionally copy over docker-compose dev overrides.

```bash
# Edit me
cp .env.sample .env

# NOTE: Make sure to symlink this if you're developing or running with DEBUG=1
#       otherwise CSS won't work properly
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
# Rebuild CSS (should happen automatically)
docker-compose run --rm tailwind-dev npm run build

# Django management command
docker-compose-run --rm app poetry run ./manage.py

# Run shell in app container
docker-compose-run --rm app bash
poetry shell  # optional, if you want the Python environment
```


### Production Mode (`DEBUG=0`)

Build and start containers,

```bash
docker-compose build
docker-compose up -d
```

NOTE: gunicorn will listen on `127.0.0.1:${LISTEN_PORT}` (default `8000` in your `.env` file).
You will have to reverse proxy into the service using `nginx` (or similar) and serve the
static + media assets (deployed to the `static/` and `media/` folders, respectively).
