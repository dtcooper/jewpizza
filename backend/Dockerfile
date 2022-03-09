FROM python:3.10-alpine AS base

ARG POETRY_VERSION=1.1.13


# Build frontend
FROM node:16-alpine AS frontend

COPY frontend/package.json frontend/package-lock.json /app/frontend/
WORKDIR /app/frontend
RUN npm install --production

COPY backend/ /app/backend
COPY frontend/ /app/frontend

ARG GIT_REV=unknown
RUN sed -i "s/\(jew\.pizza compiled [a-zA-Z]*\)\\\\n/\1 (revision $GIT_REV)\\\\n/" package.json \
    && npm run build


FROM base as audiowaveform

ARG AUDIOWAVEFORM_VERSION=1.6.0

RUN apk add --no-cache \
        boost-dev \
        cmake \
        g++ \
        gcc \
        gd-dev \
        libid3tag-dev \
        libmad-dev \
        libsndfile-dev \
        make

RUN mkdir -p /usr/src/audiowaveform && cd /usr/src/audiowaveform \
    && wget -qO - "https://github.com/bbc/audiowaveform/archive/refs/tags/${AUDIOWAVEFORM_VERSION}.tar.gz" | tar xz --strip-components 1 \
    && mkdir build && cd build \
    && cmake -D ENABLE_TESTS=0 .. \
    && make && make install


FROM base AS poetry

RUN apk add --no-cache \
    libffi-dev \
    gcc \
    musl-dev

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY backend/pyproject.toml backend/poetry.lock /app/backend/
WORKDIR /app/backend

RUN poetry export > requirements.txt \
    && poetry export --dev --without-hashes | grep '^pytest' > requirements-tests.txt


FROM base AS final

ARG DEBUG=0 \
    WAIT_FOR_VERSION=2.2.3

ENV DJANGO_SETTINGS_MODULE=jew_pizza.settings \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN wget -qO /usr/local/bin/wait-for "https://raw.githubusercontent.com/eficode/wait-for/v${WAIT_FOR_VERSION}/wait-for" \
    && chmod +x /usr/local/bin/wait-for

RUN apk add --no-cache \
        # Keep for audiowaveform + psycopg2 + ffmpeg
        boost-filesystem \
        boost-program_options \
        boost-regex \
        ffmpeg \
        libgd \
        libid3tag \
        libmad \
        libpq \
        libsndfile \
    && if [ "$DEBUG" -a "$DEBUG" != '0' ]; then \
        # Add extra packages, poetry, and shell niceities
        apk add --no-cache \
            # Dev extras
            jq \
            redis \
            # Needed for poetry + poetry install (g++ for brotli, poetry doesn't pull in the binary wheel bug @ v1.1.13)
            g++ \
            gcc \
            libffi-dev \
            libpq-dev \
            musl-dev \
            # Needed for frontend dev
            nodejs \
            npm \
        && pip install --no-cache-dir "poetry==$POETRY_VERSION" \
        && mv -v /etc/profile.d/color_prompt.sh.disabled /etc/profile.d/color_prompt.sh \
        && echo "alias npm='npm --prefix=/app/frontend'" > /etc/profile.d/aliases.sh \
        && echo "alias npx='npx --prefix=/app/frontend'" >> /etc/profile.d/aliases.sh \
        && echo "alias redis-cli='redis-cli -h redis'" >> /etc/profile.d/aliases.sh \
    ; fi

COPY --from=poetry /app/backend/requirements.txt /app/backend/requirements-tests.txt /app/backend/
COPY backend/pyproject.toml backend/poetry.lock /app/backend/
WORKDIR /app/backend

RUN if [ "$DEBUG" -a "$DEBUG" != '0' ]; then \
        poetry install \
    ; else \
        # Packages needed for pip install, removed afterwards
        apk add --no-cache \
            libpq-dev \
            gcc \
            musl-dev \
        && pip install --no-cache-dir -r requirements.txt \
        && apk del \
            libpq-dev \
            gcc \
            musl-dev \
    ; fi

# Copy over needed files from source tree (break symlinks)
COPY backend/ /app/backend
COPY radio/reload.liq /app/backend/radio/jinja2/radio/

# Copy over needed files from stages (overwrite symlinks)
COPY --from=audiowaveform /usr/local/bin/audiowaveform /usr/local/bin/audiowaveform
RUN rm -vrf /app/backend/admin_tools/static/admin_tools/vendor/
COPY --from=frontend /app/frontend/node_modules/simpledotcss/simple.*css /app/backend/admin_tools/static/admin_tools/vendor/css/
COPY --from=frontend /app/frontend/node_modules/alpinejs/dist/cdn.js /app/backend/admin_tools/static/admin_tools/vendor/js/alpine.js
COPY --from=frontend /app/frontend/node_modules/alpinejs/dist/cdn.min.js /app/backend/admin_tools/static/admin_tools/vendor/js/alpine.min.js
COPY --from=frontend /app/backend/webcore/static/webcore/css/*.min.css* /app/backend/webcore/static/webcore/css/
COPY --from=frontend /app/backend/webcore/static/webcore/js/* /app/backend/webcore/static/webcore/js/

ENTRYPOINT ["/app/backend/entrypoint.sh"]
CMD []

ARG GIT_REV=unknown \
    BUILD_DATE=unknown
ENV GIT_REV=${GIT_REV} \
    BUILD_DATE=${BUILD_DATE}
