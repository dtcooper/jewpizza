FROM nginx:1.21.6-alpine AS modules

ARG NGX_BROTLI_VERSION=9aec15e2 \
    NGX_HEADERS_MORE_VERSION=0.33 \
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

RUN mkdir -p /usr/src/nginx && cd /usr/src/nginx && mkdir ../brotli ../nchan ../headers-more \
    && wget -qO - "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" | tar xz --strip=1  \
    && wget -qO - "https://github.com/google/ngx_brotli/tarball/${NGX_BROTLI_VERSION}" | tar xz --strip=1 -C ../brotli \
    && wget -qO - "https://github.com/slact/nchan/tarball/v${NGX_NCHAN_VERSION}" | tar xz --strip=1 -C ../nchan \
    && wget -qO - "https://github.com/openresty/headers-more-nginx-module/tarball/v${NGX_HEADERS_MORE_VERSION}" | tar xz --strip=1 -C ../headers-more \
    && CONFARGS=$(nginx -V 2>&1 | sed -n -e 's/^.*arguments: //p') \
    && sh -c "./configure --with-compat ${CONFARGS} --add-dynamic-module=../brotli --add-dynamic-module=../nchan --add-dynamic-module=../headers-more" \
    && make modules && strip objs/*.so


FROM jonasal/nginx-certbot:3.1.0-nginx1.21.6-alpine AS final

ARG JINJA2_CLI_VERSION=0.8.1

ENV CERTBOT_AUTHENTICATOR=dns-digitalocean \
    RENEWAL_INTERVAL=1d

RUN pip install --no-cache-dir jinja2-cli==$JINJA2_CLI_VERSION

RUN echo -e 'include modules.conf;\n' | cat - /etc/nginx/nginx.conf > /tmp/nginx.conf \
    && mv -v /tmp/nginx.conf /etc/nginx/nginx.conf \
    # Add hostname to nginx logs
    && sed -i 's/$remote_addr/$host \0/' /etc/nginx/nginx.conf

COPY --from=modules /usr/src/nginx/objs/*.so /usr/lib/nginx/modules/
COPY image/ /
