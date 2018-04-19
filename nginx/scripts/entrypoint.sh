# Credit to Elliot Saba <staticfloat@gmail.com>
# https://github.com/staticfloat/docker-nginx-certbot/blob/master/scripts/entrypoint.sh
#!/bin/sh

# Create our config file from the template
envsubst < /etc/nginx/conf.d/cts.template > /etc/nginx/conf.d/cts.conf

# When we get killed, kill all our children
trap "exit" INT TERM
trap "kill 0" EXIT

# Source in util.sh so we can have our nice tools
. $(cd $(dirname $0); pwd)/util.sh

# Immediately run auto_enable_configs so that nginx is in a runnable state
auto_enable_configs

# Start up nginx, save PID so we can reload config inside of run_certbot.sh
nginx -g "daemon off;" &
export NGINX_PID=$!

# Next, run certbot to request all the ssl certs we can find
/scripts/run_certbot.sh

# Lastly, run startup scripts
for f in /scripts/startup/*.sh; do
    if [[ -x "$f" ]]; then
        echo "Running startup script $f"
        $f
    fi
done

# Create proper permissions for static files served by nginx
chown -R $USER:www-data /home/media
chown -R $USER:www-data /home/static

echo "Done with startup"

# Run `cron -f &` so that it's a background job owned by bash and then `wait`.
# This allows SIGINT (e.g. CTRL-C) to kill cron gracefully, due to our `trap`.
cron -f &
wait "$NGINX_PID"