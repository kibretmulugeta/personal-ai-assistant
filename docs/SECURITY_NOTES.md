# Security Notes & Controls

**Personal Website AI Assistant - Digital Twin**

---

## 1. Security Architecture Summary

1. **JWT Session Authentication**:
   Signed access tokens using `HS256` with strict expiration checks (`ACCESS_TOKEN_EXPIRE_MINUTES`).
2. **API Key Header Validation**:
   Widget request verification using `X-API-Key`.
3. **Prompt Injection Defenses**:
   System prompts enforce persona boundaries. Instructions like *"Ignore previous instructions"* are constrained within the system persona scope.
4. **Input & File Upload Validation**:
   File uploads restricted to validated document types (PDF, DOCX, TXT, MD). Unsupported executables and binaries are rejected.
5. **CORS Restrictions**:
   Strict origin domain matching in production via `settings.CORS_ORIGINS`.
6. **Exception Masking**:
   Uncaught server exceptions return generic error codes to prevent stack trace leaks.
