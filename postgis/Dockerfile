FROM postgres:10

# Install PostGIS
RUN apt-get clean && apt-get update && apt-get install -y \
    postgresql-10-postgis-2.4 \
    postgresql-10-postgis-2.4-scripts \
    postgresql-10-pgrouting

# Add the initialization script
COPY init-postgis.sh /docker-entrypoint-initdb.d/