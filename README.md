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

Build and start containers

```bash
docker-compose build
docker-compose up
```
