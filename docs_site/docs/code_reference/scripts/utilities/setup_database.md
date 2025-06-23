# Setup Database

**Module:** `scripts.utilities.setup_database`
**File:** `/app/scripts/utilities/setup_database.py`
**Package:** `utilities`

Database setup script for Narrative Gravity Analysis.
This script helps with initial database setup and testing.

## Dependencies

- `os`
- `pathlib`
- `psycopg2`
- `psycopg2.extensions`
- `sqlalchemy`
- `src.models.base`
- `sys`

## Table of Contents

### Functions
- [test_database_connection](#test-database-connection)
- [check_environment](#check-environment)
- [create_database_if_not_exists](#create-database-if-not-exists)
- [main](#main)

## Functions

### `test_database_connection`
```python
test_database_connection()
```

Test that we can connect to the database.

---

### `check_environment`
```python
check_environment()
```

Check that environment is set up correctly.

---

### `create_database_if_not_exists`
```python
create_database_if_not_exists()
```

Create the database if it doesn't exist.

---

### `main`
```python
main()
```

Main setup function.

---

*Generated on 2025-06-23 10:38:43*