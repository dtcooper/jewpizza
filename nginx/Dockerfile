ARG NGINX_CONTAINER_VERSION=1.25.4-alpine

# Alias container to copy over brotli module
FROM "georgjung/nginx-brotli:${NGINX_CONTAINER_VERSION}" AS brotli-copy
FROM "jonasal/nginx-certbot:5.0.1-nginx${NGINX_CONTAINER_VERSION}" AS final

COPY --from=brotli-copy \
    /etc/nginx/modules/ngx_http_brotli_static_module.so \
    /etc/nginx/modules/ngx_http_brotli_filter_module.so \
    /etc/nginx/modules/

# Add brotli module and hostname to nginx config
RUN echo -e '# Include brotli module\nload_module modules/ngx_http_brotli_static_module.so;\nload_module modules/ngx_http_brotli_filter_module.so;' \
        | cat - /etc/nginx/nginx.conf > /tmp/nginx.conf \
    && mv -v /tmp/nginx.conf /etc/nginx/nginx.conf \
    && sed -i 's/\$remote_addr/$host \0/' /etc/nginx/nginx.conf

ARG JINJA2_CLI_VERSION=0.8.2 \
    DOTENV_VERSION=1.0.1
RUN pip install --no-cache-dir "jinja2-cli==$JINJA2_CLI_VERSION" "python-dotenv[cli]==$DOTENV_VERSION"

ENV CERTBOT_AUTHENTICATOR=dns-digitalocean \
    RENEWAL_INTERVAL=1d

EXPOSE 80 443

ADD image/ /
