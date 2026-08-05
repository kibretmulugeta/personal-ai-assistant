"""
Pydantic schemas for authentication and token responses.
"""

from pydantic import BaseModel, Field


class TokenRequest(BaseModel):
    """Token generation request."""
    session_id: str = Field(..., description="Visitor session ID or client identifier")


class TokenResponse(BaseModel):
    """JWT token response payload."""
    access_token: str = Field(..., description="Signed JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in_minutes: int = Field(..., description="Token expiration window")
