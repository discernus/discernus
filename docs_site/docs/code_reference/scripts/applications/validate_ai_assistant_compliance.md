# Validate Ai Assistant Compliance

**Module:** `scripts.applications.validate_ai_assistant_compliance`
**File:** `/app/scripts/applications/validate_ai_assistant_compliance.py`
**Package:** `applications`

AI Assistant Compliance Validator

Validates that AI assistant suggestions follow mandatory project rules.
Designed to catch violations before they cause problems.

Usage:
    python3 scripts/production/validate_ai_assistant_compliance.py --check-suggestion "build new QA system"
    python3 scripts/production/validate_ai_assistant_compliance.py --audit-recent-changes

## Dependencies

- `argparse`
- `pathlib`
- `subprocess`
- `sys`
- `typing`

## Table of Contents

### Classes
- [AIAssistantComplianceValidator](#aiassistantcompliancevalidator)

### Functions
- [validate_orchestrator_usage](#validate-orchestrator-usage)
- [main](#main)

## Classes

### AIAssistantComplianceValidator

Validates AI assistant compliance with project rules.

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `check_suggestion_compliance`
```python
check_suggestion_compliance(self, suggestion: str) -> Tuple[Any]
```

Check if a suggestion complies with project rules.

##### `audit_recent_file_changes`
```python
audit_recent_file_changes(self) -> Tuple[Any]
```

Audit recent file changes for compliance violations.

##### `check_production_search_performed`
```python
check_production_search_performed(self) -> bool
```

Check if production search was performed recently.

##### `generate_compliance_report`
```python
generate_compliance_report(self, suggestion: str) -> str
```

Generate a comprehensive compliance report.

---

## Functions

### `validate_orchestrator_usage`
```python
validate_orchestrator_usage(suggestion_text: str) -> Dict[Any]
```

🚨 CRITICAL: Prevent AI assistants from suggesting custom scripts!

This function detects violations of the "orchestrator-first" rule where
AI assistants suggest custom scripts for experiment tasks that should
use the production orchestrator.

---

### `main`
```python
main()
```

---

*Generated on 2025-06-23 10:38:43*