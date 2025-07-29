#!/usr/bin/env python3
"""
Test script for CodeExecutor

This script validates that the CodeExecutor can:
1. Execute generated Python code safely in a subprocess
2. Handle timeouts and errors gracefully
3. Extract JSON results from code output
4. Create and work with synthetic test data
"""

import sys
import os
import logging
import tempfile

# Add the prototype directory to path
sys.path.append(os.path.dirname(__file__))

from agents.code_executor import CodeExecutor
from agents.code_executor.executor import CodeExecutionRequest
from agents.analytical_code_generator import AnalyticalCodeGenerator
from agents.analytical_code_generator.agent import CodeGenerationRequest

def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def test_basic_execution():
    """Test basic code execution functionality."""
    
    print("🧪 Testing basic CodeExecutor functionality...")
    
    executor = CodeExecutor()
    
    # Simple test code that outputs JSON
    test_code = '''
import json
import pandas as pd
import numpy as np

# Simple analysis
data = {"test": "success", "value": 42, "computed": 2 + 2}

# Output results as JSON
print("=== ANALYSIS RESULTS ===")
print(json.dumps(data, indent=2))
print("=== END RESULTS ===")
'''
    
    # Create temporary CSV files for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("artifact_id,score\ntest1,0.5\ntest2,0.8\n")
        scores_path = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("artifact_id,evidence\ntest1,sample evidence\ntest2,more evidence\n")
        evidence_path = f.name
    
    try:
        # Execute the test code
        request = CodeExecutionRequest(
            analysis_code=test_code,
            scores_csv_path=scores_path,
            evidence_csv_path=evidence_path,
            timeout_seconds=30
        )
        
        response = executor.execute_code(request)
        
        if not response.success:
            print(f"❌ Code execution failed: {response.error_message}")
            return False
        
        print("✅ Code execution successful!")
        print(f"⏱️  Execution time: {response.execution_time_seconds:.2f} seconds")
        print(f"📊 Results: {response.results}")
        
        # Validate expected results
        if response.results.get('test') != 'success':
            print("❌ Unexpected results content")
            return False
        
        if response.results.get('computed') != 4:
            print("❌ Computation error in results")
            return False
        
        print("✅ Results validation passed!")
        return True
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(scores_path)
            os.unlink(evidence_path)
        except OSError:
            pass

def test_synthetic_data_creation():
    """Test synthetic data creation functionality."""
    
    print("\n📊 Testing synthetic data creation...")
    
    executor = CodeExecutor()
    
    # Create temporary files for synthetic data
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        scores_path = f.name
    
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        evidence_path = f.name
    
    try:
        # Generate synthetic data
        scores_df, evidence_df = executor.create_test_data(
            scores_csv_path=scores_path,
            evidence_csv_path=evidence_path,
            num_artifacts=20
        )
        
        print(f"✅ Created synthetic data:")
        print(f"   📈 Scores: {len(scores_df)} artifacts with {len(scores_df.columns)} columns")
        print(f"   📝 Evidence: {len(evidence_df)} entries")
        
        # Validate data structure
        expected_score_columns = [
            'artifact_id', 'integrity_score', 'courage_score', 'compassion_score',
            'justice_score', 'wisdom_score', 'corruption_score', 'cowardice_score',
            'cruelty_score', 'injustice_score', 'folly_score'
        ]
        
        if list(scores_df.columns) != expected_score_columns:
            print(f"❌ Unexpected score columns: {list(scores_df.columns)}")
            return False
        
        expected_evidence_columns = [
            'artifact_id', 'dimension', 'evidence_text', 'context', 'confidence', 'reasoning'
        ]
        
        if list(evidence_df.columns) != expected_evidence_columns:
            print(f"❌ Unexpected evidence columns: {list(evidence_df.columns)}")
            return False
        
        print("✅ Data structure validation passed!")
        return True
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(scores_path)
            os.unlink(evidence_path)
        except OSError:
            pass

