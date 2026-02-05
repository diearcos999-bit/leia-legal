"""
Tests for authentication endpoints.
"""
import pytest


class TestRegister:
    """Tests for /api/auth/register endpoint."""

    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePass123",
                "full_name": "New User"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "newuser@example.com"

    def test_register_duplicate_email(self, client, test_user):
        """Test registration with already registered email."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "SecurePass123",
                "full_name": "Another User"
            }
        )
        assert response.status_code == 400
        assert "ya está registrado" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "not-an-email",
                "password": "SecurePass123",
                "full_name": "Test User"
            }
        )
        assert response.status_code == 422

    def test_register_short_password(self, client):
        """Test registration with too short password."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "short",
                "full_name": "Test User"
            }
        )
        assert response.status_code == 422

    def test_register_password_no_number(self, client):
        """Test registration with password without numbers."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "OnlyLetters",
                "full_name": "Test User"
            }
        )
        assert response.status_code == 422

    def test_register_password_no_letter(self, client):
        """Test registration with password without letters."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "12345678",
                "full_name": "Test User"
            }
        )
        assert response.status_code == 422


class TestLogin:
    """Tests for /api/auth/login endpoint."""

    def test_login_success(self, client, test_user):
        """Test successful login."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "TestPass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "test@example.com"

    def test_login_wrong_password(self, client, test_user):
        """Test login with incorrect password."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "WrongPassword123"
            }
        )
        assert response.status_code == 401
        assert "incorrectos" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent email."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "SomePassword123"
            }
        )
        assert response.status_code == 401

    def test_login_invalid_email_format(self, client):
        """Test login with invalid email format."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "not-an-email",
                "password": "SomePassword123"
            }
        )
        assert response.status_code == 422


class TestMe:
    """Tests for /api/auth/me endpoint."""

    def test_get_current_user(self, client, test_user, auth_headers):
        """Test getting current user info."""
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test User"

    def test_get_current_user_no_token(self, client):
        """Test getting current user without token."""
        response = client.get("/api/auth/me")
        assert response.status_code == 403

    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token."""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
