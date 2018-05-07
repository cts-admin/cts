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
python manage.py loaddata $DB_DATA_FILE

# start slack bot
python manage.py sos_bot

# serve with gunicorn
gunicorn cts.wsgi:application -w 2 --timeout 120 -b :8000