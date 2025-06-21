# Models

**Module:** `src.models.models`
**File:** `/app/src/models/models.py`
**Package:** `models`

Core database models for Narrative Gravity Analysis.
Implements the 5 core entities: Corpus, Document, Chunk, Job, Task
plus v2.1 enhancements: Experiment, Run for hierarchical analysis
as specified in Epic 1 technical requirements.

## Dependencies

- `base`
- `datetime`
- `sqlalchemy`
- `sqlalchemy.orm`
- `sqlalchemy.sql`
- `uuid`

## Table of Contents

### Classes
- [User](#user)
- [Corpus](#corpus)
- [Document](#document)
- [Chunk](#chunk)
- [Experiment](#experiment)
- [Run](#run)
- [Job](#job)
- [Task](#task)

## Classes

### User
*Inherits from: Base*

User table: Authentication and authorization for API access.
Implements Epic 1 requirement G: Security & Access Control.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

### Corpus
*Inherits from: Base*

Corpus table: Container for uploaded document collections.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

### Document
*Inherits from: Base*

Document table: Individual texts with metadata.
Stores core document-level fields from the universal schema.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

### Chunk
*Inherits from: Base*

Chunk table: Individual text chunks from documents.
Stores chunk-level metadata and framework-specific data.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

### Experiment
*Inherits from: Base*

Experiment table: Research experiments with hypotheses and configurations.
v2.1 enhancement for hierarchical analysis research workbench.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

### Run
*Inherits from: Base*

Run table: Individual analysis executions with hierarchical results.
v2.1 enhancement supporting hierarchical ranking and justifications.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

### Job
*Inherits from: Base*

Job table: Batch processing jobs for multiple chunks.
Enhanced for v2.1 hierarchical analysis compatibility.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

### Task
*Inherits from: Base*

Task table: Individual processing tasks.
Enhanced for v2.1 hierarchical analysis results.

#### Methods

##### `__repr__`
```python
__repr__(self)
```

---

*Generated on 2025-06-21 20:19:04*