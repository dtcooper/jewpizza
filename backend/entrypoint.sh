#!/bin/sh

cd /app/backend

# Source .env file
if [ -f /.env ]; then
    . /.env
else
    echo "Couldn't find .env file. Exiting."
    exit 1
fi

if [ "$DEBUG" -a "$DEBUG" != '0' ]; then
    DEBUG=1
    # Use the poetry's virtualenv (DEBUG only)
    export PATH="$(poetry env info -p)/bin:$PATH"
else
    DEBUG=
fi

if [ -z "$NO_STARTUP_MESSAGE" ]; then
    printf "Starting app container revision $GIT_REV built on $(date -d "@$(date -u -D '%Y-%m-%dT%TZ' -d "$BUILD_DATE" +%s)")"
    if [ "$DEBUG" ]; then
        printf ' (DEBUG mode on)'
    fi
    echo
fi

if [ "$DEBUG" -a ! -f ../docker-compose.override.yml ]; then
    echo "WARNING: docker-compose.override.yml NOT found. You'll need to symlink so DEBUG can to work properly."
fi

if [ "$RUN_HUEY" ]; then
    export __RUN_HUEY=1
fi

if [ -z "$SECRET_KEY" ]; then
    echo "SECRET_KEY not set. Exiting."
    exit 1
fi

wait_for_service() {
    echo "Waiting for ${1}..."
    wait-for -t 0 "$1"
}

init_db () {
    if [ "$(./manage.py shell -c 'from django.contrib.auth.models import User; print("" if User.objects.exists() else "1")')" = 1 ]; then
        DJANGO_SUPERUSER_PASSWORD=cooper ./manage.py createsuperuser --noinput --username dave --email 'david@jew.pizza'
    fi

    ./manage.py loaddata shows/showdates.json shows/episodes.json
}

init_umami_debug_only () {
    if [ -z "$(./manage.py constance get UMAMI_WEBSITE_ID)" ]; then
        echo "No UMAMI_WEBSITE_ID with DEBUG = True. Setting..."
        wait_for_service umami:3000
        WEBSITE_ID="$(cat <<'END' | python
import requests

token = requests.post(
'http://umami:3000/api/auth/login',
json={'username': 'dave', 'password': 'cooper'}).json()['token']
uuid = requests.post(
'http://umami:3000/api/website',
json={'domain': 'localhost', 'name': 'jew.pizza local dev', 'enable_share_url': False},
headers={'Authorization': f'Bearer {token}'}).json()['website_uuid']
print(uuid)
END
)"
        wait_for_service redis:6379
        ./manage.py constance set UMAMI_WEBSITE_ID "$WEBSITE_ID"
    fi
}

if [ "$#" != 0 ]; then
    if [ "$DEBUG" ]; then
        # Make psql work easily
        export PGHOST=db
        export PGUSER=postgres
        export PGPASSWORD=postgres
        export ENV=/etc/profile
    fi

    exec "$@"

elif [ "$RUN_HUEY" ]; then
    if [ -z "$HUEY_WORKERS" ]; then
        HUEY_WORKERS="$(python -c 'import multiprocessing as m; print(max(m.cpu_count() * 3, 6))')"
    fi

    wait_for_service db:5432 &
    wait_for_service redis:6379 &
    wait

    CMD="./manage.py run_huey --workers $HUEY_WORKERS --flush-locks"
    if [ "$DEBUG" ]; then
        exec watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- $CMD
    else
        exec $CMD
    fi

else
    wait_for_service db:5432 -- ./manage.py migrate &

    if [ "$DEBUG" -a ! -d '../frontend/node_modules' ]; then
        # In case /app is mounted in Docker, needed to re-install the /app/frontend/node_modules folder
        npm --prefix=../frontend install &
    fi

    if [ -z "$DEBUG" ]; then
        ./manage.py collectstatic --noinput &
    fi

    wait_for_service redis:6379 &

    # Wait on DB migrated, static collected, and redis up. Ready to start afterwards.
    wait

    # We can initialize the DB (fixtures) async
    init_db &

    if [ "$DEBUG" ]; then
        init_umami_debug_only &
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
                --access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
                --access-logfile - \
            jew_pizza.wsgi
    fi
fi
