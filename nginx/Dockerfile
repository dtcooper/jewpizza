FROM jonasal/nginx-certbot:5.0.1-nginx1.25.4

# Add hostname to nginx config
RUN sed -i 's/\$remote_addr/$host \0/' /etc/nginx/nginx.conf

# Allow pip to work, normally I'd use poetry but it's just a few packages for the entrypoint
ARG PIP_BREAK_SYSTEM_PACKAGES=1
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

ENV CERTBOT_AUTHENTICATOR=dns-digitalocean \
    RENEWAL_INTERVAL=1d

EXPOSE 80 443

COPY image/ /
