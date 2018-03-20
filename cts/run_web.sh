#!/bin/sh

# wait for PSQL server to start
sleep 10

# prepare init migration
python manage.py makemigrations

# migrate db, so we have the latest db schema
python manage.py migrate

# collect static files
python manage.py collectstatic --noinput

# Delete the initial wagtail welcome page
python clear_wagtail_data.py

# load default database data
python manage.py loaddata np-nf_no-auth_no-contenttypes.json

# serve with gunicorn
gunicorn cts.wsgi:application -w 2 -b :8000