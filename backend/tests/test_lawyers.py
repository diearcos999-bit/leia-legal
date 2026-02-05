"""
Tests for lawyers endpoints.
"""
import pytest


class TestListLawyers:
    """Tests for GET /api/lawyers endpoint."""

    def test_list_lawyers_empty(self, client):
        """Test listing lawyers when database is empty."""
        response = client.get("/api/lawyers")
        assert response.status_code == 200
        data = response.json()
        assert data["lawyers"] == []
        assert data["total"] == 0

    def test_list_lawyers_with_data(self, client, sample_lawyers):
        """Test listing lawyers with data."""
        response = client.get("/api/lawyers")
        assert response.status_code == 200
        data = response.json()
        assert len(data["lawyers"]) == 3
        assert data["total"] == 3

    def test_list_lawyers_filter_by_specialty(self, client, sample_lawyers):
        """Test filtering lawyers by specialty."""
        response = client.get("/api/lawyers?specialty=Derecho%20Laboral")
        assert response.status_code == 200
        data = response.json()
        assert len(data["lawyers"]) == 1
        assert data["lawyers"][0]["specialty"] == "Derecho Laboral"

    def test_list_lawyers_filter_by_location(self, client, sample_lawyers):
        """Test filtering lawyers by location."""
        response = client.get("/api/lawyers?location=Santiago%20Centro")
        assert response.status_code == 200
        data = response.json()
        assert len(data["lawyers"]) == 1
        assert data["lawyers"][0]["location"] == "Santiago Centro"

    def test_list_lawyers_search_by_name(self, client, sample_lawyers):
        """Test searching lawyers by name."""
        response = client.get("/api/lawyers?search=Maria")
        assert response.status_code == 200
        data = response.json()
        assert len(data["lawyers"]) == 1
        assert "Maria" in data["lawyers"][0]["name"]

    def test_list_lawyers_pagination(self, client, sample_lawyers):
        """Test pagination."""
        response = client.get("/api/lawyers?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["lawyers"]) == 2
        assert data["total"] == 3
        assert data["page"] == 1
        assert data["page_size"] == 2

    def test_list_lawyers_pagination_page_2(self, client, sample_lawyers):
        """Test second page of pagination."""
        response = client.get("/api/lawyers?page=2&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["lawyers"]) == 1  # Only 1 lawyer on page 2

    def test_list_lawyers_combined_filters(self, client, sample_lawyers):
        """Test combining multiple filters."""
        response = client.get(
            "/api/lawyers?specialty=Derecho%20Laboral&location=Santiago%20Centro"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["lawyers"]) == 1


class TestGetLawyer:
    """Tests for GET /api/lawyers/{id} endpoint."""

    def test_get_lawyer_success(self, client, test_lawyer):
        """Test getting a specific lawyer."""
        response = client.get(f"/api/lawyers/{test_lawyer.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_lawyer.id
        assert data["name"] == "Test Lawyer"
        assert data["specialty"] == "Derecho Laboral"

    def test_get_lawyer_not_found(self, client):
        """Test getting a non-existent lawyer."""
        response = client.get("/api/lawyers/99999")
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]

    def test_get_lawyer_price_format(self, client, test_lawyer):
        """Test that price is formatted correctly."""
        response = client.get(f"/api/lawyers/{test_lawyer.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["price"] is not None
        assert "$" in data["price"]
