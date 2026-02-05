"""
Pytest configuration and fixtures for JusticiaAI backend tests.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, get_db
from main import app
from models import User, Lawyer
from auth import get_password_hash


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("TestPass123"),
        full_name="Test User",
        is_active=True,
        is_verified=False,
        role="user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_lawyer(db_session):
    """Create a test lawyer."""
    lawyer = Lawyer(
        name="Test Lawyer",
        specialty="Derecho Laboral",
        experience="10 years",
        rating=4.5,
        reviews=50,
        location="Santiago Centro",
        price_min=50000,
        price_max=80000,
        description="Test lawyer description",
        is_verified=True
    )
    db_session.add(lawyer)
    db_session.commit()
    db_session.refresh(lawyer)
    return lawyer


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for a logged-in user."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_lawyers(db_session):
    """Create multiple test lawyers."""
    lawyers = [
        Lawyer(
            name="Maria Gonzalez",
            specialty="Derecho Laboral",
            experience="12 years",
            rating=4.9,
            reviews=127,
            location="Santiago Centro",
            price_min=50000,
            price_max=80000,
            description="Labor law specialist",
            is_verified=True
        ),
        Lawyer(
            name="Carlos Rodriguez",
            specialty="Derecho de Familia",
            experience="8 years",
            rating=4.8,
            reviews=89,
            location="Las Condes",
            price_min=60000,
            price_max=100000,
            description="Family law specialist",
            is_verified=True
        ),
        Lawyer(
            name="Ana Martinez",
            specialty="Deudas y Cobranzas",
            experience="15 years",
            rating=5.0,
            reviews=203,
            location="Providencia",
            price_min=40000,
            price_max=70000,
            description="Debt specialist",
            is_verified=True
        ),
    ]
    for lawyer in lawyers:
        db_session.add(lawyer)
    db_session.commit()
    return lawyers
