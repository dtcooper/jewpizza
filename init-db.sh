#!/bin/sh

# Initialize postgres DB for umami (mounts automatically to postgres container)

set -e

UMAMI_SQL_URL='https://raw.githubusercontent.com/mikecao/umami/9b1a75fd9/sql/schema.postgresql.sql'

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<EOSQL
    CREATE DATABASE umami;
    GRANT ALL PRIVILEGES ON DATABASE umami TO $POSTGRES_USER;
EOSQL

# Still insecure, should be changed
wget -qO - "$UMAMI_SQL_URL" | psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname umami
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname umami <<'EOSQL'
    UPDATE account SET username = 'dave', password = '$2a$10$YS9D7OL81EBXBe4DzS6mEOsVR6lfz/QpMTx83IWaxZYc725VDA/HK';
EOSQL
