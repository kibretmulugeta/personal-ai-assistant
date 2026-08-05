"""
Unit and integration tests for health check endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_liveness_endpoint(async_client: AsyncClient):
    """Test that /api/v1/health/liveness returns status 200 and 'alive'."""
    response = await async_client.get("/api/v1/health/liveness")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "alive"


@pytest.mark.asyncio
async def test_health_endpoint_schema(async_client: AsyncClient):
    """Test overall health check endpoint structure."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data
    assert "app_name" in json_data
    assert "components" in json_data
