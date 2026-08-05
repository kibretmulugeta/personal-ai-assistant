# Personal Website AI Assistant (Digital Twin)

**Standalone AI Assistant & Professional Digital Twin of Alemu Kibret Mulugeta**

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL pgvector](https://img.shields.io/badge/PostgreSQL-pgvector-336791.svg)](https://github.com/pgvector/pgvector)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Overview

The **Personal Website AI Assistant** is a production-ready, standalone AI service that functions as the professional digital twin of **Alemu Kibret Mulugeta** (AI Researcher, Machine Learning Engineer, Full-Stack Developer).

It is designed to be embedded into any personal portfolio website or Next.js application using a lightweight JavaScript floating widget (`widget.js`), providing interactive discussions about research, project explanations, resume downloads, contact submissions, and domain-specific RAG knowledge retrieval.

---

## 🏗️ System Architecture

```text
[Visitor on Portfolio Website]
              │
              ▼
[Embeddable Floating Widget (widget.js / React Component)]
              │
     Streaming SSE / WebSockets / REST APIs
              │
              ▼
[FastAPI Backend Service (apps/backend/app/main.py)]
              │
      JWT & X-API-Key Security Middleware
              │
              ▼
[Multi-Agent System Layer (packages/agents/)]
  ├── Router Agent (Intent Classifier: KNOWLEDGE | ACTION | GENERAL)
  ├── Knowledge Agent (RAG Context + Source Citation Assembly)
  └── Action Agent (Function Calling Tool Execution Engine)
          │                      │
          ▼                      ▼
[LLM Provider Adapter Layer]   [Tool Registry (packages/tools/)]
  (OpenAI, Gemini, Anthropic,     (download_resume, list_projects,
   Groq, OpenRouter, Ollama)       submit_contact_form, etc.)
          │
          ▼
[RAG & pgvector Store (packages/rag/ & packages/database/)]
  ├── Document Parsers (PDF, DOCX, TXT, MD, JSON, CSV)
  ├── Recursive Character Chunker
  ├── Embedding Factory (OpenAI & BGE/E5/SentenceTransformers)
  └── Async PostgreSQL + pgvector Vector Similarity Search (<=>)
```

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13+, FastAPI, SQLAlchemy 2.0 (Asyncio), Alembic, Pydantic v2, HTTPX, SSE (`StreamingResponse`), WebSockets.
- **Database**: Supabase / PostgreSQL 16 with `pgvector` extension, Redis.
- **AI Layer**: Provider-agnostic adapters for **OpenAI**, **Anthropic**, **Google Gemini**, **Groq**, **OpenRouter**, and **Ollama**.
- **Embedding Models**: Configurable embeddings (**OpenAI** `text-embedding-3-small` & **SentenceTransformers** BGE/E5).
- **Frontend Widget**: Vanilla JS script (`widget.js`), Vanilla CSS design system (`widget.css`), React component wrapper (`WebsiteAssistantWidget.jsx`).

---

## 🚀 Quick Start

### 1. Clone & Configure Environment
```bash
git clone https://github.com/alemukibret/personal-ai-assistant.git
cd personal-ai-assistant
cp .env.example .env
```

### 2. Start Services via Docker Compose
```bash
docker compose -f docker/docker-compose.yml up -d postgres redis
```

### 3. Run Alembic Database Migrations
```bash
python -m alembic -c packages/database/alembic.ini upgrade head
```

### 4. Start FastAPI Server
```bash
uvicorn apps.backend.app.main:app --reload --port 8000
```

### 5. Run Test Suite
```bash
python -m pytest -v
```

---

## 🔌 Embeddable Widget Integration

Add this snippet before `</body>` on your portfolio site:

```html
<script src="https://api.alemukibret.dev/widget.js"></script>
<script>
  WebsiteAssistant.init({
    apiKey: "your-widget-api-key",
    apiEndpoint: "https://api.alemukibret.dev/api/v1",
    theme: "dark",
    position: "bottom-right",
    primaryColor: "#6366f1"
  });
</script>
```

Or use the React wrapper component:
```jsx
import { WebsiteAssistantWidget } from './components/WebsiteAssistantWidget';

export default function App() {
  return <WebsiteAssistantWidget apiEndpoint="https://api.alemukibret.dev/api/v1" theme="dark" />;
}
```

---

## 📚 Documentation Directory

- [docs/ARCHITECTURE.md](file:///e:/Developer/Ml%20projects/Chat%20Platform/docs/ARCHITECTURE.md): System architecture and package design.
- [docs/API_DOCUMENTATION.md](file:///e:/Developer/Ml%20projects/Chat%20Platform/docs/API_DOCUMENTATION.md): Complete REST, SSE, and WebSocket API reference.
- [docs/DEPLOYMENT_GUIDE.md](file:///e:/Developer/Ml%20projects/Chat%20Platform/docs/DEPLOYMENT_GUIDE.md): Render, Supabase, Docker, and Nginx deployment guide.
- [docs/WIDGET_INTEGRATION_GUIDE.md](file:///e:/Developer/Ml%20projects/Chat%20Platform/docs/WIDGET_INTEGRATION_GUIDE.md): HTML and React widget integration manual.
- [docs/SECURITY_NOTES.md](file:///e:/Developer/Ml%20projects/Chat%20Platform/docs/SECURITY_NOTES.md): Security controls and prompt injection defenses.
- [docs/RAG_PIPELINE.md](file:///e:/Developer/Ml%20projects/Chat%20Platform/docs/RAG_PIPELINE.md): Ingestion, chunking, embeddings, and retrieval details.
- [docs/TROUBLESHOOTING_GUIDE.md](file:///e:/Developer/Ml%20projects/Chat%20Platform/docs/TROUBLESHOOTING_GUIDE.md): Troubleshooting common issues.
- [docs/PRODUCTION_RELEASE_REPORT.md](file:///e:/Developer/Ml%20projects/Chat%20Platform/docs/PRODUCTION_RELEASE_REPORT.md): Final production release audit report.
