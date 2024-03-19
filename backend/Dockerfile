FROM python:3.12.2-bookworm

ENV DJANGO_SETTINGS_MODULE=jewpizza.settings \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

ARG POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml poetry.lock /app/
WORKDIR /app
ARG DEV_MODE=0
RUN poetry install $([ -z "$DEV_MODE" -o "$DEV_MODE" = '0' ] && echo '--without=dev') \
    && if [ "$DEV_MODE" -a "$DEV_MODE" != '0' ]; then \
        # Download relevant verion's bash completion (in dev only)
        wget -qO /etc/bash_completion.d/django_bash_completion \
            "https://raw.githubusercontent.com/django/django/$(python -c 'import django; print(".".join(map(str, django.VERSION[:2])))')/extras/django_bash_completion" \
    ; fi

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]
CMD []
