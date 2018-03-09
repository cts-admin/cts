#!/bin/sh

# wait for PSQL server to start
sleep 10

# prepare init migration
su -m myuser -c "python manage.py makemigrations"
# migrate db, so we have the latest db schema
su -m myuser -c "python manage.py migrate"

# collect static files
su -m myuser -c "python manage.py collectstatic --noinput"

# start development server on public ip interface, on port 8000
#su -m myuser -c "python manage.py runserver 0.0.0.0:8000"

# serve with gunicorn
su -m myuser -c "gunicorn cts.wsgi -b 0.0.0.0:8000"