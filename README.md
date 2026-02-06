# OneWave Backend 

AI 기반 취업 준비 플랫폼 - 포트폴리오 분석 & 면접 시뮬레이션 백엔드 API

## 프로젝트 소개

OneWave는 취업 준비생을 위한 AI 기반 커리어 코칭 플랫폼입니다.
사용자의 포트폴리오를 분석하고, 실전 같은 AI 면접 시뮬레이션을 제공하여 취업 성공률을 높입니다.

### 주요 기능

- **AI 포트폴리오 분석**: 사용자 프로젝트와 채용공고 매칭 분석
  - 스킬 매칭도 평가
  - 부족한 역량 식별
  - 맞춤형 교육 프로그램 추천

- **AI 면접 시뮬레이션**: 실전 같은 기술 면접 연습
  - 엄격한 면접관 에이전트 (심화 질문)
  - 따뜻한 멘토 에이전트 (피드백 & 팁)
  - 한국어 음성 TTS 지원

- **프로젝트 & 채용공고 관리**: 포트폴리오 및 채용 정보 CRUD
- **사용자 인증**: JWT 기반 안전한 인증 시스템

---

## 기술 스택

### Backend
- **FastAPI** - 고성능 비동기 웹 프레임워크
- **SQLModel** - SQL 데이터베이스 ORM (Pydantic + SQLAlchemy)
- **PostgreSQL** - 관계형 데이터베이스
- **Python 3.10+**

### AI & ML
- **Google Gemini 2.5 Flash** - LLM 기반 분석 & 대화 생성
- **Google Cloud Text-to-Speech** - 한국어 음성 합성

### Authentication & Security
- **JWT (python-jose)** - 토큰 기반 인증
- **Passlib + Bcrypt** - 비밀번호 해싱

### Infrastructure
- **Docker & Docker Compose** - 컨테이너화 배포
- **Uvicorn** - ASGI 서버 (8 workers)

---

## 빠른 시작

### 1. 사전 요구사항

- Docker & Docker Compose
- Google Cloud Platform 계정 (TTS API)
- Google AI Studio 계정 (Gemini API)

### 2. 설치 및 실행

```bash
# 1. 저장소 클론
git clone https://github.com/your-org/onewave-be.git
cd onewave-be

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 API 키 및 설정 입력

# 3. Google Cloud 서비스 계정 키 설정
# Google Cloud Console에서 TTS API용 서비스 계정 키 다운로드
# 프로젝트 루트에 service-account-key.json 저장

# 4. Docker Compose로 실행
docker-compose up --build -d

# 5. 로그 확인
docker-compose logs -f web
```

서버가 `http://localhost:8000`에서 실행됩니다.

### 3. API 문서 확인

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 환경 변수 설정

`.env` 파일에 다음 변수를 설정하세요:

```bash
# Database
POSTGRES_USER=onewave
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=onewave
DATABASE_URL=postgresql://onewave:your-secure-password@db:5432/onewave

# Security
SECRET_KEY=your-secret-key-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Gemini API (https://ai.google.dev/)
GEMINI_API_KEY=your-gemini-api-key

# Google Cloud TTS
GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json

# TTS Settings
TTS_VOICE_NAME=ko-KR-Wavenet-A
```

### API 키 발급 방법

