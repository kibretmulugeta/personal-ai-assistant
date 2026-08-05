# Troubleshooting Guide

**Personal Website AI Assistant**

---

## 1. Common Issues & Solutions

### Issue 1: `ConnectionRefusedError` during PostgreSQL connection
- **Cause**: Database server is not running locally or DATABASE_URL string is incorrect.
- **Solution**:
  - Run `docker compose -f docker/docker-compose.yml up -d postgres`.
  - Check `.env` `DATABASE_URL` parameter (`postgresql+asyncpg://...`).

### Issue 2: `pgvector` extension error during migration
- **Cause**: Standard PostgreSQL image without pgvector installed.
- **Solution**: Use `pgvector/pgvector:pg16` image or enable `CREATE EXTENSION IF NOT EXISTS vector;` in Supabase.

### Issue 3: SSE Streaming cuts off prematurely in Nginx
- **Cause**: Nginx response buffering enabled.
- **Solution**: Add `proxy_buffering off;` and `proxy_read_timeout 600s;` in `docker/nginx.conf`.
