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
   - ** 태그 기반 수업 추천(GET /courses/recommend) **

4. **결제**
   - 결제 내역 조회(GET /me/payments)
   - 결제 취소(POST /payments/:id/cancel)
   - ** 수업/시험 동시 결제(POST /bulk/payment/apply) **

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
cd edu_apply
```

### 2. 초기 데이터 추가
```bash
# # ========================================================
# 0. Tag값 추가 (정적 데이터 20개) - 반드시 먼저 수행
# # ========================================================
python manage.py loaddata apps/courses/tags.json

# #  =======================================================
# 1. Test, Course 초기 데이터(각 15,000개) 입력 - 아래 두 방식 중 택1 
#  ⚠️ Courses 초기 데이터 입력시, 각 row별 Tag 매핑으로 인해 약간의 지연 발생 
# # ========================================================

# 명령어 한번에 Test, Course 초기 데이터 (각 15,000개) Insert
bash apps/seed.sh

# 각각 명령어로 Test, Course 초기 데이터 (각 15,000개) Insert
python manage.py seed_courses
python manage.py seed_tests
```

### 3. 서비스 실행
```bash
docker-compose up --build
```