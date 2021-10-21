# aiohttp throws exception with Python 3.10 - https://github.com/aio-libs/aiohttp/issues/5996
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG POETRY_VERSION=1.1.11 \
    WAIT_FOR_IT_VERSION=81b1373f \
    DEBUG=0

RUN wget -qO /usr/local/bin/wait-for-it "https://raw.githubusercontent.com/vishnubob/wait-for-it/${WAIT_FOR_IT_VERSION}/wait-for-it.sh" \
    && chmod +x /usr/local/bin/wait-for-it

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

RUN mkdir /app
WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry install \
    # In prod use "--no-dev"
    $(if [ -z "$DEBUG" -o "$DEBUG" = '0' ]; then echo '--no-dev'; fi)

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]
