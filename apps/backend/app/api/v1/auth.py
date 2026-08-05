"""
Authentication API Router.
Provides JWT token issuance for clients and widget sessions.
"""

import uuid
from fastapi import APIRouter, status
from apps.backend.app.core.config import settings
from apps.backend.app.schemas.auth import TokenRequest, TokenResponse
from packages.auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def generate_token(request: TokenRequest) -> TokenResponse:
    """Generate signed JWT access token for widget or client session."""
    session_id = request.session_id or f"session_{uuid.uuid4().hex[:12]}"
    token = create_access_token(
        subject=session_id,
        additional_claims={"session_id": session_id},
    )
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
