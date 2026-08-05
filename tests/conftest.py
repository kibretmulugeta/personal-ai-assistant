"""
Pytest Async Fixtures for application integration testing.
"""

import sys
from pathlib import Path
import pytest
from httpx import ASGITransport, AsyncClient

# Inject backend and packages into python path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "apps" / "backend"))
sys.path.insert(0, str(root_dir / "packages" / "shared"))
sys.path.insert(0, str(root_dir / "packages" / "database"))

from apps.backend.app.main import app


@pytest.fixture
async def async_client():
    """Yields an HTTPX AsyncClient for endpoint testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
