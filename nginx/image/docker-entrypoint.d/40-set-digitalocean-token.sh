#!/bin/sh

INI_FILE=/etc/letsencrypt/digitalocean.ini
SCRIPT="$(basename "$0")"

# ALSO use USE_LOCAL_CA with dir mounted, with instructions on how to install

if [ "$DIGITALOCEAN_API_TOKEN" -a "$USE_LOCAL_CA" -ne '1' ]; then
    echo "$SCRIPT: Writing digitalocean API token to $INI_FILE"
    echo "dns_digitalocean_token = $DIGITALOCEAN_API_TOKEN" > "$INI_FILE"
    chmod 600 "$INI_FILE"

elif [ -z "$DEBUG" -o "$DEBUG" = '0' ]; then
    echo "$SCRIPT: DIGITALOCEAN_API_TOKEN needs to be set. See .env file."
    exit 1

elif [ "$USE_LOCAL_CA" -ne '1' ]; then
    echo "$SCRIPT: set NGINX_DEBUG_MODE_ONLY_USE_LOCAL_CERTIFICATE_AUTHORITY=1 or DIGITALOCEAN_API_TOKEN. See .env file."
    exit 1
fi
