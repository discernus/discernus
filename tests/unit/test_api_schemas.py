import pytest
from pydantic import ValidationError
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.api.schemas import JobCreate, UserCreate, UserRole, DocumentBase, DocumentType

class TestApiSchemas:
    """
    Unit tests for the Pydantic schemas in the API.
    """

    # --- JobCreate Schema Tests ---
    def test_job_create_valid(self):
        """Tests successful validation of a valid JobCreate schema."""
        valid_data = {
            "corpus_id": 1,
            "text_ids": ["text1", "text2"],
            "frameworks": ["civic_virtue", "moral_rhetorical_posture"],
            "models": ["gpt-4o"]
        }
        job = JobCreate(**valid_data)
        assert job.corpus_id == 1
        assert job.run_count == 5  # Default value

    def test_job_create_invalid_framework(self):
        """Tests that an unsupported framework raises a ValidationError."""
        invalid_data = {
            "corpus_id": 1,
            "text_ids": ["text1"],
            "frameworks": ["unsupported_framework"],
            "models": ["gpt-4o"]
        }
        with pytest.raises(ValidationError, match="Unsupported framework"):
            JobCreate(**invalid_data)

    # --- UserCreate Schema Tests ---
    def test_user_create_valid(self):
        """Tests successful validation of a valid UserCreate schema."""
        user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "a_valid_password"
        }
        user = UserCreate(**user_data)
        assert user.username == "test_user"
        assert user.role == UserRole.user  # Default value

    @pytest.mark.parametrize("invalid_username", ["a", "user name", "user!"])
    def test_user_create_invalid_username(self, invalid_username):
        """Tests that invalid usernames raise a ValidationError."""
        user_data = {"username": invalid_username, "email": "test@example.com", "password": "password"}
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    @pytest.mark.parametrize("invalid_email", ["not-an-email", "test@", "@domain.com", "test@domain"])
    def test_user_create_invalid_email(self, invalid_email):
        """Tests that invalid emails raise a ValidationError."""
        user_data = {"username": "testuser", "email": invalid_email, "password": "password"}
        with pytest.raises(ValidationError, match="Invalid email format"):
            UserCreate(**user_data)

    # --- DocumentBase Schema Tests ---
    def test_document_base_valid(self):
        """Tests successful validation of a valid DocumentBase schema."""
        doc_data = {
            "text_id": "doc1", "title": "A Title", "document_type": "speech",
            "author": "An Author", "date": datetime.now(), "schema_version": "1.0.0"
        }
        doc = DocumentBase(**doc_data)
        assert doc.text_id == "doc1"

    def test_document_base_invalid_schema_version(self):
        """Tests that an invalid schema version raises a ValidationError."""
        doc_data = {
            "text_id": "doc1", "title": "A Title", "document_type": "speech",
            "author": "An Author", "date": datetime.now(), "schema_version": "1.0" # Invalid
        }
        with pytest.raises(ValidationError, match="String should match pattern"):
            DocumentBase(**doc_data) 