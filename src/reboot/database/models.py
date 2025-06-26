import enum
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Enum
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
    __tablename__ = 'reboot_analysis_jobs'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    results = relationship("AnalysisResult", back_populates="job")

    def __repr__(self):
        return f"<AnalysisJob(id='{self.id}', status='{self.status}')>"

class AnalysisResult(Base):
    __tablename__ = 'reboot_analysis_results'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, ForeignKey('reboot_analysis_jobs.id'), nullable=False)
    
    # We can store the full signature if needed, or just the centroid
    centroid_x = Column(Float, nullable=False)
    centroid_y = Column(Float, nullable=False)
    
    # Storing scores as a JSONB or Text field is better for flexibility
    # For now, let's assume we might want to query them and keep them separate
    # This part can be refactored to a JSONB field later for better performance
    scores = Column(String, nullable=False) # Store as JSON string
    
    job = relationship("AnalysisJob", back_populates="results")

    def __repr__(self):
        return f"<AnalysisResult(id={self.id}, job_id='{self.job_id}')>" 