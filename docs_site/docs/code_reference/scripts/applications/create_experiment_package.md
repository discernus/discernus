# Create Experiment Package

**Module:** `scripts.applications.create_experiment_package`
**File:** `/app/scripts/applications/create_experiment_package.py`
**Package:** `applications`

Experiment Package Generator
Creates standardized, self-contained experiment packages for reproducible research.

Usage:
    python scripts/create_experiment_package.py <experiment_id> [--template=<template>]
    
Examples:
    python scripts/create_experiment_package.py mft_validation_study_20250618
    python scripts/create_experiment_package.py civic_virtue_reliability_study --template=multi_llm

## Dependencies

- `argparse`
- `datetime`
- `json`
- `os`
- `pathlib`
- `shutil`
- `yaml`

## Table of Contents

### Classes
- [ExperimentPackageGenerator](#experimentpackagegenerator)

### Functions
- [main](#main)

## Classes

### ExperimentPackageGenerator

Generates standardized experiment packages for reproducible research.

#### Methods

##### `__init__`
```python
__init__(self, base_dir: str)
```

##### `create_package`
```python
create_package(self, experiment_id: str, template: str, framework: str, description: str)
```

Create a complete experiment package with standardized structure.

##### `_create_directory_structure`
```python
_create_directory_structure(self, package_dir: Path)
```

Create the standardized directory structure.

##### `_create_readme`
```python
_create_readme(self, package_dir: Path, experiment_id: str, framework: str, description: str)
```

Generate comprehensive README documentation.

##### `_create_corpus_manifest`
```python
_create_corpus_manifest(self, package_dir: Path, experiment_id: str, framework: str)
```

Create corpus manifest template.

##### `_create_metadata_files`
```python
_create_metadata_files(self, package_dir: Path, experiment_id: str, framework: str)
```

Create metadata file templates.

##### `_create_basic_config`
```python
_create_basic_config(self, package_dir: Path, experiment_id: str, framework: str)
```

Create basic experiment configuration.

---

## Functions

### `main`
```python
main()
```

Main CLI interface.

---

*Generated on 2025-06-21 20:19:04*