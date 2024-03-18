ARG NGINX_CONTAINER_VERSION=1.25.4-alpine

# Alias container to copy over brotli module
FROM "georgjung/nginx-brotli:${NGINX_CONTAINER_VERSION}" AS brotli
FROM "jonasal/nginx-certbot:5.0.1-nginx${NGINX_CONTAINER_VERSION}" AS final

COPY --from=brotli \
    /etc/nginx/modules/ngx_http_brotli_static_module.so \
    /etc/nginx/modules/ngx_http_brotli_filter_module.so \
    /etc/nginx/modules/

# Add brotli module and hostname to nginx config
RUN echo -e '# Include brotli module\nload_module modules/ngx_http_brotli_static_module.so;\nload_module modules/ngx_http_brotli_filter_module.so;' \
        | cat - /etc/nginx/nginx.conf > /tmp/nginx.conf \
    && mv -v /tmp/nginx.conf /etc/nginx/nginx.conf \
    && sed -i 's/\$remote_addr/$host \0/' /etc/nginx/nginx.conf

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

ENV CERTBOT_AUTHENTICATOR=dns-digitalocean \
    RENEWAL_INTERVAL=1d

EXPOSE 80 443

COPY image/ /
