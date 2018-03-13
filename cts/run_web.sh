#!/bin/sh

# wait for PSQL server to start
sleep 10

# prepare init migration
su -m myuser -c "python manage.py makemigrations"
# migrate db, so we have the latest db schema
su -m myuser -c "python manage.py migrate"

# collect static files
su -m myuser -c "python manage.py collectstatic --noinput"

# serve with gunicorn
su -m myuser -c "gunicorn cts.wsgi:application -w 2 -b :8000"