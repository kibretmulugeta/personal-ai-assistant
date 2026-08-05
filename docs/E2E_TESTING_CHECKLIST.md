# End-to-End Testing & Verification Checklist

**Personal Website AI Assistant - Digital Twin of Alemu Kibret Mulugeta**

---

## 1. Backend Infrastructure & Health Checks

- [ ] **Liveness Probe**: `GET /api/v1/health/liveness` returns status 200 `{"status": "alive"}`.
- [ ] **Readiness Probe**: `GET /api/v1/health/readiness` verifies database ping `SELECT 1`.
- [ ] **Aggregate Health**: `GET /api/v1/health` returns status of database and Redis.
- [ ] **OpenAPI / Swagger UI**: `GET /api/v1/docs` loads OpenAPI documentation cleanly.

---

## 2. Intent Routing & Multi-Agent Classification

- [ ] **Resume Intent**: Query `"Can I download your resume?"` routes to `ACTION` with `action_name="download_resume"`.
- [ ] **Contact Intent**: Query `"How can I contact Alemu?"` routes to `ACTION` with `action_name="submit_contact_form"`.
- [ ] **Projects Intent**: Query `"What projects has Alemu built?"` routes to `ACTION` with `action_name="list_projects"`.
- [ ] **Knowledge Intent**: Query `"Tell me about your M.Sc. research on U-Net stroke segmentation"` routes to `KNOWLEDGE` route.

---

## 3. RAG Document Ingestion & Retrieval

- [ ] **PDF Ingestion**: `POST /api/v1/documents/upload` successfully parses PDF binary, extracts pages, chunks text, generates embeddings, and saves into `pgvector`.
- [ ] **DOCX Ingestion**: Uploads `.docx` file and creates document record.
- [ ] **Duplicate Detection**: Uploading identical file returns existing document record based on SHA256 checksum.
- [ ] **Source Attribution**: Chat responses derived from retrieved documents include source citations (filename, chunk index, similarity score).

---

## 4. REST, SSE Streaming & WebSockets

- [ ] **REST Message**: `POST /api/v1/chat/message` returns full `ChatResponse`.
- [ ] **SSE Streaming**: `GET /api/v1/chat/stream?message=...` streams token chunks (`data: {"type": "content", "delta": "..."}`).
- [ ] **WebSocket Real-Time**: `WEBSOCKET /api/v1/chat/ws` establishes bidirectional streaming connection.

---

## 5. Embeddable Widget UI & Functionality

- [ ] **Widget Initialization**: `WebsiteAssistant.init()` mounts floating toggle button on bottom-right of host page.
- [ ] **Toggle & Expand**: Clicking floating button opens animated glassmorphic chat window.
- [ ] **Dark / Light Mode**: Clicking theme button toggles between dark (`#0f172a`) and light (`#ffffff`) theme.
- [ ] **Reset Session**: Clicking reset button clears chat window and starts new visitor session.
- [ ] **Code Syntax Highlighting**: Fenced code blocks (` ```python ...``` `) render with copy-to-clipboard button.
- [ ] **Resume Download Card**: Action card displays clickable download link for `Alemu_Kibret_Resume.pdf`.
