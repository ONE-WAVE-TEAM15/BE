FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml .
# 의존성 먼저 설치 (캐싱 활용)
RUN uv pip install --system -r pyproject.toml

COPY . .

# 실행 (FastAPI 0.100+ 버전 기준)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]