# Generate Comprehensive Docs

**Module:** `scripts.applications.generate_comprehensive_docs`
**File:** `/app/scripts/applications/generate_comprehensive_docs.py`
**Package:** `applications`

Comprehensive Documentation Generator for Discernus
Auto-discovers ALL Python modules and generates complete documentation ecosystem.

This addresses the limitation of the narrow API-only documentation approach
by providing comprehensive coverage similar to Sphinx autodoc but without
the dependency issues.

Usage:
    python3 scripts/applications/generate_comprehensive_docs.py
    python3 scripts/applications/generate_comprehensive_docs.py --include-scripts

## Dependencies

- `argparse`
- `comprehensive_docs_generator`
- `pathlib`
- `sys`

## Table of Contents

### Functions
- [main](#main)

## Functions

### `main`
```python
main()
```

Main entry point for comprehensive documentation generation.

---

*Generated on 2025-06-23 10:38:43*