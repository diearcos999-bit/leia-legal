"""
Database configuration and session management for LEIA.
Uses SQLite for MVP simplicity - can be migrated to PostgreSQL for production.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - SQLite for MVP, PostgreSQL for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./leia.db")

# Create engine
# For SQLite, we need check_same_thread=False for FastAPI
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.
    Ensures the session is closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.
    Call this on application startup.
    """
    Base.metadata.create_all(bind=engine)
