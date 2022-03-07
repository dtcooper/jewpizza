#!/bin/sh

if [ "$(wget -q -O - -t 1 -T 15 http://localhost:8000/ping/)" = pong ]; then
    exit 0
else
    exit 1
fi
