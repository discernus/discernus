# Check Existing Systems

**Module:** `scripts.applications.check_existing_systems`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/scripts/applications/check_existing_systems.py`
**Package:** `applications`

Check Existing Systems - Production-First Search

Run this script before building any new functionality to see if we already
have something that does what you want to build.

Uses clean search strategy:
1. Search PRODUCTION code first (src/, scripts/production/, docs/specifications/)
2. Only search experimental if no production matches found
3. Never search deprecated code unless explicitly requested

Usage:
    python3 scripts/production/check_existing_systems.py "quality assurance"
    python3 scripts/production/check_existing_systems.py "experiment execution"
    python3 scripts/production/check_existing_systems.py "data export" --include-experimental

## Dependencies

- `argparse`
- `pathlib`
- `subprocess`
- `sys`

## Table of Contents

### Classes
- [ProductionCodeSearcher](#productioncodesearcher)

### Functions
- [show_inventory](#show-inventory)
- [main](#main)

## Classes

### ProductionCodeSearcher

Clean search focusing on production-ready code.

#### Methods

##### `__init__`
```python
__init__(self, include_experimental, include_deprecated)
```

##### `search_production_code`
```python
search_production_code(self, query: str)
```

Search production code directories first.

##### `search_experimental_code`
```python
search_experimental_code(self, query: str)
```

Search experimental code if no production matches.

##### `search_deprecated_code`
```python
search_deprecated_code(self, query: str)
```

Search deprecated code (only if explicitly requested).

---

## Functions

### `show_inventory`
```python
show_inventory()
```

Show the existing systems inventory.

---

### `main`
```python
main()
```

---

*Generated on 2025-06-21 12:44:48*