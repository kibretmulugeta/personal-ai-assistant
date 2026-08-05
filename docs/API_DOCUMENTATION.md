# API Reference Documentation

**Personal Website AI Assistant - Digital Twin API v1**

Base URL: `https://api.alemukibret.dev/api/v1`

---

## 1. Authentication Endpoints

### POST `/auth/token`
Generates a signed JWT access token for visitor chat sessions.

- **Request Body**:
  ```json
  {
    "session_id": "sess_12345678"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
    "token_type": "bearer",
    "expires_in_minutes": 1440
  }
  ```

---

## 2. Chat & Streaming Endpoints

### POST `/chat` / `/chat/message`
Standard REST chat completion endpoint.

- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "message": "Can I download your resume?",
    "session_id": "sess_12345678",
    "history": []
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "response": "You can download Alemu Kibret Mulugeta's professional resume below.",
    "route": "ACTION",
    "session_id": "sess_12345678",
    "action": {
      "action_name": "download_resume",
      "data": {
        "download_url": "/api/v1/assets/Alemu_Kibret_Resume.pdf",
        "filename": "Alemu_Kibret_Resume.pdf"
      }
    },
    "sources": [],
    "tokens_used": 25
  }
  ```

### GET `/chat/stream`
Server-Sent Events (SSE) token-by-token streaming endpoint.

- **Query Parameters**:
  - `message`: Visitor message string
  - `session_id`: Optional session ID
- **Response Stream**:
  ```text
  data: {"type": "metadata", "session_id": "sess_123", "route": "KNOWLEDGE"}

  data: {"type": "content", "delta": "Alemu "}

  data: {"type": "content", "delta": "holds an M.Sc."}

  data: {"type": "done"}
  ```

### WEBSOCKET `/chat/ws`
Real-time bidirectional WebSocket chat channel.

---

## 3. Contact & Document Ingestion Endpoints

### POST `/contact/submit`
Submits a contact inquiry to Alemu Kibret Mulugeta.

### POST `/documents/upload`
Uploads a document (PDF, DOCX, TXT, MD) into the `pgvector` knowledge base.

### GET `/documents`
Lists ingested knowledge base documents.
