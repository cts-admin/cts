#!/usr/bin/env bash

cat /media/ave/ae722e82-1476-4374-acd8-a8a18ef8ae7a/cts_dump-12-1.sql | docker exec -i cts_dev_con psql -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U postgres

