#!/usr/bin/env sh

python manage.py makemigrations
python manage.py migrate --noinput
python manage.py initadmin
python manage.py loaddata products.json
python manage.py collectstatic --noinput
cp -r /app/static/. /backend_static/static/

gunicorn --bind 0.0.0.0:8888 store.wsgi 