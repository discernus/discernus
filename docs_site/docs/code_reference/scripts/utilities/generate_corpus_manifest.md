# Generate Corpus Manifest

**Module:** `scripts.utilities.generate_corpus_manifest`
**File:** `/app/scripts/utilities/generate_corpus_manifest.py`
**Package:** `utilities`

Corpus Hash Manifest Generator

Generates SHA-256 hash manifests for corpus files and collections.
Part of Phase 3: Corpus Management for the comprehensive experiment orchestrator.

Usage:
    python scripts/generate_corpus_manifest.py <path> [options]

## Dependencies

- `argparse`
- `datetime`
- `hashlib`
- `json`
- `pathlib`
- `sys`
- `typing`

## Table of Contents

### Functions
- [calculate_file_hash](#calculate-file-hash)
- [generate_file_manifest](#generate-file-manifest)
- [generate_collection_manifest](#generate-collection-manifest)
- [save_manifest](#save-manifest)
- [validate_manifest](#validate-manifest)
- [main](#main)

## Functions

### `calculate_file_hash`
```python
calculate_file_hash(file_path: Path) -> str
```

Calculate SHA-256 hash of file

---

### `generate_file_manifest`
```python
generate_file_manifest(file_path: Path) -> Dict[Any]
```

Generate manifest for a single file

---

### `generate_collection_manifest`
```python
generate_collection_manifest(directory: Path, pattern: str, recursive: bool) -> Dict[Any]
```

Generate manifest for a collection of files

---

### `save_manifest`
```python
save_manifest(manifest: Dict[Any], output_file: Path, pretty: bool)
```

Save manifest to JSON file

---

### `validate_manifest`
```python
validate_manifest(manifest_file: Path, target_path: Path) -> bool
```

Validate existing manifest against current files

---

### `main`
```python
main()
```

---

*Generated on 2025-06-23 10:38:43*