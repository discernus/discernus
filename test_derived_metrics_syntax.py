#!/usr/bin/env python3
"""
Unit test for derived metrics syntax error fix.
Tests that the DerivedMetricsAgent generates valid Python syntax.
"""

import tempfile
import os
import json
from pathlib import Path
from discernus.agents.automated_derived_metrics.agent import AutomatedDerivedMetricsAgent
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger

def test_derived_metrics_syntax_generation():
    """Test that derived metrics agent generates valid Python syntax."""
    
    # Create a minimal test setup
    experiment_path = Path("/Volumes/code/discernus/projects/nano_test_experiment")
    security_boundary = ExperimentSecurityBoundary(experiment_path)
    run_folder = experiment_path / "shared_cache"
    run_folder.mkdir(parents=True, exist_ok=True)
    
    # Create components
    artifact_storage = LocalArtifactStorage(
        security_boundary=security_boundary,
        run_folder=run_folder,
        run_name="test_run"
    )
    
    audit_logger = AuditLogger(
        security_boundary=security_boundary,
        run_folder=experiment_path / "session" / "test_session"
    )
    
    # Create derived metrics agent
    agent = AutomatedDerivedMetricsAgent(
        model="vertex_ai/gemini-2.5-pro",
        audit_logger=audit_logger
    )
    
    # Create temporary workspace
    with tempfile.TemporaryDirectory() as temp_dir:
        workspace_path = Path(temp_dir)
        
        # Create framework content file
        framework_content = """# Test Framework

## Dimensions
- sentiment: Positive vs negative sentiment
- confidence: High vs low confidence

## Derived Metrics
- net_sentiment: Overall sentiment score (positive_sentiment - negative_sentiment)
- sentiment_magnitude: Strength of sentiment (abs(positive_sentiment) + abs(negative_sentiment))
"""
        (workspace_path / "framework_content.md").write_text(framework_content)
        
        # Create experiment spec file
        experiment_spec = {
            "name": "test_experiment",
            "description": "Test experiment for syntax validation",
            "data_columns": ["sentiment", "confidence"],
            "sample_data": [
                {"sentiment": 0.8, "confidence": 0.9},
                {"sentiment": -0.3, "confidence": 0.7}
            ]
        }
        (workspace_path / "experiment_spec.json").write_text(json.dumps(experiment_spec))
        
        print("🧪 Testing derived metrics syntax generation...")
        
        try:
            # Generate derived metrics functions
            result = agent.generate_functions(workspace_path)
            
            print(f"✅ Generated functions successfully")
            print(f"📊 Status: {result.get('status', 'unknown')}")
            print(f"📁 Output file: {result.get('output_file', 'unknown')}")
        
            # Check if functions were generated
            if result.get('status') != 'success':
                raise Exception(f"Function generation failed: {result}")
            
            # Get the generated code
            output_filename = result.get('output_file')
            if not output_filename:
                raise Exception("No output file generated")
            
            output_file = workspace_path / output_filename
            if not output_file.exists():
                raise Exception(f"Output file not found: {output_file}")
            
            # Read the generated code
            with open(output_file, 'r') as f:
                generated_code = f.read()
            
            print(f"📝 Generated code length: {len(generated_code)} characters")
            print(f"📝 First 200 characters: {generated_code[:200]}...")
            
            # Debug: Show all function definitions
            import re
            function_defs = re.findall(r'def\s+(\w+)\(', generated_code)
            print(f"🔍 Functions found: {function_defs}")
            
            # Test 1: Check for basic Python syntax
            try:
                compile(generated_code, output_file, 'exec')
                print("✅ Generated code compiles successfully")
            except SyntaxError as e:
                print(f"❌ Syntax error in generated code:")
                print(f"   Line {e.lineno}: {e.text}")
                print(f"   Error: {e.msg}")
                raise Exception(f"Generated code has syntax error: {e}")
            
            # Test 2: Check for required functions
            if 'def calculate_derived_metrics(' not in generated_code:
                raise Exception("Missing calculate_derived_metrics function")
            
            if 'def calculate_net_sentiment(' not in generated_code:
                raise Exception("Missing calculate_net_sentiment function")
            
            if 'def calculate_sentiment_magnitude(' not in generated_code:
                raise Exception("Missing calculate_sentiment_magnitude function")
            
            print("✅ All required functions present")
            
            # Test 3: Try to import the module
            try:
                import sys
                import importlib.util
                
                spec = importlib.util.spec_from_file_location("test_module", output_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                print("✅ Generated module imports successfully")
                
                # Test 4: Check if functions are callable
                if not hasattr(module, 'calculate_derived_metrics'):
                    raise Exception("calculate_derived_metrics function not found in module")
                
                if not callable(module.calculate_derived_metrics):
                    raise Exception("calculate_derived_metrics is not callable")
                
                print("✅ Generated functions are callable")
                
            except Exception as e:
                print(f"❌ Module import failed: {e}")
                raise Exception(f"Generated module cannot be imported: {e}")
            
            print("🎉 All tests passed! Derived metrics syntax is valid.")
            return True
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False

if __name__ == "__main__":
    success = test_derived_metrics_syntax_generation()
    exit(0 if success else 1)
