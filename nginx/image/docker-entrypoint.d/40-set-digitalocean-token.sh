#!/bin/sh

INI_FILE=/etc/letsencrypt/digitalocean.ini
SCRIPT="$(basename "$0")"

echo "$SCRIPT: Writing digitalocean API token to $INI_FILE"
echo "$SCRIPT: dns_digitalocean_token = $DIGITALOCEAN_API_TOKEN" > "$INI_FILE"
chmod 600 "$INI_FILE"
