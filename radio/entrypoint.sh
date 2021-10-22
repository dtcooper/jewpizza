#!/bin/sh

cd /radio

if [ -f /.env ]; then
    . /.env
else
    echo "Couldn't find .env file. Exiting."
    exit 1
fi

wait_for_services() {
    wait-for-it -t 0 app:8000
    wait-for-it -t 0 redis:6379
}

if [ "$#" != 0 ]; then
    exec "$@"
elif [ "$DEBUG" -a "$DEBUG" != '0' -a -d /watch -a -z "$__SKIP_WATCHDOG" ]; then
    wait_for_services
    export __SKIP_WATCHDOG=1
    exec watchmedo auto-restart --directory=/watch/ --pattern=*.liq -- /entrypoint.sh
else
    if [ -z "$__SKIP_WATCHDOG" ]; then
        wait_for_services
    fi

    URL="http://app:8000/internal/radio/liquidsoap/script/"
    SCRIPT="/radio/script.liq"
    if ! wget "--header=X-Secret-Key: $SECRET_KEY" -qO /radio/script.liq "$URL" ; then
        echo "Error fetching script at $URL"
        exit 1
    fi

    echo "Downloaded script to $SCRIPT"
    if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
        echo '===== script.liq ====='
        pygmentize -l ruby "$SCRIPT" | cat -n
        echo '======================'
    fi

    exec liquidsoap "$SCRIPT"
fi
