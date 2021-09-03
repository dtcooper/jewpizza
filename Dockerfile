FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.8

# Install node and some other useful packages
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get update \
    && apt-get install --yes --no-install-recommends \
        libpq-dev \
        nodejs \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO /usr/local/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/81b1373f/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it

RUN mkdir -p /app/jew_pizza
WORKDIR /app/jew_pizza

RUN pip install "poetry==$POETRY_VERSION"

COPY jew_pizza/pyproject.toml jew_pizza/poetry.lock /app/jew_pizza/
RUN poetry install

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]
CMD []
