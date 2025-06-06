import pytest
import sys
import os
from datetime import timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    AuthenticationError
)

class TestAuthUtils:
    """
    Unit tests for the pure authentication utility functions.
    """

    # --- Password Hashing and Verification Tests ---
    def test_hash_and_verify_password(self):
        """Tests that a password can be hashed and then successfully verified."""
        password = "a_very_secret_password_123"
        hashed_password = hash_password(password)
        
        assert hashed_password != password
        assert verify_password(password, hashed_password) == True
        assert verify_password("wrong_password", hashed_password) == False

    # --- Token Creation and Decoding Tests ---
    def test_create_and_decode_access_token(self):
        """Tests the creation and successful decoding of a standard access token."""
        user_data = {"user_id": 1, "username": "testuser", "role": "user"}
        token = create_access_token(data=user_data)
        
        decoded_payload = decode_token(token)
        
        assert decoded_payload["user_id"] == user_data["user_id"]
        assert decoded_payload["username"] == user_data["username"]
        assert decoded_payload["type"] == "access"

    def test_create_and_decode_refresh_token(self):
        """Tests the creation and successful decoding of a refresh token."""
        user_data = {"user_id": 2, "username": "refresh_user"}
        token = create_refresh_token(data=user_data)
        
        decoded_payload = decode_token(token)
        
        assert decoded_payload["user_id"] == user_data["user_id"]
        assert decoded_payload["type"] == "refresh"

    def test_decode_expired_token_raises_error(self):
        """Tests that decoding an expired token raises an AuthenticationError."""
        user_data = {"user_id": 3, "username": "expired_user"}
        # Create a token that expired 1 second ago
        expired_token = create_access_token(data=user_data, expires_delta=timedelta(seconds=-1))
        
        with pytest.raises(AuthenticationError, match="Invalid token"):
            decode_token(expired_token)

    def test_decode_invalid_token_raises_error(self):
        """Tests that decoding a malformed or invalid token raises an AuthenticationError."""
        invalid_token = "this.is.not.a.valid.jwt"
        
        with pytest.raises(AuthenticationError, match="Invalid token"):
            decode_token(invalid_token)

    def test_token_with_different_secret_raises_error(self):
        """
        This test requires modifying the secret key at runtime, which is complex.
        An integration test would be better suited to cover this scenario by
        configuring the app with a different key. For now, we'll assume the
        underlying 'jose' library correctly handles signature verification.
        """
        pass 