# Base

**Module:** `src.models.base`
**File:** `/app/src/models/base.py`
**Package:** `models`

Database configuration and base classes for Narrative Gravity Analysis.

🐘 PRIMARY DATABASE: PostgreSQL (Production/Development)
   - Connection: postgresql://postgres:postgres@localhost:5432/narrative_gravity
   - Used for: Main app, API, Celery workers, production data
   - Migrations: Managed by Alembic

📁 SQLite Usage:
   - Testing only: In-memory SQLite for unit tests
   - Logging fallback: logs/discernus_stats.db when PostgreSQL unavailable
   - NOT used for main application data

See docs/architecture/database_architecture.md for complete details.

## Dependencies

- `dotenv`
- `os`
- `sqlalchemy`
- `sqlalchemy.ext.declarative`
- `sqlalchemy.orm`
- `sqlalchemy.pool`
- `src.utils.database`

## Table of Contents

### Functions
- [get_db](#get-db)
- [get_db_session](#get-db-session)
- [create_all_tables](#create-all-tables)
- [drop_all_tables](#drop-all-tables)

## Functions

### `get_db`
```python
get_db()
```

Dependency to get database session.

---

### `get_db_session`
```python
get_db_session()
```

Get a new database session for background tasks.

---

### `create_all_tables`
```python
create_all_tables()
```

Create all tables - used for initial setup.

---

### `drop_all_tables`
```python
drop_all_tables()
```

Drop all tables - used for testing cleanup.

---

*Generated on 2025-06-23 10:38:43*