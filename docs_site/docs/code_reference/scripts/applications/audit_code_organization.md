# Audit Code Organization

**Module:** `scripts.applications.audit_code_organization`
**File:** `/app/scripts/applications/audit_code_organization.py`
**Package:** `applications`

Audit Code Organization

Shows current code organization and recommends what should go where
based on the new production/experimental/deprecated structure.

Usage:
    python3 scripts/production/audit_code_organization.py

## Dependencies

- `collections`
- `os`
- `pathlib`

## Table of Contents

### Functions
- [analyze_file](#analyze-file)
- [audit_directory](#audit-directory)
- [main](#main)

## Functions

### `analyze_file`
```python
analyze_file(file_path)
```

Analyze a file to determine if it's production-ready, experimental, or deprecated.

---

### `audit_directory`
```python
audit_directory(directory_path, max_depth)
```

Audit files in a directory.

---

### `main`
```python
main()
```

Main audit function.

---

*Generated on 2025-06-21 20:19:04*