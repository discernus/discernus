# Political_Spectrum Framework

**Version:** v2025.06.04  
**Status:** draft  
**Created:** 2025-06-12

## Description

Political Spectrum Framework - updated for circular engine and left-right clustering

## Theoretical Foundation

No theoretical foundation documented.

## Framework Structure

This framework contains 1 dipoles with the following wells:

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
    framework_name="political_spectrum", 
    version="v2025.06.04"
).first()
```

## Development Notes

No development notes.

---
*Generated automatically by framework_sync.py*
