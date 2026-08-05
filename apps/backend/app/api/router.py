"""
Main API Router aggregator combining versioned v1 sub-routers.
"""

from fastapi import APIRouter
from apps.backend.app.api.v1.auth import router as auth_router
from apps.backend.app.api.v1.chat import router as chat_router
from apps.backend.app.api.v1.contact import router as contact_router
from apps.backend.app.api.v1.documents import router as documents_router
from apps.backend.app.api.v1.health import router as health_router

api_router = APIRouter()

# Register v1 routes
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(chat_router)
api_router.include_router(contact_router)
api_router.include_router(documents_router)
