#!/usr/bin/env bash

cd /usr/src/app/

python manage.py migrate
gunicorn PulaDemo.wsgi -w 4 -b 0.0.0.0:8000
# python manage.py runserver 0.0.0.0:8000