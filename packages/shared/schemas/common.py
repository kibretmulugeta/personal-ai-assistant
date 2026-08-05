"""
Common Pydantic schemas for API requests, responses, health checks, and pagination.
"""

from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standardized API response wrapper."""

    success: bool = Field(default=True, description="Indicates if the request succeeded")
    message: str = Field(default="Operation completed successfully", description="Status message")
    data: Optional[T] = Field(default=None, description="Payload data")
    errors: Optional[Dict[str, Any]] = Field(default=None, description="Detailed error information if failed")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="UTC response timestamp")


class HealthStatus(BaseModel):
    """Health check endpoint status response model."""

    status: str = Field(..., description="Overall app status ('healthy', 'degraded', 'unhealthy')")
    app_name: str = Field(..., description="Application name")
    environment: str = Field(..., description="Environment (development, production)")
    version: str = Field(..., description="App version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Current server UTC timestamp")
    components: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Individual status of dependent services (database, redis)",
    )


class PaginationMeta(BaseModel):
    """Pagination metadata model."""

    total: int = Field(..., description="Total items matching query")
    page: int = Field(..., description="Current page index (1-based)")
    page_size: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total pages count")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response wrapper."""

    items: List[T] = Field(default_factory=list, description="List of items")
    meta: PaginationMeta = Field(..., description="Pagination metadata")
