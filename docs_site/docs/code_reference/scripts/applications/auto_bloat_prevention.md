# Auto Bloat Prevention

**Module:** `scripts.applications.auto_bloat_prevention`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/scripts/applications/auto_bloat_prevention.py`
**Package:** `applications`

Auto Bloat Prevention Integration

Integrates bloat prevention directly into the orchestrator and test systems
so cleanup happens automatically without user intervention.

## Dependencies

- `argparse`
- `bloat_prevention_system`
- `logging`
- `os`
- `pathlib`
- `subprocess`
- `sys`
- `test_isolation_system`

## Table of Contents

### Classes
- [AutoBloatPrevention](#autobloatprevention)

### Functions
- [setup_automatic_bloat_prevention](#setup-automatic-bloat-prevention)
- [main](#main)

## Classes

### AutoBloatPrevention

Automatic bloat prevention that integrates with existing systems

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `detect_and_prevent_bloat`
```python
detect_and_prevent_bloat(self)
```

Automatically detect and prevent bloat based on current state

##### `_is_test_environment`
```python
_is_test_environment(self) -> bool
```

Check if running in test environment

##### `_assess_current_bloat`
```python
_assess_current_bloat(self) -> dict
```

Assess current bloat levels and determine if cleanup is needed

##### `install_orchestrator_hooks`
```python
install_orchestrator_hooks(self)
```

Install hooks into orchestrator for automatic cleanup

---

## Functions

### `setup_automatic_bloat_prevention`
```python
setup_automatic_bloat_prevention()
```

Set up automatic bloat prevention in the project

---

### `main`
```python
main()
```

CLI entry point

---

*Generated on 2025-06-21 12:44:48*