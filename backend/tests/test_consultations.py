"""
Tests for consultations endpoints.
"""
import pytest


class TestCreateConsultation:
    """Tests for POST /api/consultations endpoint."""

    def test_create_consultation_success(self, client, test_lawyer):
        """Test creating a consultation successfully."""
        response = client.post(
            "/api/consultations",
            json={
                "lawyer_id": test_lawyer.id,
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+56912345678",
                "description": "I need help with a labor dispute"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["status"] == "pending"
        assert data["lawyer_id"] == test_lawyer.id

    def test_create_consultation_without_phone(self, client, test_lawyer):
        """Test creating consultation without optional phone."""
        response = client.post(
            "/api/consultations",
            json={
                "lawyer_id": test_lawyer.id,
                "name": "Jane Doe",
                "email": "jane@example.com",
                "description": "I need help with a family matter"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["phone"] is None

    def test_create_consultation_lawyer_not_found(self, client):
        """Test creating consultation with non-existent lawyer."""
        response = client.post(
            "/api/consultations",
            json={
                "lawyer_id": 99999,
                "name": "John Doe",
                "email": "john@example.com",
                "description": "I need legal help"
            }
        )
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]

    def test_create_consultation_invalid_email(self, client, test_lawyer):
        """Test creating consultation with invalid email."""
        response = client.post(
            "/api/consultations",
            json={
                "lawyer_id": test_lawyer.id,
                "name": "John Doe",
                "email": "not-an-email",
                "description": "I need legal help"
            }
        )
        assert response.status_code == 422

    def test_create_consultation_short_name(self, client, test_lawyer):
        """Test creating consultation with name too short."""
        response = client.post(
            "/api/consultations",
            json={
                "lawyer_id": test_lawyer.id,
                "name": "J",
                "email": "john@example.com",
                "description": "I need legal help"
            }
        )
        assert response.status_code == 422

    def test_create_consultation_short_description(self, client, test_lawyer):
        """Test creating consultation with description too short."""
        response = client.post(
            "/api/consultations",
            json={
                "lawyer_id": test_lawyer.id,
                "name": "John Doe",
                "email": "john@example.com",
                "description": "Short"
            }
        )
        assert response.status_code == 422

    def test_create_consultation_with_auth(self, client, test_lawyer, auth_headers):
        """Test creating consultation as authenticated user."""
        response = client.post(
            "/api/consultations",
            json={
                "lawyer_id": test_lawyer.id,
                "name": "Test User",
                "email": "test@example.com",
                "description": "I need help with a legal matter"
            },
            headers=auth_headers
        )
        assert response.status_code == 200


class TestListConsultations:
    """Tests for GET /api/consultations endpoint."""

    def test_list_consultations_requires_auth(self, client):
        """Test that listing consultations requires authentication."""
        response = client.get("/api/consultations")
        assert response.status_code == 403

    def test_list_consultations_authenticated(self, client, auth_headers, test_lawyer):
        """Test listing consultations as authenticated user."""
        # First create a consultation
        client.post(
            "/api/consultations",
            json={
                "lawyer_id": test_lawyer.id,
                "name": "Test User",
                "email": "test@example.com",
                "description": "I need help with a legal matter"
            },
            headers=auth_headers
        )

        # Then list consultations
        response = client.get("/api/consultations", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
