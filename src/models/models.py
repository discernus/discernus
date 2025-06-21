"""
Core database models for Narrative Gravity Analysis.
Implements the 5 core entities: Corpus, Document, Chunk, Job, Task
plus v2.1 enhancements: Experiment, Run for hierarchical analysis
as specified in Epic 1 technical requirements.
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Float, Boolean, 
    ForeignKey, JSON, ARRAY
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from .base import Base


class User(Base):
    """
    User table: Authentication and authorization for API access.
    Implements Epic 1 requirement G: Security & Access Control.
    """
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Role-based access control
    role = Column(String(50), default="user")  # "admin", "user"
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Profile information
    full_name = Column(String(255), nullable=True)
    organization = Column(String(255), nullable=True)
    
    # Security and tracking
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    # API access tracking
    api_key_hash = Column(String(255), nullable=True)  # For API key authentication
    rate_limit_quota = Column(Integer, default=1000)  # Requests per hour
    
    # Relationships
    uploaded_corpora = relationship("Corpus", back_populates="uploader")
    created_jobs = relationship("Job", back_populates="creator")
    experiments = relationship("Experiment", back_populates="creator")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"


class Corpus(Base):
    """
    Corpus table: Container for uploaded document collections.
    """
    __tablename__ = "corpus"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    upload_timestamp = Column(DateTime, default=func.now())
    record_count = Column(Integer, default=0)
    uploader_id = Column(Integer, ForeignKey("user.id"), nullable=True)  # Link to user who uploaded
    description = Column(Text, nullable=True)
    
    # Relationships
    uploader = relationship("User", back_populates="uploaded_corpora")
    documents = relationship("Document", back_populates="corpus", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="corpus", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Corpus(id={self.id}, name='{self.name}', records={self.record_count})>"


class Document(Base):
    """
    Document table: Individual texts with metadata.
    Stores core document-level fields from the universal schema.
    """
    __tablename__ = "document"
    
    id = Column(Integer, primary_key=True, index=True)
    corpus_id = Column(Integer, ForeignKey("corpus.id"), nullable=False)
    
    # Core schema fields (document-level)
    text_id = Column(String(255), nullable=False, unique=True, index=True)
    title = Column(String(500), nullable=False)
    document_type = Column(String(50), nullable=False)  # speech, op_ed, article, etc.
    author = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=False)  # ISO 8601 date
    publication = Column(String(255), nullable=True)
    medium = Column(String(50), nullable=True)  # print, online, TV, radio
    campaign_name = Column(String(255), nullable=True)
    audience_size = Column(Integer, nullable=True)
    source_url = Column(Text, nullable=True)
    schema_version = Column(String(20), nullable=False)
    
    # JSON for flexible metadata and framework extensions
    document_metadata = Column(JSON, default=dict, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    corpus = relationship("Corpus", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Document(id={self.id}, text_id='{self.text_id}', title='{self.title[:50]}...')>"


class Chunk(Base):
    """
    Chunk table: Individual text chunks from documents.
    Stores chunk-level metadata and framework-specific data.
    """
    __tablename__ = "chunk"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("document.id"), nullable=False)
    
    # Core chunk fields from universal schema
    chunk_id = Column(Integer, nullable=False)  # Zero-based index within document
    total_chunks = Column(Integer, nullable=False)
    chunk_type = Column(String(20), nullable=False)  # fixed, sectional, semantic
    chunk_size = Column(Integer, nullable=False)  # Characters in this chunk
    chunk_overlap = Column(Integer, nullable=True)  # Chars overlapping previous
    document_position = Column(Float, nullable=False)  # 0.0-1.0 normalized start
    word_count = Column(Integer, nullable=False)
    unique_words = Column(Integer, nullable=False)
    word_density = Column(Float, nullable=False)  # unique_words / word_count
    chunk_content = Column(Text, nullable=False)
    
    # JSON for framework-specific extensions
    framework_data = Column(JSON, default=dict, nullable=False)
    
    # Processing status
    processing_status = Column(String(20), default="pending")  # pending, processing, completed, failed
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    tasks = relationship("Task", back_populates="chunk", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Chunk(id={self.id}, doc_id={self.document_id}, chunk={self.chunk_id}/{self.total_chunks})>"


class Experiment(Base):
    """
    Experiment table: Research experiments with hypotheses and configurations.
    v2.1 enhancement for hierarchical analysis research workbench.
    """
    __tablename__ = "experiment"
    
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    
    # Experiment metadata
    name = Column(String(255), nullable=False)
    hypothesis = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    research_context = Column(Text, nullable=True)
    
    # Configuration
    prompt_template_id = Column(String(100), nullable=False)  # ID from prompt template store
    framework_config_id = Column(String(100), nullable=False)  # ID from framework config store
    scoring_algorithm_id = Column(String(100), nullable=False)  # Hierarchical, Winner-Take-Most, etc.
    
    # Analysis mode
    analysis_mode = Column(String(50), default="single_model")  # single_model, multi_model_comparison
    selected_models = Column(JSON, nullable=False)  # Array of model names for multi-model
    
    # Status and results
    status = Column(String(20), default="draft")  # draft, active, completed, archived
    total_runs = Column(Integer, default=0)
    successful_runs = Column(Integer, default=0)
    
    # Academic metadata
    research_notes = Column(Text, nullable=True)
    publication_status = Column(String(50), default="unpublished")  # unpublished, submitted, published
    tags = Column(JSON, default=list, nullable=False)  # Research tags for organization
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    creator = relationship("User", back_populates="experiments")
    runs = relationship("Run", back_populates="experiment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Experiment(id={self.id}, name='{self.name}', status='{self.status}')>"


class Run(Base):
    """
    Run table: Individual analysis executions with hierarchical results.
    v2.1 enhancement supporting hierarchical ranking and justifications.
    """
    __tablename__ = "run"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiment.id"), nullable=False)
    
    # Run identification
    run_number = Column(Integer, nullable=False)  # Sequential within experiment
    text_id = Column(String(255), nullable=True)  # Link to original text source
    
    # Input data
    text_content = Column(Text, nullable=False)
    input_length = Column(Integer, nullable=False)  # Character count
    
    # Model and execution metadata
    llm_model = Column(String(100), nullable=False)
    llm_version = Column(String(50), nullable=True)
    prompt_template_version = Column(String(20), nullable=False)
    framework_version = Column(String(20), nullable=False)
    
    # Hierarchical Analysis Results (v2.1)
    raw_scores = Column(JSON, nullable=False)  # Well scores: {"Dignity": 0.7, "Truth": 0.6, ...}
    hierarchical_ranking = Column(JSON, nullable=True)  # Primary/secondary/tertiary wells with weights
    framework_fit_score = Column(Float, nullable=True)  # How well framework fits the text (0.0-1.0)
    
    # Well Justifications (v2.1)
    well_justifications = Column(JSON, nullable=True)  # Detailed LLM reasoning per well
    
    # Calculated Metrics
    narrative_elevation = Column(Float, nullable=True)
    polarity = Column(Float, nullable=True)
    coherence = Column(Float, nullable=True)
    directional_purity = Column(Float, nullable=True)
    narrative_position_x = Column(Float, nullable=True)
    narrative_position_y = Column(Float, nullable=True)
    
    # Execution metadata
    execution_time = Column(DateTime, default=func.now())
    duration_seconds = Column(Float, nullable=True)
    api_cost = Column(Float, nullable=True)
    
    # Raw LLM interaction data
    raw_prompt = Column(Text, nullable=True)  # Complete prompt sent to LLM
    raw_response = Column(Text, nullable=True)  # Complete raw response from LLM
    model_parameters = Column(JSON, nullable=True)  # Temperature, max_tokens, etc.
    
    # Status and error handling
    status = Column(String(20), default="completed")  # pending, running, completed, failed
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    
    # Provenance and audit trail
    complete_provenance = Column(JSON, nullable=False)  # Full traceability data
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    experiment = relationship("Experiment", back_populates="runs")
    
    def __repr__(self):
        return f"<Run(id={self.id}, experiment={self.experiment_id}, model='{self.llm_model}', run={self.run_number})>"


class Job(Base):
    """
    Job table: Batch processing jobs for multiple chunks.
    Enhanced for v2.1 hierarchical analysis compatibility.
    """
    __tablename__ = "job"
    
    id = Column(Integer, primary_key=True, index=True)
    corpus_id = Column(Integer, ForeignKey("corpus.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    experiment_id = Column(Integer, ForeignKey("experiment.id"), nullable=True)  # v2.1: Link to experiment
    
    # Job configuration
    job_name = Column(String(255), nullable=True)
    text_ids = Column(JSON, nullable=False)  # Array of text_id strings to process
    frameworks = Column(JSON, nullable=False)  # Array of framework names
    models = Column(JSON, nullable=False)  # Array of model names/configs
    run_count = Column(Integer, default=5)  # Number of runs per chunk/model combo
    
    # v2.1 Hierarchical Analysis Configuration
    prompt_template_config = Column(JSON, nullable=True)  # Hierarchical prompt configuration
    scoring_algorithm = Column(String(50), default="traditional")  # traditional, hierarchical, winner_take_most
    analysis_mode = Column(String(50), default="single_model")  # single_model, multi_model_comparison
    
    # Job status and metadata
    status = Column(String(20), default="pending")  # pending, running, completed, failed, cancelled
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    failed_tasks = Column(Integer, default=0)
    
    # Cost tracking
    estimated_cost = Column(Float, nullable=True)
    actual_cost = Column(Float, default=0.0)
    
    # Configuration and parameters
    job_config = Column(JSON, default=dict, nullable=False)  # Additional job parameters
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    corpus = relationship("Corpus", back_populates="jobs")
    creator = relationship("User", back_populates="created_jobs")
    experiment = relationship("Experiment")  # Optional link to experiment
    tasks = relationship("Task", back_populates="job", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Job(id={self.id}, status='{self.status}', tasks={self.completed_tasks}/{self.total_tasks})>"


class Task(Base):
    """
    Task table: Individual processing tasks.
    Enhanced for v2.1 hierarchical analysis results.
    """
    __tablename__ = "task"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job.id"), nullable=False)
    chunk_id = Column(Integer, ForeignKey("chunk.id"), nullable=False)
    
    # Task specification
    framework = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    run_number = Column(Integer, nullable=False)  # 1-based run number
    
    # Task status and execution
    status = Column(String(20), default="pending")  # pending, running, completed, failed, retrying
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    
    # v2.1 Enhanced Results Structure
    result_data = Column(JSON, nullable=True)  # Traditional LLM response and analysis results
    hierarchical_result = Column(JSON, nullable=True)  # v2.1: Hierarchical ranking data
    justifications = Column(JSON, nullable=True)  # v2.1: Well justifications and evidence
    
    # Results and error handling
    last_error = Column(Text, nullable=True)
    error_count = Column(Integer, default=0)
    
    # Cost tracking
    api_cost = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    
    # Relationships
    job = relationship("Job", back_populates="tasks")
    chunk = relationship("Chunk", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task(id={self.id}, job={self.job_id}, chunk={self.chunk_id}, {self.framework}, run={self.run_number})>"


# Index definitions for optimal querying
from sqlalchemy import Index

# Composite indexes for common query patterns
Index('idx_document_corpus_textid', Document.corpus_id, Document.text_id)
Index('idx_chunk_document_chunkid', Chunk.document_id, Chunk.chunk_id)
Index('idx_task_job_status', Task.job_id, Task.status)
Index('idx_task_chunk_framework', Task.chunk_id, Task.framework)
Index('idx_job_corpus_status', Job.corpus_id, Job.status)

# JSON indexes for framework data queries (created in migration)
# These will be added via Alembic migration:
# CREATE INDEX idx_chunk_framework_data ON chunk USING gin (framework_data);
# CREATE INDEX idx_task_result_data ON task USING gin (result_data); 