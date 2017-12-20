#!/bin/bash
set -e

# At this point the database was created by the postgres image entrypoint, but
# the server is not yet running.
#
# As we can not create extension in single-user mode we have to start the
# server. (the -w option means "wait until operation completes")
gosu postgres pg_ctl start -w

# Enable PostGIS as describe here https://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS23UbuntuPGSQL96Apt

# enable PostGIS
gosu postgres psql -U postgres -c "CREATE EXTENSION adminpack"
gosu postgres psql -U postgres $PG_DB -c "CREATE SCHEMA postgis"
gosu postgres psql -U postgres $PG_DB -c "ALTER DATABASE $PG_DB SET search_path=public, postgis, contrib"
gosu postgres psql -U postgres $PG_DB -c "CREATE EXTENSION postgis SCHEMA postgis"

# enable pgRouting
gosu postgres psql -U postgres $PG_DB -c "CREATE EXTENSION pgrouting"

# enable Topology
gosu postgres psql -U postgres $PG_DB -c "CREATE EXTENSION postgis_topology"

# fuzzy matching needed for Tiger
gosu postgres psql -U postgres $PG_DB -c "CREATE EXTENSION fuzzystrmatch"

# Enable US Tiger Geocoder
gosu postgres psql -U postgres $PG_DB -c "CREATE EXTENSION postgis_tiger_geocoder"

# We stop the server, the postgres image entrypoint script will continue and
# will finish by starting it.
gosu postgres pg_ctl stop -w