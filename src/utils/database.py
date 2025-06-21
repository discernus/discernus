"""
Database utilities for Discernus Analysis Platform.
Provides database connection helpers and configuration management.
"""

import os
from typing import Optional


def get_database_url() -> str:
    """
    Get the database URL from environment variables.
    
    Returns:
        Database URL string for SQLAlchemy connection
        
    Raises:
        ValueError: If DATABASE_URL is not configured
    """
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        # Fallback to individual components
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'discernus')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'postgres')
        
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    return database_url


def get_database_config() -> dict:
    """
    Get complete database configuration.
    
    Returns:
        Dictionary with database configuration parameters
    """
    database_url = get_database_url()
    
    # Parse the URL to extract components
    import urllib.parse
    
    if database_url.startswith('postgresql://'):
        parsed = urllib.parse.urlparse(database_url)
        config = {
            'url': database_url,
            'host': parsed.hostname,
            'port': parsed.port or 5432,
            'database': parsed.path.lstrip('/'),
            'username': parsed.username,
            'password': parsed.password,
            'driver': 'postgresql'
        }
    else:
        # SQLite fallback for testing
        config = {
            'url': database_url,
            'driver': 'sqlite'
        }
    
    return config 