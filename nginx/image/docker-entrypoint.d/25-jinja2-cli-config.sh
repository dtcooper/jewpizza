#!/bin/sh

SCRIPT="$(basename "$0")"
TEMPLATE_FILE=/etc/nginx/templates/jewpizza.conf.j2
CONF_FILE=/etc/nginx/conf.d/jewpizza.conf

if [ -f /.env ]; then
    set -a
    . /.env
    set +a
else
    echo "Couldn't find .env file. Exiting."
    exit 1
fi

export DNS_RESOLVER_IP="$(grep nameserver /etc/resolv.conf | grep -o '[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*')"
echo "Using resolver IP: $DNS_RESOLVER_IP"

for subdomain in $NGINX_EXTRA_SUBDOMAINS; do
    subdomain="$(echo "$subdomain" | cut -d ':' -f 1)"
    mkdir -p "/serve/$subdomain"
done

echo "$SCRIPT: Rendering jinja2 template ($TEMPLATE_FILE)"

# --format=env and empty env (/dev/null) needed to fix weird bug
# And we can't use /etc/.env as input file, jinja2-cli doesn't properly allow
# quoted strings in env file
jinja2 --format=env -o "$CONF_FILE" "$TEMPLATE_FILE" /dev/null

if [ ! -f "$CONF_FILE" ]; then
    echo "$SCRIPT: $CONF_FILE failed to render. Exiting."
    exit 1
fi

echo "$SCRIPT: Rendered config ($CONF_FILE)"

if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
    echo "========== begin: $CONF_FILE =========="
    cat -n "$CONF_FILE"
    echo "=========== end: $CONF_FILE ==========="
fi
