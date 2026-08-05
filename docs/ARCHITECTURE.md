# Architecture Documentation

**Personal Website AI Assistant (Digital Twin of Alemu Kibret Mulugeta)**

---

## 1. High-Level Architecture Overview

The system follows a strict **Clean Architecture** model organized into an asynchronous FastAPI backend application, a shared core utility package, database persistence layer with `pgvector`, an abstract LLM adapter layer, a multi-agent system, a RAG pipeline, a function calling tool registry, and an embeddable frontend widget.

```text
personal-ai-assistant/
├── apps/
│   ├── backend/                           # FastAPI Service
│   └── widget/                            # Standalone Widget & React Wrapper
├── packages/
│   ├── agents/                            # Multi-Agent Layer (Router, Knowledge, Action)
│   ├── auth/                              # JWT & API Key Security
│   ├── database/                          # Async SQLAlchemy 2.0 & pgvector
│   ├── llm/                               # Provider Adapters (OpenAI, Gemini, etc.)
│   ├── prompts/                           # Persona & System Prompts
│   ├── rag/                               # Ingestion, Chunking, Embeddings, Retrieval
│   ├── shared/                            # Schemas & Domain Exceptions
│   └── tools/                             # Function Calling Tools Registry
├── docker/                                # Dockerfile & docker-compose.yml & Nginx
├── docs/                                  # Production Documentation
├── scripts/                               # DB utilities
├── tests/                                 # Pytest Test Suite
└── render.yaml                            # Render.com IaC Blueprint
```

---

## 2. Component Design Principles

### 2.1 Provider Agnosticism
All LLM models are wrapped behind `BaseLLMAdapter`. Switching active LLM provider (OpenAI, Anthropic, Gemini, Groq, OpenRouter, Ollama) requires only changing `ACTIVE_LLM_PROVIDER` in `.env`.

### 2.2 Async-First Execution
All I/O operations (database access, API HTTP requests, SSE streaming, WebSockets) execute asynchronously using Python `asyncio` and `asyncpg`.

### 2.3 Layer Decoupling
Business logic is completely isolated from FastAPI route handlers. Route handlers delegate intent classification and execution directly to the Multi-Agent System (`RouterAgent`, `KnowledgeAgent`, `ActionAgent`).
