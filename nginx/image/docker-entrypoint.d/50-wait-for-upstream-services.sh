#!/bin/sh

SERVICES='app:8000 logs:8080 umami:3000 icecast:8888'

for service in $SERVICES; do
    wait-for-it -t 0 "$service"
done
