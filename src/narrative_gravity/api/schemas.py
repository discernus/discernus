"""
Pydantic schemas for API request/response validation.
Implements data models for Epic 1 corpus and job management endpoints.
Enhanced for v2.1 hierarchical analysis.
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict, validator
from typing import List, Optional, Dict, Any, Union
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
    model_config = ConfigDict(from_attributes=True)

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
    date: Union[datetime, str]
    publication: Optional[str] = Field(None, max_length=255)
    medium: Optional[str] = Field(None, max_length=50)
    campaign_name: Optional[str] = Field(None, max_length=255)
    audience_size: Optional[int] = Field(None, ge=0)
    source_url: Optional[str] = None
    schema_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    document_metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('date', mode='before')
    def date_to_datetime(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Invalid ISO 8601 date format")
        return v

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
    text_ids: List[str] = Field(..., min_length=1)
    frameworks: List[str] = Field(..., min_length=1)
    models: List[str] = Field(..., min_length=1)
    run_count: int = Field(default=5, ge=1, le=20)
    job_config: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('frameworks')
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
    
# Configuration schemas for v2.1 frontend

class FrameworkConfigResponse(BaseModel):
    """Schema for framework configuration response."""
    id: str = Field(..., description="Framework identifier")
    name: str = Field(..., description="Framework display name")  
    version: str = Field(..., description="Framework version")
    description: str = Field(..., description="Framework description")
    dipoles: List[Dict[str, Any]] = Field(..., description="Framework dipole configuration")

class PromptTemplateResponse(BaseModel):
    """Schema for prompt template response."""
    id: str = Field(..., description="Template identifier")
    name: str = Field(..., description="Template display name")
    version: str = Field(..., description="Template version")
    content: str = Field(..., description="Template content")
    framework_compatibility: List[str] = Field(default_factory=list, description="Compatible frameworks")

class ScoringAlgorithmResponse(BaseModel):
    """Schema for scoring algorithm response."""
    id: str = Field(..., description="Algorithm identifier")
    name: str = Field(..., description="Algorithm display name")
    description: str = Field(..., description="Algorithm description")
    version: str = Field(..., description="Algorithm version")
    
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

    @field_validator('chunk_id')
    def validate_chunk_consistency(cls, v, info: any):
        """Ensure chunk_id is less than total_chunks."""
        if 'total_chunks' in info.data and v >= info.data['total_chunks']:
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

# Authentication schemas

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserCreate(BaseSchema):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, max_length=255)
    organization: Optional[str] = Field(None, max_length=255)
    role: 'UserRole' = Field(default='user')

    @field_validator('username')
    def validate_username(cls, v):
        """Validate username format."""
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens")
        return v

    @field_validator('email')
    def validate_email_format(cls, v):
        """Validate email format using a more robust regex."""
        import re
        # A regex that is compliant with most modern email address standards
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", v):
            raise ValueError("Invalid email format")
        return v

class UserLogin(BaseSchema):
    """Schema for user login."""
    username: str = Field(..., max_length=255)
    password: str = Field(..., max_length=128)

class UserResponse(BaseSchema):
    """Schema for user information in responses."""
    id: int
    username: str
    email: str
    full_name: Optional[str]
    organization: Optional[str]
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]
    rate_limit_quota: int

class UserUpdate(BaseSchema):
    """Schema for updating user information."""
    full_name: Optional[str] = Field(None, max_length=255)
    organization: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = Field(None, max_length=255)

    @field_validator('email')
    def validate_email(cls, v):
        """Validate email format."""
        if v:
            import re
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
                raise ValueError("Invalid email format")
            return v.lower()
        return v

class PasswordChange(BaseSchema):
    """Schema for changing password."""
    current_password: str = Field(..., max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)

class TokenResponse(BaseSchema):
    """Schema for authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class TokenRefresh(BaseSchema):
    """Schema for token refresh request."""
    refresh_token: str

# v2.1 Hierarchical Analysis Schemas

