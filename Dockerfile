# Python base image
FROM python:3.13-slim

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리 생성
WORKDIR /app

# 시스템 패키지 업데이트 및 psycopg2 설치를 위한 라이브러리 추가
RUN apt-get update \
    && apt-get install -y gcc libpq-dev netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 소스 복사
COPY . /app/

# entrypoint.sh 복사
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 엔트리포인트 설정
ENTRYPOINT ["sh", "/app/entrypoint.sh"]