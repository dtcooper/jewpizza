FROM python:3.9

EXPOSE 8000/tcp

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG POETRY_VERSION=1.1.8 \
    DEBUG=0

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO /usr/local/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/81b1373f/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

RUN mkdir -p /app/backend
WORKDIR /app/backend
COPY backend/pyproject.toml backend/poetry.lock /app/backend/
RUN poetry install \
    $(if [ -z "$DEBUG" -o "$DEBUG" = '0' ]; then echo '--no-dev'; fi)

RUN mkdir -p /app/frontend
COPY frontend/package.json frontend/package-lock.json /app/frontend/
RUN npm --prefix=../frontend install \
    && echo "alias npm='npm --prefix=/app/frontend'" >> /root/.bashrc

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]
CMD []