class WellJustification(BaseModel):
    """Individual well justification with LLM reasoning."""
    score: float = Field(..., ge=0.0, le=1.0, description="Well score (0.0-1.0)")
    reasoning: str = Field(..., description="LLM reasoning for this score")
    evidence_quotes: List[str] = Field(default_factory=list, description="Supporting quotes from text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="LLM confidence in this assessment")

class HierarchicalRanking(BaseModel):
    """Hierarchical ranking of wells with relative weights."""
    primary_wells: List[Dict[str, Union[str, float]]] = Field(..., description="Top 2-3 driving wells with weights")
    secondary_wells: List[Dict[str, Union[str, float]]] = Field(default_factory=list, description="Supporting wells")
    total_weight: float = Field(100.0, description="Total weight should sum to 100%")
    
    @validator('total_weight')
    def validate_total_weight(cls, v):
        if not (99.0 <= v <= 101.0):  # Allow small floating point errors
            raise ValueError('Total weight must sum to approximately 100%')
        return v

class CalculatedMetrics(BaseModel):
    """Calculated narrative metrics."""
    narrative_elevation: float = Field(..., description="Overall narrative elevation score")
    polarity: float = Field(..., description="Narrative polarity (-1.0 to 1.0)")
    coherence: float = Field(..., description="Narrative coherence score")
    directional_purity: float = Field(..., description="Directional purity score")

class NarrativePosition(BaseModel):
    """2D narrative position coordinates."""
    x: float = Field(..., description="X coordinate in narrative space")
    y: float = Field(..., description="Y coordinate in narrative space")

class CompleteProvenance(BaseModel):
    """Complete provenance and audit trail."""
    prompt_template_hash: str = Field(..., description="Hash of prompt template used")
    framework_version: str = Field(..., description="Framework version identifier")
    scoring_algorithm_version: str = Field(..., description="Scoring algorithm version")
    llm_model: str = Field(..., description="LLM model identifier")
    timestamp: str = Field(..., description="ISO timestamp of analysis")
    experiment_id: Optional[int] = Field(None, description="Associated experiment ID")

# Experiment Schemas

class ExperimentCreate(BaseModel):
    """Schema for creating a new experiment."""
    name: str = Field(..., max_length=255, description="Experiment name")
    hypothesis: Optional[str] = Field(None, description="Research hypothesis")
    description: Optional[str] = Field(None, description="Experiment description")
    research_context: Optional[str] = Field(None, description="Research context and background")
    
    # Configuration
    prompt_template_id: str = Field(..., description="Prompt template identifier")
    framework_config_id: str = Field(..., description="Framework configuration identifier")
    scoring_algorithm_id: str = Field(..., description="Scoring algorithm identifier")
    
    # Analysis mode
    analysis_mode: str = Field(default="single_model", description="Analysis mode")
    selected_models: List[str] = Field(..., description="Selected LLM models")
    
    # Academic metadata
    research_notes: Optional[str] = Field(None, description="Research notes")
    tags: List[str] = Field(default_factory=list, description="Research tags")

class ExperimentUpdate(BaseModel):
    """Schema for updating an experiment."""
    name: Optional[str] = Field(None, max_length=255)
    hypothesis: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    research_context: Optional[str] = Field(None)
    research_notes: Optional[str] = Field(None)
    publication_status: Optional[str] = Field(None)
    tags: Optional[List[str]] = Field(None)
    status: Optional[str] = Field(None)

class ExperimentResponse(BaseModel):
    """Schema for experiment responses."""
    id: int
    creator_id: Optional[int]
    name: str
    hypothesis: Optional[str]
    description: Optional[str]
    research_context: Optional[str]
    
    # Configuration
    prompt_template_id: str
    framework_config_id: str
    scoring_algorithm_id: str
    analysis_mode: str
    selected_models: List[str]
    
    # Status and results
    status: str
    total_runs: int
    successful_runs: int
    
    # Academic metadata
    research_notes: Optional[str]
    publication_status: str
    tags: List[str]
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Run Schemas

class RunCreate(BaseModel):
    """Schema for creating a new analysis run."""
    text_content: str = Field(..., description="Text to analyze")
    text_id: Optional[str] = Field(None, description="Optional text identifier")
    llm_model: str = Field(..., description="LLM model to use")
    llm_version: Optional[str] = Field(None, description="LLM version")

class RunResponse(BaseModel):
    """Schema for run responses with hierarchical results."""
    id: int
    experiment_id: int
    run_number: int
    text_id: Optional[str]
    text_content: str
    input_length: int
    
    # Model and execution metadata
    llm_model: str
    llm_version: Optional[str]
    prompt_template_version: str
    framework_version: str
    
    # Hierarchical Analysis Results
    raw_scores: Dict[str, float]
    hierarchical_ranking: Optional[HierarchicalRanking]
    framework_fit_score: Optional[float]
    well_justifications: Optional[Dict[str, WellJustification]]
    
    # Calculated Metrics
    narrative_elevation: Optional[float]
    polarity: Optional[float]
    coherence: Optional[float]
    directional_purity: Optional[float]
    narrative_position_x: Optional[float]
    narrative_position_y: Optional[float]
    
    # Execution metadata
    execution_time: datetime
    duration_seconds: Optional[float]
    api_cost: Optional[float]
    
    # Status
    status: str
    success: bool
    error_message: Optional[str]
    
    # Provenance
    complete_provenance: CompleteProvenance
    
    # Timestamps
    created_at: datetime
    
    class Config:
        from_attributes = True

# Enhanced Analysis Request/Response Schemas

class SingleTextAnalysisRequest(BaseModel):
    """Enhanced request schema for single text analysis."""
    text_content: str = Field(..., description="Text to analyze")
    experiment_id: Optional[int] = Field(None, description="Optional experiment association")
    
    # Configuration
    prompt_template_id: str = Field(..., description="Prompt template to use")
    framework_config_id: str = Field(..., description="Framework configuration to use")
    scoring_algorithm_id: str = Field(..., description="Scoring algorithm to use")
    
    # Model configuration
    llm_model: str = Field(..., description="LLM model to use")
    model_parameters: Optional[Dict[str, Any]] = Field(None, description="Model parameters")
    
    # Analysis options
    include_justifications: bool = Field(True, description="Include well justifications")
    include_hierarchical_ranking: bool = Field(True, description="Include hierarchical ranking")

class SingleTextAnalysisResponse(BaseModel):
    """Enhanced response schema for single text analysis."""
    analysis_id: str = Field(..., description="Unique analysis identifier")
    text_content: str = Field(..., description="Analyzed text")
    
    # Configuration used
    framework: str = Field(..., description="Framework used")
    model: str = Field(..., description="Model used")
    
    # Results
    raw_scores: Dict[str, float] = Field(..., description="Raw well scores")
    hierarchical_ranking: Optional[HierarchicalRanking] = Field(None, description="Hierarchical ranking")
    well_justifications: Optional[Dict[str, WellJustification]] = Field(None, description="Well justifications")
    
    # Calculated metrics
    calculated_metrics: CalculatedMetrics = Field(..., description="Calculated narrative metrics")
    narrative_position: NarrativePosition = Field(..., description="2D narrative position")
    
    # Analysis metadata
    framework_fit_score: float = Field(..., description="Framework fit score")
    dominant_wells: List[Dict[str, Union[str, float]]] = Field(..., description="Top dominant wells")
    
    # Execution metadata
    execution_time: datetime = Field(..., description="Analysis execution time")
    duration_seconds: Optional[float] = Field(None, description="Analysis duration")
    api_cost: Optional[float] = Field(None, description="API cost")

# Multi-Model Comparison Schemas

class MultiModelAnalysisRequest(BaseModel):
    """Request schema for multi-model comparison analysis."""
    text_content: str = Field(..., description="Text to analyze")
    experiment_id: Optional[int] = Field(None, description="Optional experiment association")
    
    # Configuration
    prompt_template_id: str = Field(..., description="Prompt template to use")
    framework_config_id: str = Field(..., description="Framework configuration to use")
    scoring_algorithm_id: str = Field(..., description="Scoring algorithm to use")
    
    # Multi-model configuration
    selected_models: List[str] = Field(..., description="Models to compare")
    runs_per_model: int = Field(default=3, description="Number of runs per model")

class ModelComparisonResult(BaseModel):
    """Individual model result in multi-model comparison."""
    model: str = Field(..., description="Model identifier")
    runs: List[RunResponse] = Field(..., description="Individual runs for this model")
    
    # Aggregated statistics
    mean_scores: Dict[str, float] = Field(..., description="Mean scores across runs")
    score_variance: Dict[str, float] = Field(..., description="Score variance across runs")
    consistency_score: float = Field(..., description="Model consistency score")

class MultiModelAnalysisResponse(BaseModel):
    """Response schema for multi-model comparison analysis."""
    analysis_id: str = Field(..., description="Unique analysis identifier")
    text_content: str = Field(..., description="Analyzed text")
    
    # Configuration
    framework: str = Field(..., description="Framework used")
    scoring_algorithm: str = Field(..., description="Scoring algorithm used")
    
    # Results by model
    model_results: List[ModelComparisonResult] = Field(..., description="Results by model")
    
    # Cross-model analysis
    model_agreement: Dict[str, float] = Field(..., description="Inter-model agreement scores")
    consensus_scores: Dict[str, float] = Field(..., description="Consensus scores across models")
    stability_metrics: Dict[str, Any] = Field(..., description="Stability analysis metrics")
    
    # Execution metadata
    total_runs: int = Field(..., description="Total number of runs")
    total_cost: float = Field(..., description="Total API cost")
    execution_time: datetime = Field(..., description="Analysis start time") 