**Gemini API:**
1. [Google AI Studio](https://ai.google.dev/) 접속
2. "Get API Key" 클릭
3. 생성된 키를 `GEMINI_API_KEY`에 입력

**Google Cloud TTS:**
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 프로젝트 생성 후 "Cloud Text-to-Speech API" 활성화
3. 서비스 계정 생성 및 JSON 키 다운로드
4. `service-account-key.json`으로 프로젝트 루트에 저장

---

##  API 엔드포인트

### 인증 (Authentication)

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/auth/signup` | 회원가입 |
| POST | `/auth/login` | 로그인 (JWT 토큰 발급) |

### 사용자 (Users)

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|----------|
| GET | `/users/me` | 현재 사용자 정보 조회 | ✅ |
| POST | `/users/survey` | 설문조사 제출 (도메인 설정) | ✅ |
| POST | `/users/portfolio` | 포트폴리오 정보 업데이트 | ✅ |

### 프로젝트 (Projects)

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|----------|
| POST | `/users/me/projects` | 프로젝트 생성 | ✅ |
| GET | `/users/me/projects` | 내 프로젝트 목록 조회 | ✅ |
| PUT | `/users/me/projects/{id}` | 프로젝트 수정 | ✅ |
| DELETE | `/users/me/projects/{id}` | 프로젝트 삭제 | ✅ |

### 채용공고 (Jobs)

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|----------|
| GET | `/jobs` | 채용공고 목록 조회 | ❌ |
| GET | `/jobs/{id}` | 채용공고 상세 조회 | ❌ |

### AI 분석 (Analysis)

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|----------|
| POST | `/analysis/portfolio` | AI 포트폴리오 분석 | ✅ |

**응답 예시:**
```json
{
  "skill_match": "지원자는 Python, FastAPI 스킬을 보유...",
  "fit_evaluation": "프로젝트 경험이 백엔드 개발 직무에 적합...",
  "missing_competencies": ["Kubernetes", "Redis"],
  "overall_score": 75,
  "recommended_programs": [...],
  "analyzed_project": "OneWave Backend API",
  "analyzed_job": "카카오뱅크 - 백엔드 개발자"
}
```

### AI 면접 (Interview)

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|----------|
| POST | `/interview/start` | 면접 시작 (인사말 + TTS) | ✅ |
| POST | `/interview/chat/interviewer` | 면접관 질문 생성 + TTS | ✅ |
| POST | `/interview/chat/mentor` | 멘토 피드백 생성 | ✅ |

**면접 플로우:**
```
1. /interview/start
   → 면접관 인사말 (텍스트 + 음성)

2. [사용자 답변]

3. /interview/chat/interviewer
   → 면접관 심화 질문 (텍스트 + 음성)

4. [사용자 답변]

5. /interview/chat/mentor
   → 멘토 피드백 & 개선 팁

6. 2-5 반복
```

---

## 프로젝트 구조

```
onewave-be/
├── app/
│   ├── api/
│   │   ├── deps.py              # 의존성 주입 (인증 등)
│   │   └── routes/
│   │       ├── auth.py          # 인증 라우트
│   │       ├── users.py         # 사용자 라우트
│   │       ├── jobs.py          # 채용공고 라우트
│   │       ├── analysis.py      # AI 분석 라우트
│   │       └── interview.py     # AI 면접 라우트
│   ├── core/
│   │   ├── config.py            # 설정 관리
│   │   ├── database.py          # DB 연결 (연결 풀 최적화)
│   │   └── security.py          # JWT 인증 로직
│   ├── models/
│   │   ├── user.py              # User 모델
│   │   ├── project.py           # Project 모델
│   │   └── job.py               # Job 모델
│   ├── schemas/
│   │   ├── user.py              # User 스키마
│   │   ├── project.py           # Project 스키마
│   │   ├── job.py               # Job 스키마
│   │   ├── analysis.py          # Analysis 응답 스키마
│   │   └── interview.py         # Interview 스키마
│   ├── services/
│   │   ├── llm_service.py       # Gemini LLM 서비스
│   │   └── tts_service.py       # Google TTS 서비스
│   ├── utils/
│   │   └── ai_analysis.py       # AI 포트폴리오 분석 로직
│   └── main.py                  # FastAPI 앱 진입점
├── dummy_data/
│   ├── job_dummy.json           # 채용공고 더미 데이터
│   └── program_dummy.json       # 교육 프로그램 더미 데이터
├── docker-compose.yml           # Docker Compose 설정
├── Dockerfile                   # Docker 이미지 빌드
├── pyproject.toml               # Python 의존성
├── initial_data.py              # DB 초기 데이터 로드
└── .env.example                 # 환경 변수 예시
```

---

## 🗄️ 데이터베이스 초기화

더미 데이터를 DB에 로드하려면:

```bash
# Docker 컨테이너 내에서 실행
docker-compose exec web python initial_data.py
```

이 명령은 `dummy_data/job_dummy.json`의 채용공고 데이터를 DB에 추가합니다.

---

## 개발 모드 실행

Docker 없이 로컬에서 개발하려면:

```bash
# 1. 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. 의존성 설치
pip install -e .

# 3. PostgreSQL 실행 (별도 설치 필요)
# 또는 Docker로 DB만 실행:
docker-compose up -d db

# 4. 환경 변수 설정
export DATABASE_URL=postgresql://onewave:onewave@localhost:5432/onewave
export GEMINI_API_KEY=your-key
# ... (기타 환경 변수)

# 5. 개발 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 성능 최적화

### 현재 최적화 상태

- **Uvicorn 8 Workers**: 동시 요청 처리 능력 향상
- **DB 연결 풀**: `pool_size=20`, `max_overflow=30` (총 50개 연결)
- **TTS 캐싱**: 중복 텍스트 음성 변환 방지
- **비동기 처리**: FastAPI async/await 패턴 활용

### 예상 성능 (OCI 24GB, 8코어 서버 기준)

- **동시 접속**: ~40-50명
- **평균 응답 시간**: 2-5초 (AI API 호출 포함)
- **최대 DB 연결**: 50개

**100명 이상 동시 접속을 위한 추가 최적화:**
- 비동기 HTTP 클라이언트 (httpx)
- Redis 캐싱
- Celery 백그라운드 작업 큐
- Rate Limiting (slowapi)

---

## 테스트

```bash
# 단위 테스트 실행 (TODO)
pytest

# API 엔드포인트 테스트
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

---

## 라이선스

MIT License

---

## 👥 팀

OneWave Team 15

---

## 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 문의

프로젝트에 대한 문의사항이 있으시면 Issues를 통해 연락주세요.
