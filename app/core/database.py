from sqlmodel import create_engine, Session

from app.core.config import DATABASE_URL

# DB 연결 풀 설정 (100명 동시 접속 대비)
engine = create_engine(
    DATABASE_URL,
    echo=False,  # 프로덕션에서는 로그 off (성능 향상)
    pool_size=20,  # 기본 커넥션 풀 크기
    max_overflow=30,  # 추가 가능한 최대 연결 수
    pool_pre_ping=True,  # 연결 유효성 자동 체크
    pool_recycle=3600,  # 1시간마다 연결 재생성 (MySQL timeout 방지)
)


def get_session():
    with Session(engine) as session:
        yield session
