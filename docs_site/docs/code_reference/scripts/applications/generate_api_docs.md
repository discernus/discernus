# Generate Api Docs

**Module:** `scripts.applications.generate_api_docs`
**File:** `/app/scripts/applications/generate_api_docs.py`
**Package:** `applications`

Production API Documentation Generator for Discernus
Automatically generates API documentation from source code and integrates with MkDocs.

This script solves the API documentation challenge by parsing Python files directly,
avoiding the import dependency issues that plagued Sphinx autodoc attempts.

Usage:
    python3 scripts/applications/generate_api_docs.py
    python3 scripts/applications/generate_api_docs.py --modules analysis_service schemas

## Dependencies

- `api_doc_generator`
- `argparse`
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

Main entry point for the production API documentation generator.

---

*Generated on 2025-06-23 10:38:43*