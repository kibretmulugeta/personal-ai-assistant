import os
import sys

# Add repository root directory to Python path for Vercel serverless function execution
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
os.environ["PYTHONPATH"] = ROOT_DIR

from apps.backend.app.main import app as raw_app


class VercelPathRewriteMiddleware:
    """ASGI Middleware normalizing incoming request path on Vercel serverless deployments."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] in ("http", "websocket"):
            headers = {k.lower(): v for k, v in scope.get("headers", [])}
            forwarded_uri = headers.get(b"x-forwarded-uri")
            if forwarded_uri:
                path = forwarded_uri.decode("utf-8").split("?")[0]
                scope["path"] = path
            elif scope["path"].startswith("/api/index.py"):
                scope["path"] = scope["path"].replace("/api/index.py", "", 1) or "/"
            elif scope["path"].startswith("/api/index"):
                scope["path"] = scope["path"].replace("/api/index", "", 1) or "/"

        await self.app(scope, receive, send)


app = VercelPathRewriteMiddleware(raw_app)


