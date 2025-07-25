#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
fi
uv run manage.py makemigrations levels
uv run manage.py makemigrations users
uv run manage.py migrate levels
uv run manage.py migrate users
uv run manage.py makemigrations
uv run manage.py migrate
uv run manage.py createcachetable
uv run manage.py collectstatic  --noinput
gunicorn --bind 0.0.0.0:8080 --workers 3 --threads 2 core.wsgi:application

exec "$@"