import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class JobStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class AnalysisJob(Base):
    __tablename__ = "reboot_analysis_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    results = relationship("AnalysisResult", back_populates="job")

    def __repr__(self):
        return f"<AnalysisJob(id='{self.id}', status='{self.status}')>"


class AnalysisResult(Base):
    __tablename__ = "reboot_analysis_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, ForeignKey("reboot_analysis_jobs.id"), nullable=False)

    # We can store the full signature if needed, or just the centroid
    centroid_x = Column(Float, nullable=False)
    centroid_y = Column(Float, nullable=False)

    # Storing scores as a JSONB or Text field is better for flexibility
    # For now, let's assume we might want to query them and keep them separate
    # This part can be refactored to a JSONB field later for better performance
    scores = Column(String, nullable=False)  # Store as JSON string

    job = relationship("AnalysisJob", back_populates="results")

    def __repr__(self):
        return f"<AnalysisResult(id={self.id}, job_id='{self.job_id}')>"


# ==============================================================================
# V2 Statistical Comparison Infrastructure Models
# ==============================================================================


class AnalysisJobV2(Base):
    __tablename__ = "analysis_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_type = Column(String(50), nullable=False)
    configuration = Column(String, nullable=False)  # Using String for initial JSON storage
    status = Column(String(20), nullable=False, default='PENDING')
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

    results = relationship("AnalysisResultV2", back_populates="job")

    def __repr__(self):
        return f"<AnalysisJobV2(id='{self.id}', type='{self.job_type}', status='{self.status}')>"


class AnalysisResultV2(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, ForeignKey("analysis_jobs.id"), nullable=False)

    # Analysis Context
    text_content = Column(String, nullable=True)
    text_identifier = Column(String(255), nullable=True)

    # Analysis Configuration
    model = Column(String(100), nullable=False)
    framework = Column(String(100), nullable=False)
    prompt_template = Column(String(100), nullable=False)
    run_number = Column(Integer, default=1, nullable=False)

    # Results
    centroid_x = Column(Float, nullable=False)
    centroid_y = Column(Float, nullable=False)
    raw_scores = Column(String, nullable=False)  # Using String for initial JSON storage

    # Metadata
    api_cost = Column(Float, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    job = relationship("AnalysisJobV2", back_populates="results")

    def __repr__(self):
        return f"<AnalysisResultV2(id={self.id}, job_id='{self.job_id}', model='{self.model}')>"


class StatisticalComparison(Base):
    __tablename__ = "statistical_comparisons"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    comparison_type = Column(String(50), nullable=False)

    # What's being compared
    source_job_ids = Column(String, nullable=False)  # Storing as comma-separated string for now
    comparison_dimension = Column(String(50), nullable=False)

    # Statistical Results
    similarity_metrics = Column(String, nullable=True)  # JSON stored as string
    significance_tests = Column(String, nullable=True)  # JSON stored as string
    confidence_intervals = Column(String, nullable=True) # JSON stored as string

    # Conclusions
    similarity_classification = Column(String(50), nullable=True)
    confidence_level = Column(Float, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<StatisticalComparison(id='{self.id}', type='{self.comparison_type}')>"
