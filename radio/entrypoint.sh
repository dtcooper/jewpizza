#!/bin/sh

if [ "$#" != 0 ]; then
    exec "$@"
else
    wait-for-it -t 0 app:8000

    URL="http://app:8000/internal/radio/script/${SCRIPT_NAME}/"
    SCRIPT="/radio/script.liq"
    if ! wget -qO /radio/script.liq "$URL" ; then
        echo "Error fetching script at $URL"
        exit 1
    fi

    echo "Downloaded $SCRIPT_NAME script to $SCRIPT"
    exec liquidsoap "$SCRIPT"
fi
