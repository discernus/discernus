# Civic_Virtue Framework

**Version:** v2025.06.14  
**Status:** draft  
**Created:** 2025-06-14

## Description

Civic Virtue Framework - A specialized Narrative Gravity Map implementation for moral analysis of persuasive political discourse

## Theoretical Foundation

No theoretical foundation documented.

## Framework Structure

This framework contains 5 dipoles with the following wells:

Wells structure not recognized.

## Files

- `framework.json`: Complete framework configuration
- `dipoles.json`: Dipole and well definitions  
- `weights.json`: Mathematical weighting configuration
- `README.md`: This documentation file

## Usage

This framework is stored in the database as the source of truth. To use:

```python
from narrative_gravity.models.component_models import FrameworkVersion
framework = session.query(FrameworkVersion).filter_by(
    framework_name="civic_virtue", 
    version="v2025.06.14"
).first()
```

## Development Notes

No development notes.

---
*Generated automatically by framework_sync.py*
