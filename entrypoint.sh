#!/bin/sh

if [ "$#" = 0 ]; then
    exec poetry run ./manage.py runserver
else
    exec $@
fi
