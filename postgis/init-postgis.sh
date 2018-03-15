#!/bin/bash
set -e

# Enable PostGIS as describe here https://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS23UbuntuPGSQL96Apt

# enable PostGIS
psql -U postgres -c "CREATE EXTENSION adminpack"
psql -U postgres $POSTGRES_DB -c "CREATE SCHEMA postgis"
psql -U postgres $POSTGRES_DB -c "ALTER DATABASE $POSTGRES_DB SET search_path=public, postgis, contrib"
psql -U postgres $POSTGRES_DB -c "CREATE EXTENSION postgis SCHEMA postgis"

# enable pgRouting
psql -U postgres $POSTGRES_DB -c "CREATE EXTENSION pgrouting"

# enable Topology
psql -U postgres $POSTGRES_DB -c "CREATE EXTENSION postgis_topology"

# fuzzy matching needed for Tiger
psql -U postgres $POSTGRES_DB -c "CREATE EXTENSION fuzzystrmatch"

# Enable US Tiger Geocoder
psql -U postgres $POSTGRES_DB -c "CREATE EXTENSION postgis_tiger_geocoder"
