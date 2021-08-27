FROM python:3.9

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_VERSION 1.1.8

RUN mkdir /app
WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock /app/
RUN poetry install
