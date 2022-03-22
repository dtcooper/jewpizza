FROM nginx:1.21.6-alpine AS builder

ARG NGX_BROTLI_VERSION=9aec15e2 \
    NGX_DEVEL_KIT_VERSION=0.3.1 \
    NGX_HEADERS_MORE_VERSION=0.33 \
    NGX_LUA_RESTY_CORE_VERSION=0.1.23rc1 \
    NGX_LUA_RESTY_LRUCACHE_VERSION=0.11 \
    NGX_LUA_RESTY_REDIS_VERSION=0.30rc1 \
    NGX_LUA_VERSION=0.10.21rc2 \
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
    luajit-dev \
    make \
    openssl-dev \
    pcre-dev \
    perl-dev \
    zlib-dev

ENV LUAJIT_LIB=/usr/lib \
    LUAJIT_INC=/usr/include/luajit-2.1 \
    # Complation fix for lua module: https://github.com/openresty/lua-nginx-module/issues/715#issuecomment-272947697
    EXTRA_LD_OPT=-lpcre,-E

RUN mkdir -p /usr/src/nginx && cd /usr/src \
    && mkdir brotli headers-more nchan devel-kit lua lua-resty-core lua-resty-lrucache lua-resty-redis \
    && wget -qO - "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" | tar xz --strip=1 -C nginx \
    && wget -qO - "https://github.com/google/ngx_brotli/tarball/${NGX_BROTLI_VERSION}" | tar xz --strip=1 -C brotli \
    && wget -qO - "https://github.com/vision5/ngx_devel_kit/tarball/v${NGX_DEVEL_KIT_VERSION}" | tar xz --strip=1 -C devel-kit \
    && wget -qO - "https://github.com/openresty/headers-more-nginx-module/tarball/v${NGX_HEADERS_MORE_VERSION}" | tar xz --strip=1 -C headers-more \
    && wget -qO - "https://github.com/openresty/lua-nginx-module/tarball/v${NGX_LUA_VERSION}" | tar xz --strip=1 -C lua \
    && wget -qO - "https://github.com/openresty/lua-resty-core/tarball/v${NGX_LUA_RESTY_CORE_VERSION}" | tar xz --strip=1 -C lua-resty-core \
    && wget -qO - "https://github.com/openresty/lua-resty-lrucache/tarball/v${NGX_LUA_RESTY_LRUCACHE_VERSION}" | tar xz --strip=1 -C lua-resty-lrucache \
    && wget -qO - "https://github.com/openresty/lua-resty-redis/tarball/v${NGX_LUA_RESTY_REDIS_VERSION}" | tar xz --strip=1 -C lua-resty-redis \
    && wget -qO - "https://github.com/slact/nchan/tarball/v${NGX_NCHAN_VERSION}" | tar xz --strip=1 -C nchan \
    && cd lua-resty-core && make install PREFIX=/usr && cd .. \
    && cd lua-resty-lrucache && make install PREFIX=/usr && cd .. \
    && cd lua-resty-redis && make install PREFIX=/usr && cd .. \
    && cd nginx \
    && NGX_CONF_ARGS="$(nginx -V 2>&1 | sed -n -e 's/^.*arguments: //p' | sed "s/--with-ld-opt=[^ ]*/\0,$EXTRA_LD_OPT/")" \
    && sh -c "./configure --with-compat ${NGX_CONF_ARGS} --add-dynamic-module=../brotli --add-dynamic-module=../devel-kit \
        --add-dynamic-module=../lua --add-dynamic-module=../headers-more --add-dynamic-module=../nchan" \
    && make modules && strip objs/*.so


FROM jonasal/nginx-certbot:3.1.1-nginx1.21.6-alpine AS final

ARG JINJA2_CLI_VERSION=0.8.1

ENV CERTBOT_AUTHENTICATOR=dns-digitalocean \
    RENEWAL_INTERVAL=1d

RUN apk add --no-cache \
    luajit \
    pcre

RUN pip install --no-cache-dir jinja2-cli==$JINJA2_CLI_VERSION

RUN echo -e '# Include dynamic modules\ninclude "modules.conf";' | cat - /etc/nginx/nginx.conf > /tmp/nginx.conf \
    && mv -v /tmp/nginx.conf /etc/nginx/nginx.conf \
    # Add hostname to nginx logs
    && sed -i 's/\$remote_addr/$host \0/' /etc/nginx/nginx.conf

COPY --from=builder /usr/src/nginx/objs/*.so /usr/lib/nginx/modules/
COPY --from=builder /usr/lib/lua /usr/lib/lua
COPY image/ /
