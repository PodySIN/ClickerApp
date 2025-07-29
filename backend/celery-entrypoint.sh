#!/bin/sh

# Ждем, пока Django применит миграции
while ! uv run manage.py migrate --check; do
  echo "Waiting for migrations to be applied..."
  sleep 5
done

exec celery -A core worker --beat --loglevel=info