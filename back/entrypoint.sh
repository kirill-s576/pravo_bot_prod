#!/bin/bash

cd /code/back
python manage.py migrate
python manage.py collectstatic --no-input
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --reload