"""
Base and specific application exceptions for clean architecture exception handling.
"""

from typing import Any, Dict, Optional


class BaseAppException(Exception):
    """Base exception class for all domain-specific application exceptions."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_SERVER_ERROR",
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}
        self.status_code = status_code


class ResourceNotFoundException(BaseAppException):
    """Raised when a requested domain entity or database record is not found."""

    def __init__(
        self,
        resource_name: str,
        identifier: Any,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        message = f"{resource_name} with identifier '{identifier}' was not found."
        super().__init__(
            message=message,
            code="RESOURCE_NOT_FOUND",
            details=details,
            status_code=404,
        )


class ValidationException(BaseAppException):
    """Raised when request data or domain validation fails."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details=details,
            status_code=422,
        )


class DatabaseException(BaseAppException):
    """Raised when a database query or persistence action fails."""

    def __init__(
        self,
        message: str = "A database operation error occurred.",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            details=details,
            status_code=500,
        )


class RateLimitExceededException(BaseAppException):
    """Raised when a user or IP exceeds defined rate limits."""

    def __init__(
        self,
        message: str = "Rate limit exceeded. Please try again later.",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="RATE_LIMIT_EXCEEDED",
            details=details,
            status_code=429,
        )
