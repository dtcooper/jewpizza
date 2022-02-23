FROM python:3.10 as base


# Build frontend
FROM node:16-alpine AS frontend

COPY frontend/package.json frontend/package-lock.json /app/frontend/
WORKDIR /app/frontend
RUN npm install --production

COPY backend/ /app/backend
COPY frontend/ /app/frontend
RUN npm run build

# audiowaveform tool
FROM base as audiowaveform

ARG AUDIOWAVEFORM_VERSION=1.6.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        cmake \
        g++ \
        gcc \
        libboost-filesystem-dev \
        libboost-program-options-dev \
        libboost-regex-dev \
        libgd-dev \
        libid3tag0-dev \
        libmad0-dev \
        libsndfile1-dev \
        make \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/audiowaveform && cd /usr/src/audiowaveform \
    && wget -qO - "https://github.com/bbc/audiowaveform/archive/refs/tags/${AUDIOWAVEFORM_VERSION}.tar.gz" | tar xz --strip-components 1 \
    && mkdir build && cd build \
    && cmake -D ENABLE_TESTS=0 .. \
    && make && make install


# Actual app container
FROM base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=jew_pizza.settings

ARG POETRY_VERSION=1.1.13 \
    WAIT_FOR_IT_VERSION=81b1373f \
    DEBUG=0

RUN if [ "$DEBUG" -a "$DEBUG" != '0' ]; then \
        curl -fsSL https://deb.nodesource.com/setup_16.x | bash \
        && echo "alias npm='npm --prefix=/app/frontend'" >> /root/.bashrc \
        && echo "alias npx='npx --prefix=/app/frontend'" >> /root/.bashrc \
        && echo "alias redis-cli='redis-cli -h redis'" >> /root/.bashrc \
    ; fi \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        # For audiowaveform
        libboost-filesystem1.74.0 \
        libboost-program-options1.74.0 \
        libboost-regex1.74.0 \
        libgd3 \
        libid3tag0 \
        libmad0 \
        libsndfile1 \
        # Dev requirements
        $([ "$DEBUG" -a "$DEBUG" != '0' ] && echo \
            jq \
            less \
            nano \
            netcat \
            nodejs \
            postgresql-client \
            redis-tools \
        ) \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO /usr/local/bin/wait-for-it "https://raw.githubusercontent.com/vishnubob/wait-for-it/${WAIT_FOR_IT_VERSION}/wait-for-it.sh" \
    && chmod +x /usr/local/bin/wait-for-it

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY backend/pyproject.toml backend/poetry.lock /app/backend/
WORKDIR /app/backend

# In prod use "--no-dev"
RUN poetry install $([ -z "$DEBUG" -o "$DEBUG" = '0' ] && echo '--no-dev')

# Copy over needed files from source tree (break symlinks)
COPY backend/ /app/backend
COPY README.md /app/
COPY radio/reload.liq /app/backend/radio/jinja2/radio/

# Copy over needed files from stages (overwrite symlinks)
RUN rm -vrf /app/backend/admin_tools/static/admin_tools/vendor/
COPY --from=frontend /app/frontend/node_modules/simpledotcss/simple.*css /app/backend/admin_tools/static/admin_tools/vendor/css/
COPY --from=frontend /app/frontend/node_modules/alpinejs/dist/cdn.js /app/backend/admin_tools/static/admin_tools/vendor/js/alpine.js
COPY --from=frontend /app/frontend/node_modules/alpinejs/dist/cdn.min.js /app/backend/admin_tools/static/admin_tools/vendor/js/alpine.min.js
COPY --from=frontend /app/backend/webcore/static/webcore/css/*.min.css* /app/backend/webcore/static/webcore/css/
COPY --from=frontend /app/backend/webcore/static/webcore/js/* /app/backend/webcore/static/webcore/js/
COPY --from=audiowaveform /usr/local/bin/audiowaveform /usr/local/bin/audiowaveform

ENTRYPOINT ["/app/backend/entrypoint.sh"]
CMD []

ARG GIT_REV=unknown \
    BUILD_DATE=unknown
ENV GIT_REV=${GIT_REV} \
    BUILD_DATE=${BUILD_DATE}
