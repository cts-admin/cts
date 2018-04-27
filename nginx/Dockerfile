# Much taken from Elliot Saba <staticfloat@gmail.com>
# https://github.com/staticfloat/docker-nginx-certbot/blob/master/Dockerfile

FROM nginx

ENV CRED_LOC=/.htpasswd
ENV CERTBOT_EMAIL=ctsadmin@conservationtechnologysolutions.org

VOLUME /etc/letsencrypt
EXPOSE 80
EXPOSE 443

# Do this apt/pip stuff all in one RUN command to avoid creating large
# intermediate layers on non-squashable docker installs
RUN apt update && \
    apt install -y cron python python-dev libffi6 libffi-dev libssl-dev curl build-essential && \
    curl -L 'https://bootstrap.pypa.io/get-pip.py' | python && \
    pip install -U cffi certbot && \
    apt remove --purge -y python-dev build-essential libffi-dev libssl-dev curl && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy in cron job and scripts for certbot
COPY crontab /etc/cron.d/certbot
RUN crontab /etc/cron.d/certbot
COPY scripts /scripts
RUN chmod +x /scripts/*.sh

# Add /scripts/startup directory to source more startup scripts
RUN mkdir -p /scripts/startup

# Copy in default nginx configuration (which just forwards ACME requests to
# certbot, or redirects to HTTPS, but has no HTTPS configurations by default).
RUN rm -f /etc/nginx/conf.d/*
COPY config /etc/nginx/conf.d/

ENTRYPOINT []
CMD ["/bin/bash", "/scripts/entrypoint.sh"]