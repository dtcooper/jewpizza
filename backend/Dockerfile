FROM python:3.10 as audiowaveform-builder

ARG AUDIOWAVEFORM_VERSION=1.5.1

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

RUN wget -qO - "https://github.com/bbc/audiowaveform/archive/refs/tags/${AUDIOWAVEFORM_VERSION}.tar.gz" | tar xz -C /tmp \
    && cd "/tmp/audiowaveform-${AUDIOWAVEFORM_VERSION}" \
    && mkdir build && cd build \
    && cmake -D ENABLE_TESTS=0 .. \
    && make && make install

FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=jew_pizza.settings

ARG POETRY_VERSION=1.1.12 \
    WAIT_FOR_IT_VERSION=81b1373f \
    DEBUG=0

COPY --from=audiowaveform-builder /usr/local/bin/audiowaveform /usr/local/bin/audiowaveform

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        brotli \
        ffmpeg \
        gzip \
        nodejs \
        # For audiowaveform
        libboost-filesystem1.74.0 \
        libboost-program-options1.74.0 \
        libboost-regex1.74.0 \
        libgd3 \
        libid3tag0 \
        libmad0 \
        # Dev requirements
        $([ "$DEBUG" -a "$DEBUG" != '0' ] && echo \
            jq \
            less \
            nano \
            netcat \
            postgresql-client \
            redis-tools \
        ) \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO /usr/local/bin/wait-for-it "https://raw.githubusercontent.com/vishnubob/wait-for-it/${WAIT_FOR_IT_VERSION}/wait-for-it.sh" \
    && chmod +x /usr/local/bin/wait-for-it

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

RUN mkdir -p /app/backend
WORKDIR /app/backend
COPY backend/pyproject.toml backend/poetry.lock /app/backend/
RUN poetry install \
    # In prod use "--no-dev"
    $([ -z "$DEBUG" -o "$DEBUG" = '0' ] && echo '--no-dev')

RUN mkdir -p /app/frontend
COPY frontend/package.json frontend/package-lock.json /app/frontend/
RUN npm --prefix=../frontend install $([ -z "$DEBUG" -o "$DEBUG" = '0' ] && echo '--production') \
    && echo "alias npm='npm --prefix=/app/frontend'" >> /root/.bashrc \
    && echo "alias npx='npx --prefix=/app/frontend'" >> /root/.bashrc \
    # May as well set redis-cli alias while we're at it
    && echo "alias redis-cli='redis-cli -h redis'" >> /root/.bashrc

COPY . /app/

RUN npm --prefix=../frontend run build

ENTRYPOINT ["/app/backend/entrypoint.sh"]
CMD []

ARG GIT_REV=unknown
ENV GIT_REV=${GIT_REV}
