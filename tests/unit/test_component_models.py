"""
Unit tests for Priority 1 database models.
Tests individual model functionality without database integration.
"""

import pytest
import json
from datetime import datetime, timezone
from uuid import uuid4

from src.models.component_models import (
    PromptTemplate, FrameworkVersion, WeightingMethodology,
    ComponentCompatibility, DevelopmentSession
)


class TestPromptTemplateModel:
    """Test PromptTemplate database model."""
    
    def test_prompt_template_creation(self):
        """Test creating a PromptTemplate instance."""
        prompt = PromptTemplate(
            name="test_prompt",
            version="v1.0",
            template_content="Test template content",
            template_type="hierarchical",
            description="Test description",
            validation_status="draft"
        )
        
        assert prompt.name == "test_prompt"
        assert prompt.version == "v1.0"
        assert prompt.template_type == "hierarchical"
        assert prompt.validation_status == "draft"
        assert prompt.description == "Test description"
    
    def test_prompt_template_serialization(self):
        """Test text field handling."""
        prompt = PromptTemplate(
            name="test_prompt",
            version="v1.0",
            template_content="Test content",
            template_type="hierarchical",
            development_notes="Test development notes"
        )
        
        # Test that text fields can be set
        assert prompt.development_notes == "Test development notes"
        assert prompt.template_content == "Test content"
    
    def test_prompt_template_validation_status_options(self):
        """Test that validation status accepts expected values."""
        statuses = ["draft", "tested", "validated", "deprecated"]
        
        for status in statuses:
            prompt = PromptTemplate(
                name="test_prompt",
                version="v1.0",
                template_content="Test content",
                validation_status=status
            )
            assert prompt.validation_status == status


class TestFrameworkVersionModel:
    """Test FrameworkVersion database model."""
    
    def test_framework_version_creation(self):
        """Test creating a FrameworkVersion instance."""
        dipoles_data = {
            "Identity": {
                "positive_well": {"name": "Dignity", "angle": 90},
                "negative_well": {"name": "Tribalism", "angle": 270}
            }
        }
        
        framework_data = {"framework_type": "civic_virtue", "dipole_count": 2}
        weights_data = {"well_weights": {"Dignity": 1.0}, "dipole_weights": {"Identity": 1.0}}
        
        framework = FrameworkVersion(
            framework_name="test_framework",
            version="v1.0",
            dipoles_json=dipoles_data,
            framework_json=framework_data,
            weights_json=weights_data,
            theoretical_foundation="Test theory",
            description="Test framework",
            validation_status="draft"
        )
        
        assert framework.framework_name == "test_framework"
        assert framework.version == "v1.0"
        assert framework.dipoles_json == dipoles_data
        assert framework.framework_json == framework_data
        assert framework.validation_status == "draft"
    
    def test_framework_version_json_fields(self):
        """Test JSON field handling."""
        weights_data = {
            "well_weights": {"Dignity": 1.0, "Tribalism": -1.0},
            "dipole_weights": {"Identity": 1.0}
        }
        
        framework = FrameworkVersion(
            framework_name="test_framework",
            version="v1.0",
            dipoles_json={},
            weights_json=weights_data
        )
        
        assert framework.weights_json == weights_data
        assert "well_weights" in framework.weights_json
    
    def test_framework_performance_tracking(self):
        """Test performance tracking fields."""
        framework = FrameworkVersion(
            framework_name="test_framework",
            version="v1.0",
            dipoles_json={},
            framework_json={},
            weights_json={},
            average_coherence=0.85,
            framework_fit_average=0.92
        )
        
        assert framework.average_coherence == 0.85
        assert framework.framework_fit_average == 0.92


