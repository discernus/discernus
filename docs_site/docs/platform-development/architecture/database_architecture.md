# Database Architecture - Narrative Gravity Wells

## 🗄️ Database Usage Overview

The Narrative Gravity Wells project uses **multiple databases** for different purposes. This document clarifies when each is used to prevent confusion.

## 📊 Database Types & Usage

### 🐘 **PostgreSQL (PRIMARY/PRODUCTION)**
- **Purpose**: Main application database
- **Location**: External PostgreSQL server
- **Connection**: `postgresql://postgres:postgres@localhost:5432/narrative_gravity`
- **Used By**:
  - ✅ Main application (`src/narrative_gravity/app.py`)
  - ✅ API server (`src/api/`)
  - ✅ Celery workers
  - ✅ Production data storage
  - ✅ Alembic migrations

### 📁 **SQLite (FALLBACK/LOGGING)**
- **Purpose**: Fallback logging and statistics
- **Location**: `logs/narrative_gravity_stats.db`
- **Used By**:
  - ⚠️ Statistical logger when PostgreSQL unavailable
  - ⚠️ Local logging fallback
  - ❌ **NOT** for main application data

### 🧪 **SQLite (TESTING)**
- **Purpose**: Unit testing only
- **Location**: In-memory (`:memory:`)
- **Used By**:
  - ✅ Unit tests (`tests/unit/`)
  - ✅ Isolated test environments
  - ❌ **NOT** for application data

### 🗃️ **Legacy SQLite File**
- **File**: `narrative_gravity.db` (root directory)
- **Status**: ⚠️ **LEGACY/UNUSED** (0 bytes)
- **Action**: Should be removed

## 🔧 Configuration Hierarchy

### Environment Variables (`.env`)
```bash
# PRIMARY DATABASE (PostgreSQL)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/narrative_gravity

# OPTIONAL: Enable SQL debugging
SQL_DEBUG=false
```

### Fallback Logic (Statistical Logger)
1. **Try PostgreSQL** (from `DATABASE_URL`)
2. **If unavailable**: Fall back to SQLite in `logs/`
3. **Testing**: Always use in-memory SQLite

## 🚀 Setup Instructions

### 1. Initial Database Setup
```bash
python launch.py --setup-db
```

### 2. Verify PostgreSQL Connection
```bash
python -c "from src.narrative_gravity.models.base import engine; engine.connect(); print('✅ PostgreSQL connected')"
```

### 3. Check Database Status
```bash
python scripts/setup_database.py
```

## 🔍 Troubleshooting

### "Database not accessible" Error
**Cause**: PostgreSQL not running or misconfigured

**Solutions**:
```bash
# Install PostgreSQL (macOS)
brew install postgresql
brew services start postgresql

# Create database
createdb narrative_gravity

# Run setup
python launch.py --setup-db
```

### SQLite Fallback Messages
**Cause**: PostgreSQL unavailable, using fallback logging

**Fix**: Ensure PostgreSQL is running and properly configured

### Test Database Issues
**Cause**: Unit tests should always use in-memory SQLite

**Check**: Ensure test fixtures use `sqlite:///:memory:`

## 📋 Database Schema Management

### Migrations (PostgreSQL Only)
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Check status
alembic current
```

### Schema Files
- **Primary Schema**: Defined in `src/narrative_gravity/models/`
- **Migrations**: Stored in `alembic/versions/`
- **Config**: `alembic.ini` (PostgreSQL only)

## 🎯 For AI Assistants & Developers

### Default Assumptions
1. **Always assume PostgreSQL** for main application
2. **SQLite only for**:
   - Unit testing (in-memory)
   - Statistical logging fallback
   - Local development without PostgreSQL

### When to Use Each Database

| Use Case | Database | Connection |
|----------|----------|------------|
| Main app development | PostgreSQL | `DATABASE_URL` |
| Production deployment | PostgreSQL | `DATABASE_URL` |
| Unit testing | SQLite | `:memory:` |
| Statistical logging | SQLite | `logs/narrative_gravity_stats.db` |
| Schema migrations | PostgreSQL | Alembic |

### Quick Checks
```bash
# What database is configured?
echo $DATABASE_URL

# Is PostgreSQL running?
pg_isready -h localhost -p 5432

# Test connection
python -c "from src.narrative_gravity.models.base import engine; print(engine.url)"
```

## ⚠️ Common Pitfalls

1. **Don't assume SQLite for main app** - It's PostgreSQL
2. **Don't migrate SQLite files** - They're temporary/fallback
3. **Don't store production data in SQLite** - Use PostgreSQL
4. **Don't ignore database setup** - Run `--setup-db` first

## 🧹 Cleanup Actions

### Remove Legacy SQLite File
```bash
rm narrative_gravity.db  # 0-byte legacy file
```

### Clear Logs (if needed)
```bash
rm logs/narrative_gravity_stats.db*
```

This architecture ensures **PostgreSQL for production** and **SQLite only for testing/fallback**, eliminating database confusion! 