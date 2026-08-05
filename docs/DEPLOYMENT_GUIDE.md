# Production Deployment Guide

**Personal Website AI Assistant - Digital Twin of Alemu Kibret Mulugeta**

---

## 1. Overview

This document provides step-by-step instructions for deploying the standalone Digital Twin AI Assistant backend service, PostgreSQL database with `pgvector`, Redis caching layer, and the embeddable frontend widget.

---

## 2. Option A: Render Cloud Deployment (Recommended)

1. **Push Code to GitHub**:
   Ensure your repository is pushed to your GitHub account.

2. **Connect Repository to Render**:
   - Log in to [Render.com](https://render.com).
   - Click **New +** -> **Blueprint**.
   - Connect your GitHub repository containing `render.yaml`.
   - Render will automatically provision:
     - PostgreSQL database (`digital-twin-db`) with `pgvector` enabled.
     - Redis cache instance (`digital-twin-redis`).
     - FastAPI Web Service (`digital-twin-backend`).

3. **Configure Environment Variables**:
   In the Render Web Service settings, add your active provider API key (e.g. `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`).

4. **Run Database Migrations**:
   Execute Alembic migration against the production database connection string:
   ```bash
   python -m alembic -c packages/database/alembic.ini upgrade head
   ```

---

## 3. Option B: Docker Compose Production Deployment

1. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in secrets:
   ```bash
   cp .env.example .env
   ```

2. **Build and Start Container Cluster**:
   ```bash
   docker compose -f docker/docker-compose.yml up -d --build
   ```

3. **Apply Database Schema Migrations**:
   ```bash
   docker compose -f docker/docker-compose.yml exec backend python -m alembic -c packages/database/alembic.ini upgrade head
   ```

4. **Setup Nginx Reverse Proxy & SSL**:
   Use the provided [docker/nginx.conf](file:///e:/Developer/Ml%20projects/Chat%20Platform/docker/nginx.conf) with Let's Encrypt Certbot SSL certificate.

---

## 4. Frontend Widget Embed Instructions

To embed the assistant into any portfolio website or Next.js app:

### Standard HTML Script Embedding
Add the following snippet right before `</body>`:

```html
<script src="https://api.alemukibret.dev/widget.js"></script>
<script>
  WebsiteAssistant.init({
    apiKey: "your-widget-api-key",
    apiEndpoint: "https://api.alemukibret.dev/api/v1",
    theme: "dark", // "dark" | "light"
    position: "bottom-right", // "bottom-right" | "bottom-left"
    primaryColor: "#6366f1",
    welcomeMessage: "Hello! I am the AI Digital Twin of Alemu Kibret Mulugeta. Ask me about Alemu's research, projects, or download his resume!"
  });
</script>
```

### React / Next.js Component Embedding

```jsx
import { WebsiteAssistantWidget } from './components/WebsiteAssistantWidget';

export default function PortfolioPage() {
  return (
    <div>
      {/* Portfolio Content */}
      <WebsiteAssistantWidget 
        apiEndpoint="https://api.alemukibret.dev/api/v1"
        theme="dark"
        position="bottom-right"
      />
    </div>
  );
}
```
