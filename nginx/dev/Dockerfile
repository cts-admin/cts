FROM nginx

ENV SERVER_NAME="dev.conservationtechnologysolutions.com www.dev.conservationtechnologysolutions.com"
ENV CRED_LOC=/.htpasswd

COPY config/ /etc/nginx/conf.d/

CMD /bin/bash -c "envsubst < /etc/nginx/conf.d/cts.template > /etc/nginx/conf.d/cts.conf && nginx -g 'daemon off;'"