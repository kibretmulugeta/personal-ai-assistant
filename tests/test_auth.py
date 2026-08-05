"""
Unit tests for JWT token issuance, decoding, and password hashing utilities.
"""

import pytest
from packages.auth.jwt import (
    AuthenticationException,
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing():
    """Verify password hashing and verification."""
    password = "SuperSecretPassword123!"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_flow():
    """Verify JWT access token creation and payload decoding."""
    session_id = "test_sess_12345"
    token = create_access_token(subject=session_id, additional_claims={"user_role": "visitor"})

    assert isinstance(token, str)
    payload = decode_access_token(token)
    assert payload["sub"] == session_id
    assert payload["user_role"] == "visitor"


def test_jwt_token_invalid():
    """Verify exception handling on invalid token."""
    with pytest.raises(AuthenticationException):
        decode_access_token("invalid.jwt.token.string")
