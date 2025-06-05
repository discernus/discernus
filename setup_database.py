#!/usr/bin/env python3
"""
Database setup script for Narrative Gravity Analysis.
This script helps with initial database setup and testing.
"""

import os
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_database_connection():
    """Test that we can connect to the database."""
    try:
        from src.models.base import engine, SessionLocal
        
        print("Testing database connection...")
        
        # Test basic connection
        with engine.connect() as connection:
            from sqlalchemy import text
            result = connection.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            if test_value == 1:
                print("✅ Database connection successful!")
                return True
            else:
                print("❌ Database connection failed - unexpected result")
                return False
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n💡 Make sure PostgreSQL is installed and running:")
        print("   brew install postgresql")
        print("   brew services start postgresql")
        print("   createdb narrative_gravity")
        return False

def check_environment():
    """Check that environment is set up correctly."""
    print("Checking environment setup...")
    
    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found. Creating from example...")
        example_file = Path("env.example")
        if example_file.exists():
            env_file.write_text(example_file.read_text())
            print("✅ Created .env file from example")
        else:
            print("❌ env.example not found")
            return False
    else:
        print("✅ .env file exists")
    
    return True

def create_database_if_not_exists():
    """Create the database if it doesn't exist."""
    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        
        # Connect to postgres database to create our database
        conn = psycopg2.connect(
            host="localhost",
            user="postgres", 
            password="postgres",
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='narrative_gravity'")
        exists = cursor.fetchone()
        
        if not exists:
            print("Creating database 'narrative_gravity'...")
            cursor.execute("CREATE DATABASE narrative_gravity")
            print("✅ Database created successfully!")
        else:
            print("✅ Database 'narrative_gravity' already exists")
            
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Could not create database: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Narrative Gravity Analysis - Database Setup")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        return False
    
    # Create database if needed
    if not create_database_if_not_exists():
        return False
    
    # Test connection
    if not test_database_connection():
        return False
    
    print("\n🎉 Database setup complete!")
    print("\nNext steps:")
    print("1. Run initial migration: alembic revision --autogenerate -m 'Initial tables'")
    print("2. Apply migration: alembic upgrade head")
    print("3. Test with: python -c 'from src.models.base import create_all_tables; create_all_tables()'")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 