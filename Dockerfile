FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.8

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        libpq-dev \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock /app/
RUN poetry install
