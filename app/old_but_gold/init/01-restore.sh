#!/bin/bash
set -e

echo "Recreating database..."

psql -U postgres -d postgres <<-EOSQL
DROP DATABASE IF EXISTS geo_admin;
CREATE DATABASE geo_admin;
EOSQL

echo "Importing dump..."
psql -U postgres -d geo_admin -f /docker-entrypoint-initdb.d/moj_dump.ignore

echo "Database ready."