#!/bin/sh

# 마이그레이션 실행
until python manage.py migrate --noinput; do
  echo "Waiting for database..."
  sleep 1
done

echo "DB ready"

# 정적 파일 수집
python manage.py collectstatic --noinput

# 서버 실행 (gunicorn 사용)
gunicorn EduApply.wsgi:application --bind 0.0.0.0:8000
