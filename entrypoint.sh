#!/bin/sh

echo "Generating migrations..."
python manage.py makemigrations --noinput

echo "Waiting for database and applying migrations..."

# DB가 준비될 때까지 반복 시도
until python manage.py migrate --noinput; do
  echo "Database not ready yet. Waiting..."
  sleep 1
done

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn EduApply.wsgi:application --bind 0.0.0.0:8000
