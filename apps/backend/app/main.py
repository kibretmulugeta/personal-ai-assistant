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
