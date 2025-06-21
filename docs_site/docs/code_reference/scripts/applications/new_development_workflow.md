# New Development Workflow

**Module:** `scripts.applications.new_development_workflow`
**File:** `/app/scripts/applications/new_development_workflow.py`
**Package:** `applications`

New Development Workflow

Guided workflow that enforces AI assistant rules automatically.
Makes following the rules easier than breaking them.

Usage:
    python3 scripts/production/new_development_workflow.py

## Dependencies

- `pathlib`
- `subprocess`
- `sys`

## Table of Contents

### Functions
- [run_command](#run-command)
- [search_existing_systems](#search-existing-systems)
- [validate_compliance](#validate-compliance)
- [main](#main)

## Functions

### `run_command`
```python
run_command(command, check)
```

Run a command and return the result.

---

### `search_existing_systems`
```python
search_existing_systems(functionality)
```

Run the mandatory production search.

---

### `validate_compliance`
```python
validate_compliance(suggestion)
```

Validate suggestion compliance.

---

### `main`
```python
main()
```

Main workflow function.

---

*Generated on 2025-06-21 20:19:04*