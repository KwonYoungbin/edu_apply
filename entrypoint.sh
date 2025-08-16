#!/bin/sh

# DB가 준비될 때까지 대기
echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5
done

echo "PostgreSQL started"

# 마이그레이션 실행
python manage.py migrate --noinput

# 정적 파일 수집
python manage.py collectstatic --noinput

# 서버 실행 (gunicorn 사용)
gunicorn EduApply.wsgi:application --bind 0.0.0.0:8000
