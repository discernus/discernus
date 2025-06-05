"""
Pydantic schemas for API request/response validation.
Implements data models for Epic 1 corpus and job management endpoints.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Enums for validation

class DocumentType(str, Enum):
    speech = "speech"
    op_ed = "op_ed"
    article = "article"
    tv_ad_script = "tv_ad_script"
    pamphlet = "pamphlet"
    web_page = "web_page"
    social_media = "social_media"
    other = "other"

class ChunkType(str, Enum):
    fixed = "fixed"
    sectional = "sectional"
    semantic = "semantic"

class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"

class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    retrying = "retrying"

# Base schemas

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# Corpus schemas

class CorpusBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class CorpusResponse(CorpusBase):
    id: int
    upload_timestamp: datetime
    record_count: int
    uploader_id: Optional[str] = None

# Document schemas

class DocumentBase(BaseSchema):
    text_id: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., min_length=1, max_length=500)
    document_type: DocumentType
    author: str = Field(..., min_length=1, max_length=255)
    date: datetime
    publication: Optional[str] = Field(None, max_length=255)
    medium: Optional[str] = Field(None, max_length=50)
    campaign_name: Optional[str] = Field(None, max_length=255)
    audience_size: Optional[int] = Field(None, ge=0)
    source_url: Optional[str] = None
    schema_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    document_metadata: Dict[str, Any] = Field(default_factory=dict)

class DocumentResponse(DocumentBase):
    id: int
    corpus_id: int
    created_at: datetime
    updated_at: datetime

# Chunk schemas

class ChunkBase(BaseSchema):
    chunk_id: int = Field(..., ge=0)
    total_chunks: int = Field(..., ge=1)
    chunk_type: ChunkType
    chunk_size: int = Field(..., ge=1)
    chunk_overlap: Optional[int] = Field(None, ge=0)
    document_position: float = Field(..., ge=0.0, le=1.0)
    word_count: int = Field(..., ge=0)
    unique_words: int = Field(..., ge=0)
    word_density: float = Field(..., ge=0.0, le=1.0)
    chunk_content: str = Field(..., min_length=1)
    framework_data: Dict[str, Any] = Field(default_factory=dict)

class ChunkResponse(ChunkBase):
    id: int
    document_id: int
    processing_status: str
    created_at: datetime
    updated_at: datetime

# Job schemas

class JobCreate(BaseSchema):
    corpus_id: int = Field(..., gt=0)
    job_name: Optional[str] = Field(None, max_length=255)
    text_ids: List[str] = Field(..., min_items=1)
    frameworks: List[str] = Field(..., min_items=1)
    models: List[str] = Field(..., min_items=1)
    run_count: int = Field(default=5, ge=1, le=20)
    job_config: Dict[str, Any] = Field(default_factory=dict)

    @validator('frameworks')
    def validate_frameworks(cls, v):
        """Validate that frameworks are supported."""
        supported = ['civic_virtue', 'moral_rhetorical_posture', 'political_spectrum']
        for framework in v:
            if framework not in supported:
                raise ValueError(f"Unsupported framework: {framework}")
        return v

class JobResponse(BaseSchema):
    id: int
    corpus_id: int
    job_name: Optional[str]
    text_ids: List[str]
    frameworks: List[str]
    models: List[str]
    run_count: int
    status: JobStatus
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    estimated_cost: Optional[float]
    actual_cost: float
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

# Task schemas

class TaskResponse(BaseSchema):
    id: int
    job_id: int
    chunk_id: int
    framework: str
    model: str
    run_number: int
    status: TaskStatus
    attempts: int
    max_attempts: int
    result_data: Optional[Dict[str, Any]]
    last_error: Optional[str]
    error_count: int
    api_cost: Optional[float]
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime]
    finished_at: Optional[datetime]

# Detailed response schemas

class JobDetailResponse(JobResponse):
    """Extended job response with task breakdown."""
    tasks: List[TaskResponse] = []
    task_status_counts: Dict[str, int] = Field(default_factory=dict)
    progress_percentage: float = Field(default=0.0)

# System statistics

class SystemStats(BaseSchema):
    """System-wide statistics for monitoring."""
    total_corpora: int
    total_documents: int
    total_chunks: int
    total_jobs: int
    active_jobs: int
    failed_jobs: int
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    system_health: str
    database_size_mb: Optional[float]
    
# Validation schemas for JSONL ingestion

class JSONLRecord(BaseSchema):
    """Schema for validating individual JSONL records during ingestion."""
    document: DocumentBase
    chunk_id: int = Field(..., ge=0)
    total_chunks: int = Field(..., ge=1)
    chunk_type: ChunkType
    chunk_size: int = Field(..., ge=1)
    chunk_overlap: Optional[int] = Field(None, ge=0)
    document_position: float = Field(..., ge=0.0, le=1.0)
    word_count: int = Field(..., ge=0)
    unique_words: int = Field(..., ge=0)
    word_density: float = Field(..., ge=0.0, le=1.0)
    chunk_content: str = Field(..., min_length=1)
    framework_data: Dict[str, Any] = Field(default_factory=dict)

    @validator('chunk_id', 'total_chunks')
    def validate_chunk_consistency(cls, v, values):
        """Ensure chunk_id is less than total_chunks."""
        if 'chunk_id' in values and 'total_chunks' in values:
            if values['chunk_id'] >= values['total_chunks']:
                raise ValueError("chunk_id must be less than total_chunks")
        return v

# Error response schemas

class ErrorResponse(BaseSchema):
    """Standard error response format."""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ValidationErrorResponse(BaseSchema):
    """Detailed validation error for JSONL ingestion."""
    line_number: int
    error_type: str
    field_errors: Dict[str, List[str]]
    raw_content: Optional[str] = None 