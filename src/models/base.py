"""
Database configuration and base classes for Narrative Gravity Analysis.
Implements the core database models as specified in Epic 1 requirements.
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL - defaults to local PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/narrative_gravity"
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=os.getenv("SQL_DEBUG", "false").lower() == "true"
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Metadata for Alembic
metadata = Base.metadata

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session():
    """Get a new database session for background tasks."""
    return SessionLocal()

def create_all_tables():
    """Create all tables - used for initial setup."""
    Base.metadata.create_all(bind=engine)

def drop_all_tables():
    """Drop all tables - used for testing cleanup."""
    Base.metadata.drop_all(bind=engine) 