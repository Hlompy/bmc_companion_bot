#!/bin/sh
python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn -b 0.0.0.0:8000 -w 4 config.wsgi:application
