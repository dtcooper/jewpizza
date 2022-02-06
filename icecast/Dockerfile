FROM alpine:3.15 AS base


FROM base AS builder

ARG ICECAST_KH_VERSION="2.4.0-kh15"

RUN apk add --no-cache \
    build-base \
    libogg-dev \
    libtheora-dev \
    libvorbis-dev \
    libxslt-dev \
    speex-dev

RUN mkdir /build && cd /build \
    && wget -qO - "https://github.com/karlheyes/icecast-kh/archive/icecast-${ICECAST_KH_VERSION}.tar.gz" | tar xz --strip=1 \
    && ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var \
    && make && make install


FROM base

RUN apk add --no-cache \
    gettext \
    libogg \
    libtheora \
    libvorbis \
    libxslt \
    speex

RUN addgroup -S icecast && adduser -HSG icecast icecast \
    && mkdir /conf && chown icecast:icecast /conf

COPY --from=builder /usr/bin/icecast /usr/bin
COPY --from=builder /usr/share/icecast /usr/share/icecast
COPY icecast.xml.template /etc

USER icecast
CMD sh -c 'envsubst < /etc/icecast.xml.template > /conf/icecast.xml && exec icecast -c /conf/icecast.xml'
