"""
Component versioning models for Priority 1 infrastructure.
Implements systematic version control for prompt templates, frameworks, and weighting methodologies.
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Float, Boolean, 
    ForeignKey, JSON, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from .base import Base


class PromptTemplate(Base):
    """
    Prompt Templates: Versioned prompt template management.
    Enables systematic prompt engineering with complete version history.
    """
    __tablename__ = "prompt_templates"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    
    # Template content and configuration
    template_content = Column(Text, nullable=False)
    template_type = Column(String(20), default="standard")  # standard, hierarchical
    description = Column(Text, nullable=True)
    
    # Versioning and relationships
    created_by = Column(Integer, ForeignKey("user.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    parent_version_id = Column(String(36), ForeignKey("prompt_templates.id"), nullable=True)
    
    # Performance tracking
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, nullable=True)  # Based on successful runs
    average_cost = Column(Float, nullable=True)  # Average API cost per use
    
    # Development metadata
    development_notes = Column(Text, nullable=True)
    validation_status = Column(String(20), default="draft")  # draft, tested, validated, deprecated
    
    # Relationships
    creator = relationship("User")
    parent_version = relationship("PromptTemplate", remote_side=[id])
    child_versions = relationship("PromptTemplate", remote_side=[parent_version_id], overlaps="parent_version")
    compatibility_entries = relationship("ComponentCompatibility", 
                                       foreign_keys="ComponentCompatibility.prompt_template_id",
                                       overlaps="prompt_template")
    
    # Unique constraint for name + version
    __table_args__ = (UniqueConstraint('name', 'version', name='_prompt_name_version_uc'),)
    
    def __repr__(self):
        return f"<PromptTemplate(name='{self.name}', version='{self.version}', type='{self.template_type}')>"


class FrameworkVersion(Base):
    """
    Framework Versions: Versioned framework configuration management.
    Tracks evolution of framework definitions with complete provenance.
    """
    __tablename__ = "framework_versions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    framework_name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    
    # Framework configuration
    dipoles_json = Column(JSON, nullable=False)  # Complete dipole definitions
    framework_json = Column(JSON, nullable=False)  # Full framework configuration
    description = Column(Text, nullable=True)
    
    # Weighting configuration
    weights_json = Column(JSON, nullable=False)  # Well weights and mathematical parameters
    weighting_rationale = Column(Text, nullable=True)  # Theoretical justification
    
    # Versioning and relationships
    created_by = Column(Integer, ForeignKey("user.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    parent_version_id = Column(String(36), ForeignKey("framework_versions.id"), nullable=True)
    
    # Performance tracking
    usage_count = Column(Integer, default=0)
    average_coherence = Column(Float, nullable=True)  # Average coherence across runs
    framework_fit_average = Column(Float, nullable=True)  # Average framework fit score
    
    # Development metadata
    development_notes = Column(Text, nullable=True)
    validation_status = Column(String(20), default="draft")  # draft, tested, validated, deprecated
    theoretical_foundation = Column(Text, nullable=True)  # Academic basis
    
    # Relationships
    creator = relationship("User")
    parent_version = relationship("FrameworkVersion", remote_side=[id])
    child_versions = relationship("FrameworkVersion", remote_side=[parent_version_id], overlaps="parent_version")
    compatibility_entries = relationship("ComponentCompatibility", 
                                       foreign_keys="ComponentCompatibility.framework_id",
                                       overlaps="framework")
    
    # Unique constraint for framework_name + version
    __table_args__ = (UniqueConstraint('framework_name', 'version', name='_framework_name_version_uc'),)
    
    def __repr__(self):
        return f"<FrameworkVersion(name='{self.framework_name}', version='{self.version}')>"


class WeightingMethodology(Base):
    """
    Weighting Methodologies: Versioned mathematical approaches for narrative positioning.
    Tracks evolution of weighting algorithms with complete mathematical specifications.
    """
    __tablename__ = "weighting_methodologies"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    
    # Mathematical specification
    algorithm_description = Column(Text, nullable=False)
    mathematical_formula = Column(Text, nullable=True)  # LaTeX or plain text formula
    implementation_notes = Column(Text, nullable=True)
    algorithm_type = Column(String(50), nullable=False)  # linear, winner_take_most, exponential, etc.
    
    # Parameters and configuration
    parameters_json = Column(JSON, nullable=False)  # Algorithm-specific parameters
    default_weights = Column(JSON, nullable=True)  # Default weight configuration
    
    # Versioning and relationships
    created_by = Column(Integer, ForeignKey("user.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    parent_version_id = Column(String(36), ForeignKey("weighting_methodologies.id"), nullable=True)
    
    # Performance tracking
    usage_count = Column(Integer, default=0)
    average_polarity = Column(Float, nullable=True)  # Average narrative polarity
    average_elevation = Column(Float, nullable=True)  # Average narrative elevation
    stability_coefficient = Column(Float, nullable=True)  # Cross-run stability
    
    # Development metadata
    development_notes = Column(Text, nullable=True)
    validation_status = Column(String(20), default="draft")
    mathematical_validation = Column(Boolean, default=False)  # Mathematical correctness verified
    
    # Relationships
    creator = relationship("User")
    parent_version = relationship("WeightingMethodology", remote_side=[id])
    child_versions = relationship("WeightingMethodology", remote_side=[parent_version_id], overlaps="parent_version")
    compatibility_entries = relationship("ComponentCompatibility", 
                                       foreign_keys="ComponentCompatibility.weighting_method_id",
                                       overlaps="weighting_method")
    
    # Unique constraint for name + version
    __table_args__ = (UniqueConstraint('name', 'version', name='_weighting_name_version_uc'),)
    
    def __repr__(self):
        return f"<WeightingMethodology(name='{self.name}', version='{self.version}', type='{self.algorithm_type}')>"


class ComponentCompatibility(Base):
    """
    Component Compatibility Matrix: Tracks which components work well together.
    Enables systematic validation of component combinations.
    """
    __tablename__ = "component_compatibility"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Component references
    prompt_template_id = Column(String(36), ForeignKey("prompt_templates.id"), nullable=False)
    framework_id = Column(String(36), ForeignKey("framework_versions.id"), nullable=False)
    weighting_method_id = Column(String(36), ForeignKey("weighting_methodologies.id"), nullable=False)
    
    # Compatibility assessment
    compatibility_score = Column(Float, nullable=True)  # 0.0-1.0 compatibility rating
    validation_status = Column(String(20), default="untested")  # untested, testing, validated, incompatible
    
    # Performance metrics
    average_coherence = Column(Float, nullable=True)
    average_framework_fit = Column(Float, nullable=True)
    cross_run_stability = Column(Float, nullable=True)
    
    # Testing metadata
    test_run_count = Column(Integer, default=0)
    successful_runs = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    
    # Validation tracking
    validated_at = Column(DateTime, nullable=True)
    validated_by = Column(Integer, ForeignKey("user.id"), nullable=True)
    
    # Relationships
    prompt_template = relationship("PromptTemplate", overlaps="compatibility_entries")
    framework = relationship("FrameworkVersion", overlaps="compatibility_entries")
    weighting_method = relationship("WeightingMethodology", overlaps="compatibility_entries")
    validator = relationship("User")
    
    # Unique constraint for component combination
    __table_args__ = (UniqueConstraint('prompt_template_id', 'framework_id', 'weighting_method_id', 
                                      name='_component_combination_uc'),)
    
    def __repr__(self):
        return f"<ComponentCompatibility(score={self.compatibility_score}, status='{self.validation_status}')>"


class DevelopmentSession(Base):
    """
    Development Sessions: Tracks systematic component development workflows.
    Implements structured manual development with hypothesis tracking.
    """
    __tablename__ = "development_sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Session identification
    session_name = Column(String(255), nullable=False)
    component_type = Column(String(50), nullable=False)  # prompt_template, framework, weighting_method
    component_name = Column(String(100), nullable=False)  # Which component being developed
    
    # Session metadata
    hypothesis = Column(Text, nullable=True)  # What we're trying to achieve
    base_version = Column(String(20), nullable=True)  # Starting version for iteration
    target_version = Column(String(20), nullable=True)  # Intended new version
    
    # Development tracking
    researcher = Column(Integer, ForeignKey("user.id"), nullable=True)
    status = Column(String(20), default="active")  # active, completed, abandoned
    
    # Session content
    development_notes = Column(Text, nullable=True)  # Ongoing development notes
    iteration_log = Column(JSON, nullable=False, default=list)  # Array of iteration records
    test_results = Column(JSON, nullable=False, default=dict)  # Testing outcomes
    
    # Outcomes
    success_metrics = Column(JSON, nullable=False, default=dict)  # Performance improvements
    created_version_id = Column(String(36), nullable=True)  # ID of created component version
    lessons_learned = Column(Text, nullable=True)
    
    # Timestamps
    started_at = Column(DateTime, default=func.now())
    last_activity = Column(DateTime, default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    developer = relationship("User")
    
    def __repr__(self):
        return f"<DevelopmentSession(name='{self.session_name}', component='{self.component_type}', status='{self.status}')>"


# Update existing models to support component versioning

# Add foreign key columns to existing Experiment model (via migration)
class ExperimentExtension:
    """
    Extensions to existing Experiment model for component versioning.
    These will be added via Alembic migration.
    """
    # Replace string IDs with foreign key references
    prompt_template_id = Column(String(36), ForeignKey("prompt_templates.id"), nullable=True)
    framework_version_id = Column(String(36), ForeignKey("framework_versions.id"), nullable=True)
    weighting_method_id = Column(String(36), ForeignKey("weighting_methodologies.id"), nullable=True)


# Add foreign key columns to existing Run model (via migration)
class RunExtension:
    """
    Extensions to existing Run model for component versioning.
    These will be added via Alembic migration.
    """
    # Component version tracking
    prompt_template_id = Column(String(36), ForeignKey("prompt_templates.id"), nullable=True)
    framework_version_id = Column(String(36), ForeignKey("framework_versions.id"), nullable=True)
    weighting_method_id = Column(String(36), ForeignKey("weighting_methodologies.id"), nullable=True)
    
    # Enhanced provenance with component versions
    component_provenance = Column(JSON, nullable=True)  # Complete component version tracking 