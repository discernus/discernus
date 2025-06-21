# Schemas

**Module:** `src.api.schemas`
**File:** `/Volumes/dev/discernus/src/api/schemas.py`
**Package:** `api`

Pydantic schemas for API request/response validation.
Implements data models for Epic 1 corpus and job management endpoints.
Enhanced for v2.1 hierarchical analysis.

## Dependencies

- `datetime`
- `enum`
- `pydantic`
- `re`
- `typing`

## Table of Contents

### Classes
- [DocumentType](#documenttype)
- [ChunkType](#chunktype)
- [JobStatus](#jobstatus)
- [TaskStatus](#taskstatus)
- [BaseSchema](#baseschema)
- [CorpusBase](#corpusbase)
- [CorpusResponse](#corpusresponse)
- [DocumentBase](#documentbase)
- [DocumentResponse](#documentresponse)
- [ChunkBase](#chunkbase)
- [ChunkResponse](#chunkresponse)
- [JobCreate](#jobcreate)
- [JobResponse](#jobresponse)
- [TaskResponse](#taskresponse)
- [JobDetailResponse](#jobdetailresponse)
- [SystemStats](#systemstats)
- [FrameworkConfigResponse](#frameworkconfigresponse)
- [PromptTemplateResponse](#prompttemplateresponse)
- [ScoringAlgorithmResponse](#scoringalgorithmresponse)
- [JSONLRecord](#jsonlrecord)
- [ErrorResponse](#errorresponse)
- [ValidationErrorResponse](#validationerrorresponse)
- [UserRole](#userrole)
- [UserCreate](#usercreate)
- [UserLogin](#userlogin)
- [UserResponse](#userresponse)
- [UserUpdate](#userupdate)
- [PasswordChange](#passwordchange)
- [TokenResponse](#tokenresponse)
- [TokenRefresh](#tokenrefresh)
- [WellJustification](#welljustification)
- [HierarchicalRanking](#hierarchicalranking)
- [CalculatedMetrics](#calculatedmetrics)
- [NarrativePosition](#narrativeposition)
- [CompleteProvenance](#completeprovenance)
- [ExperimentCreate](#experimentcreate)
- [ExperimentUpdate](#experimentupdate)
- [ExperimentResponse](#experimentresponse)
- [RunCreate](#runcreate)
- [RunResponse](#runresponse)
- [SingleTextAnalysisRequest](#singletextanalysisrequest)
- [SingleTextAnalysisResponse](#singletextanalysisresponse)
- [MultiModelAnalysisRequest](#multimodelanalysisrequest)
- [ModelComparisonResult](#modelcomparisonresult)
- [MultiModelAnalysisResponse](#multimodelanalysisresponse)

## Classes

### DocumentType
*Inherits from: str, Enum*

---

### ChunkType
*Inherits from: str, Enum*

---

### JobStatus
*Inherits from: str, Enum*

---

### TaskStatus
*Inherits from: str, Enum*

---

### BaseSchema
*Inherits from: BaseModel*

---

### CorpusBase
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

---

### CorpusResponse
*Inherits from: [CorpusBase](src/api/schemas.md#corpusbase)*

---

### DocumentBase
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

#### Methods

##### `date_to_datetime`
```python
date_to_datetime(cls, v)
```

---

### DocumentResponse
*Inherits from: [DocumentBase](src/api/schemas.md#documentbase)*

---

### ChunkBase
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

---

### ChunkResponse
*Inherits from: [ChunkBase](src/api/schemas.md#chunkbase)*

---

### JobCreate
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

#### Methods

##### `validate_frameworks`
```python
validate_frameworks(cls, v)
```

Validate that frameworks are supported.

---

### JobResponse
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

---

### TaskResponse
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

---

### JobDetailResponse
*Inherits from: [JobResponse](src/api/schemas.md#jobresponse)*

Extended job response with task breakdown.

---

### SystemStats
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

System-wide statistics for monitoring.

---

### FrameworkConfigResponse
*Inherits from: BaseModel*

Schema for framework configuration response.

---

### PromptTemplateResponse
*Inherits from: BaseModel*

Schema for prompt template response.

---

### ScoringAlgorithmResponse
*Inherits from: BaseModel*

Schema for scoring algorithm response.

---

### JSONLRecord
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

Schema for validating individual JSONL records during ingestion.

#### Methods

##### `validate_chunk_consistency`
```python
validate_chunk_consistency(cls, v, info: any)
```

Ensure chunk_id is less than total_chunks.

---

### ErrorResponse
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

Standard error response format.

---

### ValidationErrorResponse
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

Detailed validation error for JSONL ingestion.

---

### UserRole
*Inherits from: str, Enum*

---

### UserCreate
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

Schema for creating a new user.

#### Methods

##### `validate_username`
```python
validate_username(cls, v)
```

Validate username format.

##### `validate_email_format`
```python
validate_email_format(cls, v)
```

Validate email format using a more robust regex.

---

### UserLogin
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

Schema for user login.

---

### UserResponse
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

Schema for user information in responses.

---

### UserUpdate
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

Schema for updating user information.

#### Methods

##### `validate_email`
```python
validate_email(cls, v)
```

Validate email format.

---

### PasswordChange
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

Schema for changing password.

---

### TokenResponse
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

Schema for authentication token response.

---

### TokenRefresh
*Inherits from: [BaseSchema](src/api/schemas.md#baseschema)*

Schema for token refresh request.

---

### WellJustification
*Inherits from: BaseModel*

Individual well justification with LLM reasoning.

---

### HierarchicalRanking
*Inherits from: BaseModel*

Hierarchical ranking of wells with relative weights.

#### Methods

##### `validate_total_weight`
```python
validate_total_weight(cls, v)
```

---

### CalculatedMetrics
*Inherits from: BaseModel*

Calculated narrative metrics.

---

### NarrativePosition
*Inherits from: BaseModel*

2D narrative position coordinates.

---

### CompleteProvenance
*Inherits from: BaseModel*

Complete provenance and audit trail.

---

### ExperimentCreate
*Inherits from: BaseModel*

Schema for creating a new experiment.

---

### ExperimentUpdate
*Inherits from: BaseModel*

Schema for updating an experiment.

---

### ExperimentResponse
*Inherits from: BaseModel*

Schema for experiment responses.

---

### RunCreate
*Inherits from: BaseModel*

Schema for creating a new analysis run.

---

### RunResponse
*Inherits from: BaseModel*

Schema for run responses with hierarchical results.

---

### SingleTextAnalysisRequest
*Inherits from: BaseModel*

Enhanced request schema for single text analysis.

---

### SingleTextAnalysisResponse
*Inherits from: BaseModel*

Enhanced response schema for single text analysis.

---

### MultiModelAnalysisRequest
*Inherits from: BaseModel*

Request schema for multi-model comparison analysis.

---

### ModelComparisonResult
*Inherits from: BaseModel*

Individual model result in multi-model comparison.

---

### MultiModelAnalysisResponse
*Inherits from: BaseModel*

Response schema for multi-model comparison analysis.

---

*Generated on 2025-06-21 18:56:11*