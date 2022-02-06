FROM jonasal/nginx-certbot:3.0-alpine AS base


FROM base AS brotli

ARG NGX_BROTLI_VERSION=9aec15e2

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

RUN mkdir -p /build /brotli \
    && wget -qO - "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" | tar xz --strip=1 -C /build \
    && wget -qO - "https://github.com/google/ngx_brotli/tarball/${NGX_BROTLI_VERSION}" | tar xz --strip=1 -C /brotli \
    && cd /build \
    && CONFARGS=$(nginx -V 2>&1 | sed -n -e 's/^.*arguments: //p') \
    && sh -c "./configure --with-compat ${CONFARGS} --add-dynamic-module=/brotli" \
    && make modules


FROM base

ARG JINJA2_CLI_VERSION=0.8.1

ENV CERTBOT_AUTHENTICATOR=dns-digitalocean

RUN pip install --no-cache-dir jinja2-cli==$JINJA2_CLI_VERSION

RUN echo -e 'load_module "modules/ngx_http_brotli_filter_module.so";\nload_module "modules/ngx_http_brotli_static_module.so";\n' \
        | cat - /etc/nginx/nginx.conf > /tmp/nginx.conf \
    && mv /tmp/nginx.conf /etc/nginx/nginx.conf

COPY --from=brotli \
    /build/objs/ngx_http_brotli_filter_module.so /build/objs/ngx_http_brotli_static_module.so \
    /usr/lib/nginx/modules/
COPY image/ /
