#!/bin/sh

SCRIPT="$(basename "$0")"
TEMPLATE_FILE=/etc/nginx/templates/jewpizza.conf.j2
CONF_FILE=/etc/nginx/conf.d/jewpizza.conf

echo "$SCRIPT: Rendering jinja2 template ($TEMPLATE_FILE)"
jinja2 --format=env "$TEMPLATE_FILE" /.env > "$CONF_FILE"
echo "$SCRIPT: Rendered config ($CONF_FILE)"

if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
    echo "------------- $CONF_FILE -------------"
    cat "$CONF_FILE"
    echo "------------- $CONF_FILE -------------"
fi
