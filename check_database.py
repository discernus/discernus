#!/usr/bin/env python3
"""
Database Configuration Checker
Quick script to verify database setup and configuration
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_environment():
    """Check environment configuration."""
    print("🔧 Environment Configuration")
    print("=" * 40)
    
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found")
        print("💡 Copy env.example to .env")
    
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        print(f"✅ DATABASE_URL: {db_url}")
        if db_url.startswith('postgresql'):
            print("✅ Configured for PostgreSQL")
        else:
            print("⚠️  Not configured for PostgreSQL")
    else:
        print("⚠️  DATABASE_URL not set")
    
    print()

def check_postgresql():
    """Check PostgreSQL connection."""
    print("🐘 PostgreSQL Connection")
    print("=" * 40)
    
    try:
        from src.models.base import engine
        
        # Check URL
        db_url = str(engine.url)
        print(f"Database URL: {db_url}")
        
        if not db_url.startswith('postgresql'):
            print("❌ Not using PostgreSQL!")
            return False
            
        # Test connection
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connected successfully")
            print(f"Version: {version}")
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Try: brew install postgresql && brew services start postgresql")
        print("💡 Then: createdb narrative_gravity")
        return False

def check_sqlite_usage():
    """Check SQLite file usage."""
    print("📁 SQLite File Status")
    print("=" * 40)
    
    # Check legacy file
    if Path("narrative_gravity.db").exists():
        print("⚠️  Legacy narrative_gravity.db found (should not exist)")
    else:
        print("✅ No legacy SQLite file")
    
    # Check stats file
    stats_file = Path("logs/discernus_stats.db")
    if stats_file.exists():
        size = stats_file.stat().st_size
        print(f"📊 Stats file: {stats_file} ({size} bytes)")
        print("ℹ️  This is for logging fallback only")
    else:
        print("📊 No stats file (will be created when needed)")
    
    print()

def check_alembic():
    """Check Alembic migration status."""
    print("🔄 Migration Status")
    print("=" * 40)
    
    try:
        import subprocess
        result = subprocess.run(
            ["alembic", "current"], 
            capture_output=True, 
            text=True,
            cwd=project_root
        )
        
        if result.returncode == 0:
            current = result.stdout.strip()
            if current:
                print(f"✅ Current revision: {current}")
            else:
                print("⚠️  No migrations applied")
                print("💡 Run: alembic upgrade head")
        else:
            print(f"❌ Alembic error: {result.stderr}")
            
    except FileNotFoundError:
        print("⚠️  Alembic not installed")
        print("💡 Run: pip install alembic")
    
    print()

def main():
    """Main check function."""
    print("🎯 Narrative Gravity Wells - Database Check")
    print("=" * 60)
    print()
    
    check_environment()
    pg_ok = check_postgresql()
    check_sqlite_usage()
    
    if pg_ok:
        check_alembic()
    
    print("📖 For detailed information, see: docs/architecture/database_architecture.md")
    print()
    
    if pg_ok:
        print("🎉 Database configuration looks good!")
    else:
        print("⚠️  Database needs attention")
        print("💡 Run: python launch.py --setup-db")

if __name__ == "__main__":
    main() 