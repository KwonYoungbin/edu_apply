# 📝 시험 응시 및 수업 수강 신청 시스템

이 프로젝트는 사용자가 온라인으로 **시험 응시**와 **수업 수강 신청**을 할 수 있는 웹 애플리케이션입니다.  
Django를 기반으로 구현되었으며, PostgreSQL 데이터베이스를 사용합니다.

---

## 📌 기술 스택

- **언어**: Python 3.13.x
- **프레임워크**: Django 5.2.5
- **데이터베이스**: PostgreSQL 14.xx

---

## 📑 API 명세서
### 1. 로컬 서버 실행 후 접근
- http://localhost:8000/swagger/
- http://127.0.0.1:8000/swagger/

### 2. API 호출
- 회원가입(/signup) -> 로그인(/login) 호출
- 로그인 응답값의 access값을 화면 상단의 Authorize 버튼 클릭 하여 입력
   - <span style="color:#fff5b1">**토큰 값 입력시에는 앞에 "Bearer " 입력 필요**</span>
   - <span style="color:#fff5b1">**토큰 유효 시간: 1시간**</span>

---

## 🚀 주요 기능

1. **사용자 인증 및 권한**
   - 회원 가입(POST /signup)
   - 로그인(POST /login)
   
2. **시험 관리**
   - 시험 목록 조회(GET /tests)
   - 시험 응시 신청(POST /tests/:id/apply)
   - 시험 응시 완료(POST /tests/:id/complete)

3. **수업 관리**
   - 수업 목록 조회(GET /courses)
   - 수업 수강 신청(POST /courses/:id/enroll)
   - 수업 수강 완료(POST /courses/:id/complete)

4. **결제**
   - 결제 내역 조회(GET /me/payments)
   - 결제 취소(POST /payments/:id/cancel)
   - 수업/시험 동시 결제(POST /bulk/payment/apply)

---

## ⚙️ 초기 환경 설정 (Mac OS, Linux)

### Homebrew 설치(미설치된 경우만)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Docker-compose 설치
```bash
brew install docker-compose
```

### Docker 설치
```bash
https://www.docker.com -> 접속 후 Docker 설치
```

---

## 💻 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/KwonYoungbin/edu_apply.git
```

### 2. 서비스 실행(Docker Container)
```bash
cd edu_apply
docker-compose up --build
```

### 3. 초기 데이터 추가
```bash
# =========================================
# 3. 초기 데이터 추가 (Mac OS Terminal 기준)
# =========================================

# 0. PostgreSQL 설치 (설치되지 않은 경우)
brew install postgresql

# 1. PostgreSQL 접속
# - Host: localhost
# - Port: 5433
# - User: root
# - Database: edu_apply
# - Password: 1234
psql -h localhost -p 5433 -U root -d edu_apply

# 2. 초기 데이터 SQL 파일 적용
[init_data.sql 보기](init_data.sql)
# psql 접속 후 아래 명령으로 실행 가능
# \i init_data.sql

# =========================================
# pgAdmin4 사용 시
# =========================================
# 1. pgAdmin 설치: https://www.pgadmin.org/download
# 2. Servers -> Register -> Server 클릭
#    Name: 자유롭게 입력
#    Host name/address: localhost
#    Port: 5433
#    Maintenance DB: edu_apply
#    Username: root
#    Password: 1234
# 3. pgAdmin에서 init_data.sql 실행
```