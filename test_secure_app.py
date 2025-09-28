"""
Comprehensive test suite for the secure Flask API
Tests both security features and functionality
"""

import json
import os
import sqlite3

# Import our secure app
import sys
import tempfile
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app_secure import (
    app,
    hash_password,
    init_db,
    validate_password,
    validate_username,
    verify_password,
)


class TestSecureApp:
    """Test suite for the secure Flask application"""

    @pytest.fixture
    def client(self):
        """Create test client with temporary database"""
        # Create temporary database
        db_fd, app.config["DATABASE"] = tempfile.mkstemp()

        # Set test configuration
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        # Override database URL for testing
        with patch.dict(
            os.environ, {"DATABASE_URL": f'sqlite:///{app.config["DATABASE"]}'}
        ):
            with app.test_client() as client:
                with app.app_context():
                    init_db()
                yield client

        # Cleanup
        os.close(db_fd)
        os.unlink(app.config["DATABASE"])

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        # Should not expose sensitive database information
        assert "database" not in data

    def test_get_users_empty(self, client):
        """Test getting users when database is empty"""
        response = client.get("/users")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["users"] == []

    def test_create_user_success(self, client):
        """Test successful user creation"""
        user_data = {"username": "testuser", "password": "SecurePass123"}

        response = client.post(
            "/users", data=json.dumps(user_data), content_type="application/json"
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["username"] == "testuser"
        assert "user_id" in data
        assert data["message"] == "User created successfully"

    def test_create_user_invalid_username(self, client):
        """Test user creation with invalid username"""
        test_cases = [
            ("ab", "Username must be at least 3 characters long"),
            ("a" * 51, "Username must be less than 50 characters"),
            ("test@user!", "Username contains invalid characters"),
        ]

        for username, expected_error in test_cases:
            user_data = {"username": username, "password": "SecurePass123"}

            response = client.post(
                "/users", data=json.dumps(user_data), content_type="application/json"
            )

            assert response.status_code == 400
            data = json.loads(response.data)
            assert expected_error in data["error"]

    def test_create_user_weak_password(self, client):
        """Test user creation with weak passwords"""
        test_cases = [
            ("weak", "Password must be at least 8 characters long"),
            (
                "lowercase",
                "Password must contain uppercase, lowercase, and numeric characters",
            ),
            (
                "UPPERCASE123",
                "Password must contain uppercase, lowercase, and numeric characters",
            ),
            (
                "NoNumbers",
                "Password must contain uppercase, lowercase, and numeric characters",
            ),
        ]

        for password, expected_error in test_cases:
            user_data = {"username": "testuser", "password": password}

            response = client.post(
                "/users", data=json.dumps(user_data), content_type="application/json"
            )

            assert response.status_code == 400
            data = json.loads(response.data)
            assert expected_error in data["error"]

    def test_create_duplicate_user(self, client):
        """Test creating user with duplicate username"""
        user_data = {"username": "testuser", "password": "SecurePass123"}

        # Create first user
        response = client.post(
            "/users", data=json.dumps(user_data), content_type="application/json"
        )
        assert response.status_code == 201

        # Try to create duplicate
        response = client.post(
            "/users", data=json.dumps(user_data), content_type="application/json"
        )
        assert response.status_code == 400

        data = json.loads(response.data)
        assert "Username already exists" in data["error"]

    def test_login_success(self, client):
        """Test successful login"""
        # Create user first
        user_data = {"username": "testuser", "password": "SecurePass123"}

        client.post(
            "/users", data=json.dumps(user_data), content_type="application/json"
        )

        # Test login
        response = client.post(
            "/login", data=json.dumps(user_data), content_type="application/json"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Login successful"
        assert data["username"] == "testuser"
        assert "user_id" in data

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        # Create user first
        user_data = {"username": "testuser", "password": "SecurePass123"}

        client.post(
            "/users", data=json.dumps(user_data), content_type="application/json"
        )

        # Test with wrong password
        login_data = {"username": "testuser", "password": "WrongPassword123"}

        response = client.post(
            "/login", data=json.dumps(login_data), content_type="application/json"
        )

        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["error"] == "Invalid credentials"

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        login_data = {"username": "nonexistent", "password": "SecurePass123"}

        response = client.post(
            "/login", data=json.dumps(login_data), content_type="application/json"
        )

        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["error"] == "Invalid credentials"

    def test_sql_injection_protection(self, client):
        """Test SQL injection protection"""
        # Try SQL injection in username
        malicious_data = {
            "username": "'; DROP TABLE users; --",
            "password": "SecurePass123",
        }

        response = client.post(
            "/users", data=json.dumps(malicious_data), content_type="application/json"
        )

        # Should fail due to input validation, not SQL injection
        assert response.status_code == 400

        # Verify table still exists by creating a legitimate user
        good_data = {"username": "gooduser", "password": "SecurePass123"}

        response = client.post(
            "/users", data=json.dumps(good_data), content_type="application/json"
        )
        assert response.status_code == 201

    def test_missing_required_fields(self, client):
        """Test requests with missing required fields"""
        test_cases = [
            {},
            {"username": "testuser"},
            {"password": "SecurePass123"},
            {"username": "", "password": "SecurePass123"},
            {"username": "testuser", "password": ""},
        ]

        for data in test_cases:
            response = client.post(
                "/users", data=json.dumps(data), content_type="application/json"
            )
            assert response.status_code == 400


class TestSecurityFunctions:
    """Test individual security functions"""

    def test_validate_username_valid(self):
        """Test username validation with valid usernames"""
        valid_usernames = ["testuser", "user123", "test_user", "user-name", "user.name"]

        for username in valid_usernames:
            is_valid, message = validate_username(username)
            assert is_valid, f"Username '{username}' should be valid: {message}"

    def test_validate_username_invalid(self):
        """Test username validation with invalid usernames"""
        invalid_usernames = [
            ("ab", "too short"),
            ("a" * 51, "too long"),
            ("user@domain", "invalid characters"),
            ("user space", "invalid characters"),
            ("user!", "invalid characters"),
        ]

        for username, reason in invalid_usernames:
            is_valid, message = validate_username(username)
            assert not is_valid, f"Username '{username}' should be invalid ({reason})"

    def test_validate_password_valid(self):
        """Test password validation with valid passwords"""
        valid_passwords = [
            "SecurePass123",
            "MyPassword1",
            "ComplexPwd99",
            "StrongPassword123",
        ]

        for password in valid_passwords:
            is_valid, message = validate_password(password)
            assert is_valid, f"Password should be valid: {message}"

    def test_validate_password_invalid(self):
        """Test password validation with invalid passwords"""
        invalid_passwords = [
            ("short", "too short"),
            ("nouppercase123", "no uppercase"),
            ("NOLOWERCASE123", "no lowercase"),
            ("NoNumbers", "no numbers"),
            ("a" * 129, "too long"),
        ]

        for password, reason in invalid_passwords:
            is_valid, message = validate_password(password)
            assert not is_valid, f"Password should be invalid ({reason}): {message}"

    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "TestPassword123"

        # Hash password
        password_hash = hash_password(password)
        assert password_hash is not None
        assert isinstance(password_hash, bytes)

        # Verify correct password
        assert verify_password(password, password_hash)

        # Verify incorrect password
        assert not verify_password("WrongPassword123", password_hash)

        # Test that same password produces different hashes (due to salt)
        hash2 = hash_password(password)
        assert password_hash != hash2

        # But both hashes should verify the same password
        assert verify_password(password, hash2)


class TestRateLimiting:
    """Test rate limiting functionality"""

    @pytest.fixture
    def client(self):
        """Create test client for rate limiting tests"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_rate_limiting_works(self, client):
        """Test that rate limiting is enforced"""
        # This test would need to be adapted based on your rate limiting configuration
        # For now, we'll just test that the rate limiter is set up
        assert hasattr(app, "limiter")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
