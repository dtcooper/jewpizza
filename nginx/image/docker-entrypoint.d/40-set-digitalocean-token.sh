#!/bin/bash

set -e

ME="$(basename "$0")"

INI_FILE=/etc/letsencrypt/digitalocean.ini

entrypoint_log() {
    if [ -z "${NGINX_ENTRYPOINT_QUIET_LOGS:-}" ]; then
        echo "$@"
    fi
}

# ALSO use USE_LOCAL_CA with dir mounted, with instructions on how to install
if [ "$DIGITALOCEAN_API_TOKEN" -a "$USE_LOCAL_CA" != '1' ]; then
    entrypoint_log "$ME: Writing digitalocean API token to $INI_FILE"
    echo "dns_digitalocean_token = $DIGITALOCEAN_API_TOKEN" > "$INI_FILE"
    chmod 600 "$INI_FILE"
elif [ "$USE_LOCAL_CA" != '1' ]; then
    entrypoint_log "$ME: ERROR: Set USE_LOCAL_CA=1 or DIGITALOCEAN_API_TOKEN=<token>. See .env file."
    exit 1
fi
