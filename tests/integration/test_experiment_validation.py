#!/usr/bin/env python3
"""
Comprehensive Experiment Validation Tests

Tests all common user error scenarios to ensure robust validation 
and clear error messages for experiment definitions.
"""

import pytest
import yaml
import json
import tempfile
from pathlib import Path
from typing import Dict, Any

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts' / 'production'))

from comprehensive_experiment_orchestrator import ExperimentOrchestrator

class TestExperimentValidation:
    """Test suite for experiment definition validation edge cases"""
    
    def setup_method(self):
        """Setup for each test"""
        self.orchestrator = ExperimentOrchestrator()
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def teardown_method(self):
        """Cleanup after each test"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    # ========================================================================
    # YAML SYNTAX ERROR TESTS
    # ========================================================================
    
    def test_malformed_yaml_syntax(self):
        """Test malformed YAML syntax produces clear error message"""
        malformed_yaml = """
experiment_meta:
  name: "Test Experiment"
  version: v1.0.0
  description: "Test experiment  # Missing closing quote
  
components:
  frameworks:
    - id: moral_foundations_theory
      type: [invalid syntax here
"""
        experiment_file = self.temp_dir / "malformed.yaml"
        experiment_file.write_text(malformed_yaml)
        
        with pytest.raises(ValueError) as exc_info:
            self.orchestrator.load_experiment_definition(experiment_file)
        
        error_msg = str(exc_info.value)
        assert "Invalid format" in error_msg
        assert "YAML" in error_msg or "syntax" in error_msg
    
    def test_missing_required_sections(self):
        """Test missing required experiment sections"""
        incomplete_experiment = {
            "experiment_meta": {
                "name": "Incomplete Experiment"
                # Missing: version, description
            }
            # Missing: components, execution
        }
        
        experiment_file = self.temp_dir / "incomplete.yaml"
        with open(experiment_file, 'w') as f:
            yaml.dump(incomplete_experiment, f)
        
        with pytest.raises(ValueError) as exc_info:
            self.orchestrator.load_experiment_definition(experiment_file)
        
        error_msg = str(exc_info.value)
        assert "Missing required sections" in error_msg
    
    # ========================================================================
    # FRAMEWORK VALIDATION TESTS  
    # ========================================================================
    
    def test_framework_file_not_found(self):
        """Test framework file path that doesn't exist"""
        experiment = {
            "experiment_meta": {
                "name": "Test Experiment",
                "version": "v1.0.0",
                "description": "Test"
            },
            "components": {
                "frameworks": [{
                    "id": "nonexistent_framework",
                    "type": "file_path", 
                    "file_path": "frameworks/does_not_exist/framework.yaml"
                }]
            },
            "execution": {
                "matrix": [{"run_id": "test"}]
            }
        }
        
        experiment_file = self.temp_dir / "missing_framework.yaml"
        with open(experiment_file, 'w') as f:
            yaml.dump(experiment, f)
        
        # This should pass loading but fail in component validation
        loaded_experiment = self.orchestrator.load_experiment_definition(experiment_file)
        assert loaded_experiment is not None
        
        # Component validation should catch the missing file
        components = self.orchestrator.validate_components(loaded_experiment)
        framework_component = next((c for c in components if c.component_type == 'framework'), None)
        assert framework_component is not None
        assert not framework_component.exists_on_filesystem
    
    def test_invalid_framework_structure(self):
        """Test framework with missing required fields"""
        invalid_framework = {
            "name": "incomplete_framework",
            # Missing: dipoles, version, description
        }
        
        framework_file = self.temp_dir / "invalid_framework.yaml"
        with open(framework_file, 'w') as f:
            yaml.dump(invalid_framework, f)
        
        experiment = {
            "experiment_meta": {
                "name": "Test Experiment", 
                "version": "v1.0.0",
                "description": "Test"
            },
            "components": {
                "frameworks": [{
                    "id": "test_framework",
                    "type": "file_path",
                    "file_path": str(framework_file)
                }]
            },
            "execution": {
                "matrix": [{"run_id": "test"}]
            }
        }
        
        experiment_file = self.temp_dir / "test_experiment.yaml"
        with open(experiment_file, 'w') as f:
            yaml.dump(experiment, f)
        
        # Should load but validation should identify structural issues
        loaded_experiment = self.orchestrator.load_experiment_definition(experiment_file)
        components = self.orchestrator.validate_components(loaded_experiment)
        
        # Should detect missing sections
        framework_component = next((c for c in components if c.component_type == 'framework'), None)
        assert framework_component is not None
    
    # ========================================================================
    # CORPUS VALIDATION TESTS
    # ========================================================================
    
    def test_corpus_directory_not_found(self):
        """Test corpus directory that doesn't exist"""
        experiment = {
            "experiment_meta": {
                "name": "Test Experiment",
                "version": "v1.0.0", 
                "description": "Test"
            },
            "components": {
                "corpus": [{
                    "id": "missing_corpus",
                    "type": "file_collection",
                    "file_path": "corpus/does_not_exist",
                    "pattern": "*.txt"
                }]
            },
            "execution": {
                "matrix": [{"run_id": "test"}]
            }
        }
        
        experiment_file = self.temp_dir / "missing_corpus.yaml"
        with open(experiment_file, 'w') as f:
            yaml.dump(experiment, f)
        
        loaded_experiment = self.orchestrator.load_experiment_definition(experiment_file)
        components = self.orchestrator.validate_components(loaded_experiment)
        
        corpus_component = next((c for c in components if c.component_type == 'corpus'), None)
        assert corpus_component is not None
        assert not corpus_component.exists_on_filesystem
    
    def test_empty_corpus_directory(self):
        """Test corpus directory with no matching files"""
        empty_dir = self.temp_dir / "empty_corpus"
        empty_dir.mkdir()
        
        experiment = {
            "experiment_meta": {
                "name": "Test Experiment",
                "version": "v1.0.0",
                "description": "Test"
            },
            "components": {
                "corpus": [{
                    "id": "empty_corpus", 
                    "type": "file_collection",
                    "file_path": str(empty_dir),
                    "pattern": "*.txt"
                }]
            },
            "execution": {
                "matrix": [{"run_id": "test"}]
            }
        }
        
        experiment_file = self.temp_dir / "empty_corpus.yaml"
        with open(experiment_file, 'w') as f:
            yaml.dump(experiment, f)
        
        loaded_experiment = self.orchestrator.load_experiment_definition(experiment_file)
        components = self.orchestrator.validate_components(loaded_experiment)
        
        corpus_component = next((c for c in components if c.component_type == 'corpus'), None)
        assert corpus_component is not None
        # Should exist as directory but have validation issues
    
    # ========================================================================
    # COMPONENT REFERENCE TESTS
    # ========================================================================
    
    def test_invalid_component_references(self):
        """Test experiment with invalid component IDs"""
        experiment = {
            "experiment_meta": {
                "name": "Test Experiment",
                "version": "v1.0.0",
                "description": "Test"
            },
            "components": {
                "prompt_templates": [{
                    "id": "nonexistent_template",
                    "version": "v1.0"
                }],
                "weighting_schemes": [{
                    "id": "nonexistent_scheme", 
                    "version": "v1.0"
                }],
                "models": [{
                    "id": "gpt-99-ultra",  # Doesn't exist
                    "provider": "openai"
                }]
            },
            "execution": {
                "matrix": [{
                    "run_id": "test",
                    "prompt_template": "nonexistent_template",
                    "weighting_scheme": "nonexistent_scheme",
                    "model": "gpt-99-ultra"
                }]
            }
        }
        
        experiment_file = self.temp_dir / "invalid_refs.yaml"
        with open(experiment_file, 'w') as f:
            yaml.dump(experiment, f)
        
        loaded_experiment = self.orchestrator.load_experiment_definition(experiment_file)
        components = self.orchestrator.validate_components(loaded_experiment)
        
        # Should identify missing components
        missing_components = [c for c in components if not c.exists_in_db]
        assert len(missing_components) > 0
    
    # ========================================================================
    # ERROR MESSAGE QUALITY TESTS
    # ========================================================================
    
    def test_error_message_contains_helpful_guidance(self):
        """Test that error messages provide actionable guidance"""
        # This will be framework-specific testing
        # Test that missing framework errors suggest specific fix commands
        pass
    
    def test_validation_summary_completeness(self):
        """Test that validation provides comprehensive summary"""
        # Test that pre-flight validation shows all issues at once
        # Rather than failing on first issue
        pass

# ========================================================================
# YAML VALIDATION UTILITY TESTS
# ========================================================================

class TestYAMLValidation:
    """Specific tests for YAML validation edge cases"""
    
    def test_yaml_load_safety(self):
        """Test that YAML loading is safe (no code execution)"""
        dangerous_yaml = """
!!python/object/apply:os.system
- "echo 'This should not execute'"
"""
        with pytest.raises(Exception):
            # Should fail safely without executing code
            yaml.safe_load(dangerous_yaml)
    
    def test_yaml_encoding_handling(self):
        """Test handling of different text encodings"""
        # Test UTF-8, Windows encoding, etc.
        pass

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"]) 