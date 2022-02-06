#!/bin/sh

SCRIPT="$(basename "$0")"

echo "$SCRIPT: Rendering jinja2 template (jewpizza.conf.j2)"
jinja2 --format=env /etc/nginx/templates/jewpizza.conf.j2 /.env | tee /etc/nginx/conf.d/jewpizza.conf
