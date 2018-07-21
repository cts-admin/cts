FROM postgres:9.6

# Install PostGIS
RUN apt-get clean && apt-get update && apt-get install -y \
    postgresql-9.6-postgis-2.3 \
    postgresql-9.6-postgis-scripts \
    postgresql-9.6-pgrouting

# Add the initialization script
COPY init-postgis.sh /docker-entrypoint-initdb.d/