# Component Models

**Module:** `src.models.component_models`
**File:** `/app/src/models/component_models.py`
**Package:** `models`

Component versioning models for Priority 1 infrastructure.
Implements systematic version control for prompt templates, frameworks, and weighting methodologies.

## Dependencies

- `base`
- `datetime`
- `sqlalchemy`
- `sqlalchemy.orm`
- `sqlalchemy.sql`
- `uuid`

## Table of Contents

### Classes
- [PromptTemplate](#prompttemplate)
- [FrameworkVersion](#frameworkversion)
- [WeightingMethodology](#weightingmethodology)
- [ComponentCompatibility](#componentcompatibility)
- [DevelopmentSession](#developmentsession)
- [ExperimentExtension](#experimentextension)
- [RunExtension](#runextension)

## Classes

### PromptTemplate
*Inherits from: Base*

Prompt Templates: Versioned prompt template management.
Enables systematic prompt engineering with complete version history.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

### FrameworkVersion
*Inherits from: Base*

Framework Versions: Versioned framework configuration management.
Tracks evolution of framework definitions with complete provenance.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

### WeightingMethodology
*Inherits from: Base*

Weighting Methodologies: Versioned mathematical approaches for narrative positioning.
Tracks evolution of weighting algorithms with complete mathematical specifications.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

### ComponentCompatibility
*Inherits from: Base*

Component Compatibility Matrix: Tracks which components work well together.
Enables systematic validation of component combinations.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

### DevelopmentSession
*Inherits from: Base*

Development Sessions: Tracks systematic component development workflows.
Implements structured manual development with hypothesis tracking.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

### ExperimentExtension

Extensions to existing Experiment model for component versioning.
These will be added via Alembic migration.

---

### RunExtension

Extensions to existing Run model for component versioning.
These will be added via Alembic migration.

---

*Generated on 2025-06-23 10:38:43*