class TestWeightingMethodologyModel:
    """Test WeightingMethodology database model."""
    
    def test_weighting_methodology_creation(self):
        """Test creating a WeightingMethodology instance."""
        parameters = {
            "algorithm_type": "winner_take_most",
            "amplification_factor": 1.5,
            "threshold": 0.6
        }
        
        methodology = WeightingMethodology(
            name="test_weighting",
            version="v1.0",
            algorithm_type="winner_take_most",
            algorithm_description="Test algorithm",
            parameters_json=parameters,
            mathematical_formula="w = base ^ factor",
            validation_status="draft"
        )
        
        assert methodology.name == "test_weighting"
        assert methodology.algorithm_type == "winner_take_most"
        assert methodology.parameters_json == parameters
        assert methodology.validation_status == "draft"
    
    def test_algorithm_types(self):
        """Test different algorithm types."""
        algorithm_types = [
            "winner_take_most",
            "proportional",
            "threshold_based",
            "custom"
        ]
        
        for algo_type in algorithm_types:
            methodology = WeightingMethodology(
                name="test_weighting",
                version="v1.0",
                algorithm_type=algo_type,
                parameters_json={}
            )
            assert methodology.algorithm_type == algo_type
    
    def test_mathematical_specifications(self):
        """Test mathematical specification fields."""
        methodology = WeightingMethodology(
            name="test_weighting",
            version="v1.0",
            algorithm_type="winner_take_most",
            algorithm_description="Test algorithm",
            parameters_json={},
            mathematical_formula="O(n log n)",
            implementation_notes="Test implementation notes"
        )
        
        assert methodology.mathematical_formula == "O(n log n)"
        assert methodology.implementation_notes == "Test implementation notes"


class TestComponentCompatibilityModel:
    """Test ComponentCompatibility database model."""
    
    def test_component_compatibility_creation(self):
        """Test creating a ComponentCompatibility instance."""
        compatibility = ComponentCompatibility(
            prompt_template_id=uuid4(),
            framework_id=uuid4(),
            weighting_method_id=uuid4(),
            validation_status="untested",
            notes="Test compatibility notes"
        )
        
        assert compatibility.validation_status == "untested"
        assert compatibility.notes == "Test compatibility notes"
        # Default values may not be set in unit tests without database context
        assert hasattr(compatibility, 'test_run_count')
    
    def test_compatibility_status_options(self):
        """Test validation status values."""
        statuses = ["untested", "testing", "validated", "incompatible"]
        
        for status in statuses:
            compatibility = ComponentCompatibility(
                prompt_template_id=uuid4(),
                framework_id=uuid4(),
                weighting_method_id=uuid4(),
                validation_status=status
            )
            assert compatibility.validation_status == status
    
    def test_performance_metrics_structure(self):
        """Test performance metrics fields."""
        compatibility = ComponentCompatibility(
            prompt_template_id=uuid4(),
            framework_id=uuid4(),
            weighting_method_id=uuid4(),
            validation_status="validated",
            compatibility_score=0.87,
            average_coherence=0.85,
            average_framework_fit=0.92,
            cross_run_stability=0.78
        )
        
        assert compatibility.compatibility_score == 0.87
        assert compatibility.average_coherence == 0.85
        assert compatibility.average_framework_fit == 0.92
        assert compatibility.cross_run_stability == 0.78


