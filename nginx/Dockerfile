FROM jonasal/nginx-certbot:3.0-alpine AS base


FROM base AS modules

ARG NGX_BROTLI_VERSION=9aec15e2 \
    NGX_NCHAN_VERSION=1.2.15

# From https://github.com/nginxinc/docker-nginx/blob/master/stable/alpine/Dockerfile
RUN apk add --no-cache \
    alpine-sdk \
    bash \
    findutils \
    gcc \
    gd-dev \
    geoip-dev \
    libc-dev \
    libedit-dev \
    libxslt-dev \
    linux-headers \
    make \
    openssl-dev \
    pcre-dev \
    perl-dev \
    zlib-dev

RUN mkdir -p /build /brotli /nchan \
    && wget -qO - "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" | tar xz --strip=1 -C /build \
    && wget -qO - "https://github.com/google/ngx_brotli/tarball/${NGX_BROTLI_VERSION}" | tar xz --strip=1 -C /brotli \
    && wget -qO - "https://github.com/slact/nchan/tarball/v${NGX_NCHAN_VERSION}" | tar xz --strip=1 -C /nchan \
    && cd /build \
    && CONFARGS=$(nginx -V 2>&1 | sed -n -e 's/^.*arguments: //p') \
    && sh -c "./configure --with-compat ${CONFARGS} --add-dynamic-module=/brotli --add-dynamic-module=/nchan" \
    && make modules


FROM base

ARG JINJA2_CLI_VERSION=0.8.1

ENV CERTBOT_AUTHENTICATOR=dns-digitalocean

RUN pip install --no-cache-dir jinja2-cli==$JINJA2_CLI_VERSION

RUN echo -e 'include modules.conf;\n' | cat - /etc/nginx/nginx.conf > /tmp/nginx.conf \
    && mv -v /tmp/nginx.conf /etc/nginx/nginx.conf \
    # Add hostname to nginx logs
    && sed -i 's/$remote_addr/$host \0/' /etc/nginx/nginx.conf

COPY --from=modules /build/objs/*.so /usr/lib/nginx/modules/
COPY image/ /
