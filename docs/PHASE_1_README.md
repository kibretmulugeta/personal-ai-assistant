# Phase 1: Core Foundation & Infrastructure Documentation

**Digital Twin AI Assistant for Alemu Kibret Mulugeta**

---

## 1. Executive Summary

Phase 1 establishes the baseline production foundation for the personal digital twin AI assistant. It provides a modular monorepo structure, asynchronous database engine (`postgresql+asyncpg`), `pgvector` vector store initialization, Alembic schema migrations, Pydantic v2 configuration management, generic async repositories, structured logging, health check endpoints, and Docker containerization.

---

## 2. Directory Architecture

```text
personal-ai-assistant/
├── apps/
│   └── backend/
│       ├── app/
│       │   ├── api/
│       │   │   ├── v1/
│       │   │   │   └── health.py          # /health, /liveness, /readiness
│       │   │   └── router.py              # API v1 Router Aggregator
│       │   ├── core/
│       │   │   ├── config.py              # Pydantic Settings & Env Validation
│       │   │   └── logging.py             # Structured JSON Logging
│       │   └── main.py                    # FastAPI Application Entrypoint
│       └── requirements.txt               # Backend Python Dependencies
├── packages/
│   ├── database/
│   │   ├── migrations/                    # Alembic Schema Migrations
│   │   │   └── versions/
│   │   │       └── 001_initial_schema.py # Initial Vector & Entity Migration
│   │   ├── models/                        # Declarative SQLAlchemy 2.0 Models
│   │   │   ├── base.py                    # UUID & Timestamp Base Model
│   │   │   ├── conversation.py            # Conversation & Message Models
│   │   │   ├── document.py                # Document & DocumentChunk (pgvector)
│   │   │   └── contact.py                 # ContactSubmission Model
│   │   ├── repositories/                  # Async Repository Pattern
│   │   │   ├── base.py                    # Generic CRUD BaseRepository
│   │   │   ├── conversation_repo.py
│   │   │   ├── message_repo.py
│   │   │   ├── document_repo.py           # Vector similarity search (<=>)
│   │   │   └── contact_repo.py
│   │   ├── session.py                     # Async Engine & Sessionmaker
│   │   └── alembic.ini                    # Migration Configuration
│   └── shared/
│       ├── exceptions.py                  # Domain Exception Hierarchy
│       └── schemas/                       # Shared Pydantic API Schemas
├── docker/
│   ├── Dockerfile                         # Python 3.13 Multi-Stage Dockerfile
│   └── docker-compose.yml                 # Postgres (pgvector), Redis, Backend
├── scripts/
│   └── init_db.py                         # Database initialization utility
├── tests/
│   ├── conftest.py                        # Pytest Async Fixtures
│   └── test_health.py                     # Health Endpoints Test Suite
├── .env.example                           # Environment configuration template
└── pyproject.toml                         # Project metadata and tooling config
```

---

## 3. Key Infrastructure Components

### 3.1 Configuration Management (`apps/backend/app/core/config.py`)
Configuration is managed via Pydantic v2 `BaseSettings`. Environment variables from `.env` are automatically validated with strong typing. Supported active providers (OpenAI, Anthropic, Gemini, Groq, OpenRouter, Ollama) can be swapped by changing configuration settings without altering business logic code.

### 3.2 Database Engine & Models (`packages/database/`)
- **Engine**: Async SQLAlchemy 2.0 with `asyncpg` driver.
- **pgvector**: Enabled via raw SQL extension and integrated into SQLAlchemy using `pgvector.sqlalchemy.Vector(1536)`.
- **Models**:
  - `Conversation` & `Message`: Session memory and conversation history tracking.
  - `Document` & `DocumentChunk`: Knowledge base storage with vector embeddings.
  - `ContactSubmission`: Inquiries sent by portfolio visitors.

### 3.3 Async Repository Pattern (`packages/database/repositories/`)
- `BaseRepository[T]`: Provides generic asynchronous CRUD helpers (`get_by_id`, `list_all`, `create`, `update`, `delete`).
- `DocumentChunkRepository.search_similar_chunks()`: Executes cosine similarity search using the `pgvector` `<=>` distance operator.

### 3.4 Health Monitoring (`apps/backend/app/api/v1/health.py`)
- **GET `/api/v1/health`**: Comprehensive health status reporting database and redis connectivity.
- **GET `/api/v1/health/liveness`**: Process liveness probe.
- **GET `/api/v1/health/readiness`**: Dependency readiness probe (`SELECT 1` ping).

---

## 4. Setup & Running Instructions

### Local Development Setup
1. **Copy Environment Variables**:
   ```bash
   cp .env.example .env
   ```

2. **Run Docker Containers (PostgreSQL pgvector & Redis)**:
   ```bash
   docker compose -f docker/docker-compose.yml up -d postgres redis
   ```

3. **Run Alembic Database Migrations**:
   ```bash
   python -m alembic -c packages/database/alembic.ini upgrade head
   ```

4. **Start Backend Server**:
   ```bash
   uvicorn apps.backend.app.main:app --reload --port 8000
   ```

5. **Run Test Suite**:
   ```bash
   pytest
   ```
