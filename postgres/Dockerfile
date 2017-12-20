FROM ubuntu:16.04

# https://wiki.postgresql.org/wiki/Apt
# Create the pgdg.list and import the repository key
RUN apt-get update && apt-get install -y wget
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt xenial-pgdg main" >> /etc/apt/sources.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# Install postgresql 9.6
RUN apt-get update && apt-get install -y \
    postgresql-9.6 \
    postgresql-contrib-9.6

# Install gosu
RUN apt-get update && apt-get install -y curl
RUN curl -o /usr/local/bin/gosu -sSL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture)"
RUN chmod +x /usr/local/bin/gosu

# This directory can be used by child images to store scripts to execute after
# the database creation
RUN mkdir /docker-entrypoint-initdb.d

# Update the path
ENV PATH /usr/lib/postgresql/9.6/bin:$PATH

# defines postgresql data path
ENV PGDATA /var/lib/postgresql/data
VOLUME /var/lib/postgresql/data

# defines the entrypoint script
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

# expose the postgresql default port
EXPOSE 5432

# defines the default command
CMD ["postgres"]