# jew.pizza Website

Here's the code for the website that powers [`jew.pizz`](https://jew.pizza).

## Setup

Create an edit `.env`, and optionally copy over docker-compose dev overrides.

```bash
# Edit me
cp .env.sample .env

# NOTE: Do this UNLESS deploying to production
ln -s docker-compose.dev.yml docker-compose.override.yml
```

## Running

### Development mode (`DEBUG=1`)

Build and start containers,

```bash
docker-compose build
docker-compose up
```

The development server will run at <http://localhost:8000/>.

### Production mode (`DEBUG=0`)

Build and start containers,

```bash
docker-compose build
docker-compose up -d
```

NOTE: gunicorn will listen on `127.0.0.1:${LISTEN_PORT}` (default `8000` in your `.env` file).
You will have to reverse proxy into the service using `nginx` (or similar) and serve the
static + media assets (deployed to the `static/` and `media/` folders, respectively).
