#!/usr/bin/env bash

/home/ave/venv/cts/bin/gunicorn --bind 0.0.0.0:8000 cts.wsgi:application