"""
FastAPI Backend Application Entrypoint.
Initializes middleware, CORS, logging, exception handlers, and routing.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from apps.backend.app.api.router import api_router
from apps.backend.app.core.config import settings
from apps.backend.app.core.logging import get_logger, setup_logging
from packages.database.session import engine
from packages.shared.exceptions import BaseAppException

logger = get_logger("backend.main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context managing startup and shutdown tasks."""
    # Startup actions
    setup_logging(log_level=settings.LOG_LEVEL, is_dev=(settings.APP_ENV == "development"))
    logger.info(
        "starting_application",
        app_name=settings.APP_NAME,
        environment=settings.APP_ENV,
        active_llm=settings.ACTIVE_LLM_PROVIDER,
        active_embedding=settings.ACTIVE_EMBEDDING_PROVIDER,
    )
    yield
    # Shutdown actions
    logger.info("shutting_down_application")
    await engine.dispose()


def create_application() -> FastAPI:
    """FastAPI Application factory."""
    app = FastAPI(
        title=settings.APP_NAME,
        description="Production-ready standalone AI assistant and digital twin of Alemu Kibret Mulugeta",
        version="0.1.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
        docs_url=f"{settings.API_V1_STR}/docs" if settings.DEBUG else None,
        redoc_url=f"{settings.API_V1_STR}/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # CORS Middleware configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Domain Exception Handler
    @app.exception_handler(BaseAppException)
    async def custom_app_exception_handler(
        request: Request, exc: BaseAppException
    ) -> JSONResponse:
        logger.warning(f"domain_exception_raised code={exc.code} message={exc.message} path={request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        )

    # Global Exception Fallback Handler
    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error(f"unhandled_exception error={str(exc)} path={request.url.path}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred on the server.",
                "details": {},
            },
        )

    # Include API Routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/", tags=["System"])
    async def root():
        """Root endpoint returning API status."""
        return {
            "name": settings.APP_NAME,
            "status": "online",
            "version": "0.1.0",
            "message": "Personal AI Assistant API is running",
            "demo_url": "/demo"
        }

    from fastapi.responses import HTMLResponse

    @app.get("/demo", response_class=HTMLResponse, tags=["System"])
    async def demo_ui():
        """Returns a live HTML page with the chat widget embedded for easy testing."""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Alemu Kibret Mulugeta - AI Assistant Demo</title>
          <style>
            body { margin: 0; padding: 0; font-family: -apple-system, sans-serif; background: #0f172a; color: #f8fafc; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
            h1 { color: #6366f1; margin-bottom: 10px; }
            p { color: #94a3b8; max-width: 600px; line-height: 1.6; }
          </style>
          <!-- Load Widget CSS from GitHub (via jsdelivr) -->
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/kibretmulugeta/personal-ai-assistant@main/apps/widget/dist/widget.css">
        </head>
        <body>
          <h1>AI Digital Twin Demo</h1>
          <p>This is a live test page hosted directly on your Vercel backend.<br>Look at the bottom right corner of the screen and click the Chat button to talk to your AI!</p>
          
          <!-- Load Widget JS from GitHub (via jsdelivr) -->
          <script src="https://cdn.jsdelivr.net/gh/kibretmulugeta/personal-ai-assistant@main/apps/widget/dist/widget.js"></script>
          <script>
            WebsiteAssistant.init({
              apiKey: "demo-api-key-12345",
              apiEndpoint: "/api/v1", // Points to this exact same Vercel deployment
              theme: "dark",
              position: "bottom-right",
              primaryColor: "#6366f1"
            });
          </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "apps.backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
