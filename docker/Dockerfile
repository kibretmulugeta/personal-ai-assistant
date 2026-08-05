# Multi-stage Dockerfile for Python 3.13 FastAPI Backend
FROM python:3.13-slim AS builder

WORKDIR /app

# Install build essentials for C extensions (e.g. asyncpg, hiredis)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt apps/backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final runtime image
FROM python:3.13-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project files
COPY pyproject.toml .
COPY .env.example .env
COPY packages ./packages
COPY apps ./apps
COPY scripts ./scripts

# Set Python path
ENV PYTHONPATH="/app/apps/backend:/app/packages/shared:/app/packages/database:${PYTHONPATH}"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health/liveness || exit 1

CMD ["uvicorn", "apps.backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
