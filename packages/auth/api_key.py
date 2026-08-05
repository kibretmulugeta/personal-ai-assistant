"""
API Key authentication utilities for securing widget and developer REST requests.
"""

from typing import Optional
from apps.backend.app.core.config import settings
from packages.auth.jwt import AuthenticationException


def validate_api_key(api_key: Optional[str]) -> bool:
    """Validate incoming API key against application SECRET_KEY or configured key.

    Args:
        api_key: Header value passed by client (X-API-Key).

    Returns:
        True if valid.

    Raises:
        AuthenticationException if invalid.
    """
    if not api_key:
        raise AuthenticationException(message="API key is missing in X-API-Key header.")
    
    # In production, compare against configured allowed widget API keys or secret key
    if api_key != settings.SECRET_KEY and not settings.DEBUG:
        raise AuthenticationException(message="Invalid API Key provided.")
    
    return True