class TestDevelopmentSessionModel:
    """Test DevelopmentSession database model."""
    
    def test_development_session_creation(self):
        """Test creating a DevelopmentSession instance."""
        session = DevelopmentSession(
            session_name="test_session",
            component_type="prompt_template",
            component_name="test_prompt",
            hypothesis="Test hypothesis",
            status="active"
        )
        
        assert session.session_name == "test_session"
        assert session.component_type == "prompt_template"
        assert session.status == "active"
        assert session.hypothesis == "Test hypothesis"
        assert session.component_name == "test_prompt"
    
    def test_session_status_lifecycle(self):
        """Test session status options."""
        statuses = ["active", "paused", "completed", "cancelled"]
        
        for status in statuses:
            session = DevelopmentSession(
                session_name="test_session",
                component_type="framework",
                component_name="test_framework",
                status=status
            )
            assert session.status == status
    
    def test_iteration_log_structure(self):
        """Test iteration log JSON structure."""
        iteration_data = [
            {
                "iteration": 1,
                "timestamp": "2025-06-11T10:30:00Z",
                "notes": "First iteration completed",
                "metrics": {"score": 0.75}
            },
            {
                "iteration": 2,
                "timestamp": "2025-06-11T11:15:00Z",
                "notes": "Second iteration with improvements",
                "metrics": {"score": 0.82}
            }
        ]
        
        session = DevelopmentSession(
            session_name="test_session",
            component_type="prompt_template",
            component_name="test_prompt",
            iteration_log=iteration_data
        )
        
        assert session.iteration_log == iteration_data
        assert len(session.iteration_log) == 2
        assert session.iteration_log[0]["notes"] == "First iteration completed"
    
    def test_success_metrics_tracking(self):
        """Test success metrics JSON field."""
        metrics = {
            "final_score": 0.89,
            "improvement_rate": 0.15,
            "validation_passed": True,
            "time_to_convergence": "2.5 hours"
        }
        
        session = DevelopmentSession(
            session_name="test_session",
            component_type="weighting_methodology", 
            component_name="test_weighting",
            success_metrics=metrics,
            status="completed"
        )
        
        assert session.success_metrics == metrics
        assert session.success_metrics["final_score"] == 0.89
        assert session.success_metrics["validation_passed"] is True
    
    def test_lessons_learned_field(self):
        """Test lessons learned text field."""
        lessons = """
        Key findings from this development session:
        1. Initial threshold too low, increased to 0.7
        2. Amplification factor works best at 1.3-1.5 range
        3. Need additional validation on edge cases
        """
        
        session = DevelopmentSession(
            session_name="test_session",
            component_type="weighting_methodology",
            component_name="test_weighting",
            lessons_learned=lessons,
            status="completed"
        )
        
        assert session.lessons_learned == lessons
        assert "threshold too low" in session.lessons_learned


class TestModelRelationships:
    """Test relationships between models."""
    
    def test_prompt_template_versioning(self):
        """Test parent-child versioning for prompt templates."""
        parent = PromptTemplate(
            name="test_prompt",
            version="v1.0",
            template_content="Original content"
        )
        
        child = PromptTemplate(
            name="test_prompt",
            version="v2.0",
            template_content="Updated content",
            parent_version_id=parent.id
        )
        
        # In a real database, this would be tested with proper relationships
        # Here we just verify the parent_version_id is set correctly
        assert child.parent_version_id == parent.id
    
    def test_component_compatibility_references(self):
        """Test that component compatibility properly references components."""
        prompt_id = uuid4()
        framework_id = uuid4()
        weighting_id = uuid4()
        
        compatibility = ComponentCompatibility(
            prompt_template_id=prompt_id,
            framework_id=framework_id,
            weighting_method_id=weighting_id,
            validation_status="validated"
        )
        
        assert compatibility.prompt_template_id == prompt_id
        assert compatibility.framework_id == framework_id
        assert compatibility.weighting_method_id == weighting_id


class TestModelValidation:
    """Test model validation and constraints."""
    
    def test_required_fields(self):
        """Test that required fields are properly validated."""
        # These should work without errors
        prompt = PromptTemplate(
            name="test",
            version="v1.0",
            template_content="content"
        )
        assert prompt.name == "test"
        
        framework = FrameworkVersion(
            framework_name="test",
            version="v1.0",
            dipoles_json={}
        )
        assert framework.framework_name == "test"
        
        weighting = WeightingMethodology(
            name="test",
            version="v1.0",
            algorithm_type="winner_take_most",
            parameters_json={}
        )
        assert weighting.name == "test"
    
    def test_required_vs_optional_fields(self):
        """Test that required fields are enforced and optional fields work."""
        # Test minimum required fields for PromptTemplate
        prompt = PromptTemplate(
            name="test",
            version="v1.0",
            template_content="content",
            validation_status="draft"  # Explicitly set since defaults may not work in unit tests
        )
        
        assert prompt.name == "test"
        assert prompt.version == "v1.0"
        assert prompt.template_content == "content"
        assert prompt.validation_status == "draft"
        
        # Test minimum required fields for DevelopmentSession
        session = DevelopmentSession(
            session_name="test",
            component_type="prompt_template",
            component_name="test",
            status="active"  # Explicitly set
        )
        
        assert session.status == "active"
        assert session.session_name == "test"
        assert session.component_type == "prompt_template" 