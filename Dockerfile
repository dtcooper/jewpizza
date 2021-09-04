FROM python:3.9

EXPOSE 8000/tcp

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.8

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
