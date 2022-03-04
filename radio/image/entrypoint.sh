#!/bin/sh

cd /var/liquidsoap

if [ -f /.env ]; then
    . /.env
else
    echo "Couldn't find .env file. Exiting."
    exit 1
fi

SCRIPT_URL="http://app:8000/internal/radio/liquidsoap/script/"
SCRIPT="/var/liquidsoap/script.liq"

wait_for_service() {
    echo "Waiting for ${1}..."
    wait-for -t 0 "$1"
}

kill_children() {
    kill $(jobs -p) 2> /dev/null
}

if [ "$#" != 0 ]; then
    exec "$@"
else
    wait_for_service app:8000

    wget -O "$SCRIPT" --header "X-Secret-Key: $SECRET_KEY" "$SCRIPT_URL"
    if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
        pygmentize -l ruby "$SCRIPT" | cat -n
    fi

    exec liquidsoap -f "$SCRIPT"
fi