def test_end_to_end_integration():
    """Test end-to-end integration with AnalyticalCodeGenerator."""
    
    print("\n🔄 Testing end-to-end integration...")
    
    # Initialize both components
    code_generator = AnalyticalCodeGenerator()
    code_executor = CodeExecutor()
    
    # Create synthetic test data
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        scores_path = f.name
    
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        evidence_path = f.name
    
    try:
        # Generate synthetic data
        code_executor.create_test_data(scores_path, evidence_path, num_artifacts=10)
        
        # Load framework specification
        with open('test_data/sample_framework.md', 'r') as f:
            framework_spec = f.read()
        
        with open('test_data/sample_scores_structure.txt', 'r') as f:
            scores_structure = f.read()
            
        with open('test_data/sample_evidence_structure.txt', 'r') as f:
            evidence_structure = f.read()
        
        # Generate analysis code
        print("📝 Generating analysis code...")
        
        code_request = CodeGenerationRequest(
            framework_spec=framework_spec,
            scores_csv_structure=scores_structure,
            evidence_csv_structure=evidence_structure,
            experiment_context="End-to-end integration test"
        )
        
        code_response = code_generator.generate_analysis_code(code_request)
        
        if not code_response.success:
            print(f"❌ Code generation failed: {code_response.error_message}")
            return False
        
        print("✅ Code generation successful!")
        
        # Execute the generated code
        print("⚙️  Executing generated code...")
        
        exec_request = CodeExecutionRequest(
            analysis_code=code_response.analysis_code,
            scores_csv_path=scores_path,
            evidence_csv_path=evidence_path,
            timeout_seconds=120  # Allow more time for complex analysis
        )
        
        exec_response = code_executor.execute_code(exec_request)
        
        if not exec_response.success:
            print(f"❌ Code execution failed: {exec_response.error_message}")
            print(f"📜 STDERR: {exec_response.stderr_output}")
            return False
        
        print("✅ Code execution successful!")
        print(f"⏱️  Execution time: {exec_response.execution_time_seconds:.2f} seconds")
        
        # Validate results structure
        results = exec_response.results
        expected_sections = ['descriptive_stats', 'reliability_metrics', 'correlations', 
                           'hypothesis_tests', 'effect_sizes', 'sample_characteristics']
        
        missing_sections = [section for section in expected_sections if section not in results]
        if missing_sections:
            print(f"⚠️  Missing result sections: {missing_sections}")
        
        present_sections = [section for section in expected_sections if section in results]
        print(f"✅ Present result sections: {present_sections}")
        
        # Show sample results
        if 'descriptive_stats' in results:
            print(f"📊 Sample descriptive stats keys: {list(results['descriptive_stats'].keys())[:3]}...")
        
        if 'hypothesis_tests' in results:
            print(f"🧪 Hypothesis tests: {list(results['hypothesis_tests'].keys())}")
        
        return True
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(scores_path)
            os.unlink(evidence_path)
        except OSError:
            pass

def test_error_handling():
    """Test error handling for invalid code."""
    
    print("\n🚨 Testing error handling...")
    
    executor = CodeExecutor()
    
    # Invalid Python code
    invalid_code = '''
import json
print("This will fail")
invalid_syntax here!!!
'''
    
    # Create temporary CSV files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("artifact_id,score\ntest1,0.5\n")
        scores_path = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("artifact_id,evidence\ntest1,evidence\n")
        evidence_path = f.name
    
    try:
        request = CodeExecutionRequest(
            analysis_code=invalid_code,
            scores_csv_path=scores_path,
            evidence_csv_path=evidence_path,
            timeout_seconds=10
        )
        
        response = executor.execute_code(request)
        
        if response.success:
            print("❌ Expected execution to fail but it succeeded")
            return False
        
        print("✅ Error handling successful!")
        print(f"📝 Error message: {response.error_message}")
        
        return True
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(scores_path)
            os.unlink(evidence_path)
        except OSError:
            pass

def main():
    """Run all tests."""
    
    setup_logging()
    
    print("🚀 Starting CodeExecutor Tests")
    print("=" * 50)
    
    # Test basic functionality
    success = test_basic_execution()
    if not success:
        print("❌ Basic execution test failed!")
        return 1
    
    # Test synthetic data creation
    success = test_synthetic_data_creation()
    if not success:
        print("❌ Synthetic data creation test failed!")
        return 1
    
    # Test error handling
    success = test_error_handling()
    if not success:
        print("❌ Error handling test failed!")
        return 1
    
    # Test end-to-end integration
    success = test_end_to_end_integration()
    if not success:
        print("❌ End-to-end integration test failed!")
        return 1
    
    print("\n🎉 All tests passed!")
    print("✅ CodeExecutor is working correctly")
    
    return 0

if __name__ == "__main__":
    exit(main()) 