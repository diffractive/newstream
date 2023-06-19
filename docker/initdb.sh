#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER localpaypal WITH ENCRYPTED PASSWORD 'localpaypal' CREATEDB;
    CREATE DATABASE localpaypal OWNER localpaypal;
    GRANT ALL PRIVILEGES ON DATABASE localpaypal TO localpaypal;
EOSQL

PGPASSWORD=localpaypal psql --username localpaypal --dbname localpaypal < /schema.sql