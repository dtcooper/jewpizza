#!/bin/sh

if [ "$(wget -q -O - -T 15 http://localhost:8000/ping/ 2> /dev/null)" = pong ]; then
    exit 0
else
    exit 1
fi
