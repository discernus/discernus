# Mft_Persuasive_Force Framework

**Version:** v2025.06.11  
**Status:** draft  
**Created:** 2025-06-12

## Description

MFT Persuasive Force Framework - updated for circular engine and even distribution

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
    framework_name="mft_persuasive_force", 
    version="v2025.06.11"
).first()
```

## Development Notes

No development notes.

---
*Generated automatically by framework_sync.py*
