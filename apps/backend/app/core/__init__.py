"""
Core backend package initialization.
"""

from apps.backend.app.core.config import settings
from apps.backend.app.core.logging import get_logger, setup_logging

__all__ = ["settings", "get_logger", "setup_logging"]
