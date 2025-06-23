# Terminology Lint

**Module:** `scripts.applications.terminology_lint`
**File:** `/app/scripts/applications/terminology_lint.py`
**Package:** `applications`

Terminology Lint - Production Compliance

Checks staged changes for legacy terminology such as "well", "dipole", or
"gravity". Intended for use as a pre-commit hook to enforce the new
cartographic vocabulary outlined in the Discernus Terminology Strategy.

## Dependencies

- `pathlib`
- `re`
- `subprocess`
- `sys`

## Table of Contents

### Functions
- [get_staged_changes](#get-staged-changes)
- [main](#main)

## Functions

### `get_staged_changes`
```python
get_staged_changes() -> list[tuple[Any]]
```

Return a list of (file, line_number, line_content) for added lines in staged changes.

---

### `main`
```python
main() -> int
```

---

*Generated on 2025-06-23 10:38:43*