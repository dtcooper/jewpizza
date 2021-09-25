#!/bin/sh

cd /app/backend

# Use the poetry's virtualenv
export PATH="$(poetry env info -p)/bin:$PATH"

# Source .env file
if [ -f /.env ]; then
    . /.env
else
    echo "Couldn't find .env file. Exiting."
    exit 1
fi

if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
    DEBUG=1
    if [ ! -f ../docker-compose.override.yml ]; then
        echo "WARNING: docker-compose.override.yml NOT found. You'll need to symlink so DEBUG can to work properly."
    fi
else
    DEBUG=
fi

# Check if secret key is set
if [ -z "$SECRET_KEY" ]; then
    echo 'Generating secret key in .env file'
    NEW_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(40))')"

    if grep -q '^SECRET_KEY=' /.env; then
        # sed in place doesn't work on docker file mounts, so copy
        sed "s/^SECRET_KEY=.*/SECRET_KEY='$NEW_SECRET_KEY'/" /.env > /tmp/new.env
        cat /tmp/new.env > /.env
        rm /tmp/new.env
    else
        echo "\nSECRET_KEY='$NEW_SECRET_KEY'" >> /.env
    fi

    . /.env
fi


if [ "$#" != 0 ]; then
    if [ "$DEBUG" ] ; then
        # Make psql work easily
        export PGHOST=db
        export PGUSER=postgres
        export PGPASSWORD=postgres
    fi

    exec "$@"
else
    if [ "$DEBUG" ]; then
        if [ ! -d '../frontend/node_modules' ]; then
            # In case /app is mounted in Docker, needed to re-install the /app/frontend/node_modules folder
            npm --prefix=../frontend install
        fi
    else
        npm --prefix=../frontend run build
        ./manage.py collectstatic --noinput
    fi

    wait-for-it -t 0 db:5432 -- ./manage.py migrate

    if [ "$DEBUG" ]; then
        exec ./manage.py runserver
    else
        if [ -z "$GUNICORN_WORKERS" ]; then
            # Number of workers =  min(<cores * 1.5 rounded up> + 1, 3)
            GUNICORN_WORKERS="$(python -c 'import multiprocessing as m; print(max(round(m.cpu_count() * 1.5 + 1), 3))')"
        fi

        exec gunicorn \
                $GUNICORN_EXTRA_ARGS \
                --forwarded-allow-ips '*' \
                -b 0.0.0.0:8000 \
                -w $GUNICORN_WORKERS \
                --capture-output \
                --error-logfile - \
                --access-logfile - \
            jew_pizza.wsgi
    fi
fi
