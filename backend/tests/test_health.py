"""
Tests for health and basic API endpoints.
"""
import pytest


class TestHealth:
    """Tests for health endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "JusticiaAI API"
        assert "version" in data
        assert "endpoints" in data

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "anthropic_configured" in data


class TestQuickQuestions:
    """Tests for quick questions endpoint."""

    def test_get_quick_questions(self, client):
        """Test getting quick questions."""
        response = client.get("/api/quick-questions")
        assert response.status_code == 200
        data = response.json()
        assert "questions" in data
        assert isinstance(data["questions"], list)
        assert len(data["questions"]) > 0


class TestFeedback:
    """Tests for feedback endpoints."""

    def test_submit_feedback_helpful(self, client):
        """Test submitting helpful feedback."""
        response = client.post(
            "/api/feedback",
            json={
                "message_id": "test-123",
                "user_question": "What is labor law?",
                "ai_response": "Labor law covers employment...",
                "feedback": "helpful"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "saved"

    def test_submit_feedback_not_helpful(self, client):
        """Test submitting not helpful feedback with correction."""
        response = client.post(
            "/api/feedback",
            json={
                "message_id": "test-456",
                "user_question": "What is labor law?",
                "ai_response": "Labor law covers employment...",
                "feedback": "not_helpful",
                "correction": "The information about deadlines was incorrect"
            }
        )
        assert response.status_code == 200

    def test_submit_feedback_invalid_type(self, client):
        """Test submitting feedback with invalid feedback type."""
        response = client.post(
            "/api/feedback",
            json={
                "message_id": "test-789",
                "user_question": "Test question",
                "ai_response": "Test response",
                "feedback": "invalid_type"
            }
        )
        assert response.status_code == 422

    def test_get_feedback_stats(self, client):
        """Test getting feedback statistics."""
        response = client.get("/api/feedback/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "helpful" in data
        assert "not_helpful" in data
