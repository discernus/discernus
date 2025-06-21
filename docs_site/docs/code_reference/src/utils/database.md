# Database

**Module:** `src.utils.database`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/src/utils/database.py`
**Package:** `utils`

Database utilities for Discernus Analysis Platform.
Provides database connection helpers and configuration management.

## Dependencies

- `os`
- `typing`
- `urllib.parse`

## Table of Contents

### Functions
- [get_database_url](#get-database-url)
- [get_database_config](#get-database-config)

## Functions

### `get_database_url`
```python
get_database_url() -> str
```

Get the database URL from environment variables.

Returns:
    Database URL string for SQLAlchemy connection
    
Raises:
    ValueError: If DATABASE_URL is not configured

---

### `get_database_config`
```python
get_database_config() -> dict
```

Get complete database configuration.

Returns:
    Dictionary with database configuration parameters

---

*Generated on 2025-06-21 12:44:48*