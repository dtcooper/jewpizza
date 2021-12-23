#!/usr/bin/env bash

if [ ! -f /.dockerenv ]; then
    echo 'Must run in docker container'
    exit 1
fi

cd "$(dirname "$0")/.."

grep_quote () {
    sed 's/[^\^]/[&]/g;s/[\^]/\\&/g' <<< "$*"
}

compare () {
    NAME="$1"
    LOCAL="$2"
    UPSTREAM="$3"
    FUZZY="$4"
    OP='='
    UP_TO_DATE=1

    if [ -z "$FUZZY" ]; then
        if [ "$UPSTREAM" != "$LOCAL" ]; then
            OP='!='
            UP_TO_DATE=
        fi
    else
        if echo "$UPSTREAM" | grep -q "^$(grep_quote "$LOCAL")"; then
            OP='^='
        else
            OP='!^='
            UP_TO_DATE=
        fi
    fi

    VERS="$LOCAL (local) $OP $UPSTREAM (remote)"

    if [ -z "$UP_TO_DATE" ]; then
        # Red
        echo -e "\x1B[91m${NAME} needs updating! ${VERS}\x1B[0m"
    else
        # Green
        echo -e "\x1B[92m${NAME} up to date.\x1B[0m $VERS"
    fi
}

if [ -z "$GITHUB_API_TOKEN" ]; then
    echo -e "\x1B[91mWarning: GITHUB_API_TOKEN not set\x1B[0m"
fi

POSTGRES_LOCAL="$(yq -r .services.db.image docker-compose.yml | sed 's/^library\/postgres:\(.*\)-alpine/\1/')"
POSTGRES_UPSTREAM="$(lastversion postgres/postgres)"
compare PostgreSQL "$POSTGRES_LOCAL" "$POSTGRES_UPSTREAM" 1

REDIS_LOCAL="$(yq -r .services.redis.image docker-compose.yml | sed 's/^library\/redis:\(.*\)-alpine/\1/')"
REDIS_UPSTREAM="$(lastversion redis/redis)"
compare Redis "$REDIS_LOCAL" "$REDIS_UPSTREAM" 1

LIQUIDSOAP_LOCAL="$(grep '^FROM ' radio/Dockerfile | sed 's/^FROM savonet\/liquidsoap:v\([0-9.]*\).*/\1/')"
LIQUIDSOAP_UPSTREAM="$(lastversion savonet/liquidsoap)"
compare Liquidsoap "$LIQUIDSOAP_LOCAL" "$LIQUIDSOAP_UPSTREAM"

DOZZLE_LOCAL="$(yq -r .services.logs.image docker-compose.yml | sed 's/^amir20\/dozzle:v//')"
DOZZLE_UPSTREAM="$(lastversion amir20/dozzle)"
compare Dozzle "$DOZZLE_LOCAL" "$DOZZLE_UPSTREAM"

UMAMI_LOCAL="$(yq -r .services.umami.image docker-compose.yml | sed 's/^ghcr.io\/mikecao\/umami:postgresql-\(.*\)/\1/')"
UMAMI_TAG="$(curl -s --user "dtcooper:$GITHUB_API_TOKEN" https://api.github.com/repos/mikecao/umami/releases/latest | jq -r .tag_name)"
UMAMI_UPSTREAM="$(curl -s --user "dtcooper:$GITHUB_API_TOKEN" "https://api.github.com/repos/mikecao/umami/git/ref/tags/$UMAMI_TAG" | jq -r .object.sha)"
compare Umami "$UMAMI_LOCAL" "$UMAMI_UPSTREAM" 1

POETRY_LOCAL="$(fgrep 'POETRY_VERSION=' backend/Dockerfile | sed 's/.*POETRY_VERSION=\([0-9.]*\).*/\1/')"
POETRY_UPSTREAM="$(lastversion python-poetry/poetry)"
compare Poetry "$POETRY_LOCAL" "$POETRY_UPSTREAM"

COMPOSE_LOCAL="$(fgrep 'COMPOSE_VERSION=' Dockerfile.controller | sed 's/.*COMPOSE_VERSION=\([0-9.]*\).*/\1/')"
COMPOSE_UPSTREAM="$(lastversion docker/compose)"
compare Compose "$COMPOSE_LOCAL" "$COMPOSE_UPSTREAM"

WAIT_FOR_IT_LOCAL="$(fgrep 'WAIT_FOR_IT_VERSION=' backend/Dockerfile | sed 's/.*WAIT_FOR_IT_VERSION=\([0-9a-z]*\).*/\1/')"
WAIT_FOR_IT_DEFAULT_BRANCH="$(curl -s --user "dtcooper:$GITHUB_API_TOKEN" https://api.github.com/repos/vishnubob/wait-for-it | jq -r .default_branch)"
WAIT_FOR_IT_UPSTREAM="$(curl -s --user "dtcooper:$GITHUB_API_TOKEN" "https://api.github.com/repos/vishnubob/wait-for-it/commits/$WAIT_FOR_IT_DEFAULT_BRANCH" | jq -r .sha)"
compare 'wait-for-it' "$WAIT_FOR_IT_LOCAL" "$WAIT_FOR_IT_UPSTREAM" 1
