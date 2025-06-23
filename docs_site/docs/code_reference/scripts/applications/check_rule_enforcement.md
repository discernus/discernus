# Check Rule Enforcement

**Module:** `scripts.applications.check_rule_enforcement`
**File:** `/app/scripts/applications/check_rule_enforcement.py`
**Package:** `applications`

Rule Enforcement Status Check

Quick verification that all AI assistant rule enforcement mechanisms 
are in place and functioning correctly.

Usage:
    python3 scripts/production/check_rule_enforcement.py

## Dependencies

- `pathlib`
- `sys`

## Table of Contents

### Functions
- [check_file_exists](#check-file-exists)
- [check_directory_exists](#check-directory-exists)
- [check_content_exists](#check-content-exists)
- [main](#main)

## Functions

### `check_file_exists`
```python
check_file_exists(file_path, description)
```

Check if a required file exists.

---

### `check_directory_exists`
```python
check_directory_exists(dir_path, description)
```

Check if a required directory exists.

---

### `check_content_exists`
```python
check_content_exists(file_path, search_text, description)
```

Check if specific content exists in a file.

---

### `main`
```python
main()
```

Main status check function.

---

*Generated on 2025-06-23 10:38:43*