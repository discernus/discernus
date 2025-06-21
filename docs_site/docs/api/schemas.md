# API Module: Schemas

Pydantic schemas for API request/response validation.
Implements data models for Epic 1 corpus and job management endpoints.
Enhanced for v2.1 hierarchical analysis.

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
- [Config](#config)
- [Config](#config)

### Functions
- [date_to_datetime](#date_to_datetime)
- [validate_frameworks](#validate_frameworks)
- [validate_chunk_consistency](#validate_chunk_consistency)
- [validate_username](#validate_username)
- [validate_email_format](#validate_email_format)
- [validate_email](#validate_email)
- [validate_total_weight](#validate_total_weight)

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
*Inherits from: BaseSchema*

---

### CorpusResponse
*Inherits from: CorpusBase*

---

### DocumentBase
*Inherits from: BaseSchema*

#### Methods

##### date_to_datetime(cls, v)

---

### DocumentResponse
*Inherits from: DocumentBase*

---

### ChunkBase
*Inherits from: BaseSchema*

---

### ChunkResponse
*Inherits from: ChunkBase*

---

### JobCreate
*Inherits from: BaseSchema*

#### Methods

##### validate_frameworks(cls, v)
Validate that frameworks are supported.

---

### JobResponse
*Inherits from: BaseSchema*

---

### TaskResponse
*Inherits from: BaseSchema*

---

### JobDetailResponse
*Inherits from: JobResponse*

Extended job response with task breakdown.

---

### SystemStats
*Inherits from: BaseSchema*

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
*Inherits from: BaseSchema*

Schema for validating individual JSONL records during ingestion.

#### Methods

##### validate_chunk_consistency(cls, v, info: any)
Ensure chunk_id is less than total_chunks.

---

### ErrorResponse
*Inherits from: BaseSchema*

Standard error response format.

---

### ValidationErrorResponse
*Inherits from: BaseSchema*

Detailed validation error for JSONL ingestion.

---

### UserRole
*Inherits from: str, Enum*

---

### UserCreate
*Inherits from: BaseSchema*

Schema for creating a new user.

#### Methods

##### validate_username(cls, v)
Validate username format.

##### validate_email_format(cls, v)
Validate email format using a more robust regex.

---

### UserLogin
*Inherits from: BaseSchema*

Schema for user login.

---

### UserResponse
*Inherits from: BaseSchema*

Schema for user information in responses.

---

### UserUpdate
*Inherits from: BaseSchema*

Schema for updating user information.

#### Methods

##### validate_email(cls, v)
Validate email format.

---

### PasswordChange
*Inherits from: BaseSchema*

Schema for changing password.

---

### TokenResponse
*Inherits from: BaseSchema*

Schema for authentication token response.

---

### TokenRefresh
*Inherits from: BaseSchema*

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

##### validate_total_weight(cls, v)

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

### Config

---

### Config

---

## Functions

### date_to_datetime(cls, v)

---

### validate_frameworks(cls, v)
Validate that frameworks are supported.

---

### validate_chunk_consistency(cls, v, info: any)
Ensure chunk_id is less than total_chunks.

---

### validate_username(cls, v)
Validate username format.

---

### validate_email_format(cls, v)
Validate email format using a more robust regex.

---

### validate_email(cls, v)
Validate email format.

---

### validate_total_weight(cls, v)

---

*Generated on 2025-06-21 11:54:02*