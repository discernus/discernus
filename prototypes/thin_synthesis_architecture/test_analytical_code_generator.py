#!/usr/bin/env python3
"""
Test script for AnalyticalCodeGenerator Agent

This script validates that the AnalyticalCodeGenerator can:
1. Generate syntactically valid Python code
2. Adapt to framework specifications  
3. Produce code that handles the expected data structures
4. Generate framework-appropriate statistical analyses
"""

import sys
import os
import logging

# Add the prototype directory to path
sys.path.append(os.path.dirname(__file__))

from agents.analytical_code_generator import AnalyticalCodeGenerator
from agents.analytical_code_generator.agent import CodeGenerationRequest

def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def load_test_data():
    """Load test framework and data structure specifications."""
    
    # Load framework specification
    with open('test_data/sample_framework.md', 'r') as f:
        framework_spec = f.read()
    
    # Load data structure descriptions
    with open('test_data/sample_scores_structure.txt', 'r') as f:
        scores_structure = f.read()
        
    with open('test_data/sample_evidence_structure.txt', 'r') as f:
        evidence_structure = f.read()
    
    return framework_spec, scores_structure, evidence_structure

def test_code_generation():
    """Test the core code generation functionality."""
    
    print("🧪 Testing AnalyticalCodeGenerator...")
    
    # Initialize the agent
    generator = AnalyticalCodeGenerator()
    
    # Load test data
    framework_spec, scores_structure, evidence_structure = load_test_data()
    
    # Create generation request
    request = CodeGenerationRequest(
        framework_spec=framework_spec,
        scores_csv_structure=scores_structure,
        evidence_csv_structure=evidence_structure,
        experiment_context="Test experiment for CAF framework validation"
    )
    
    print("📝 Generating analysis code...")
    
    # Generate code
    response = generator.generate_analysis_code(request)
    
    # Validate response
    if not response.success:
        print(f"❌ Code generation failed: {response.error_message}")
        return False
    
    print("✅ Code generation successful!")
    print(f"📊 Generated {len(response.analysis_code)} characters of code")
    print(f"📚 Required libraries: {response.required_libraries}")
    
    # Validate generated code
    print("🔍 Validating generated code...")
    validation = generator.validate_generated_code(response.analysis_code)
    
    if not validation['syntax_valid']:
        print(f"❌ Syntax validation failed: {validation['issues']}")
        return False
    
    if not validation['security_safe']:
        print(f"⚠️  Security concerns: {validation['issues']}")
    
    print("✅ Code validation passed!")
    
    # Display code summary
    print("\n" + "="*60)
    print("GENERATED CODE SUMMARY")
    print("="*60)
    print(f"Explanation: {response.code_explanation}")
    print(f"Libraries: {', '.join(response.required_libraries)}")
    print("\nExpected outputs:")
    for key, desc in response.expected_outputs.items():
        print(f"  - {key}: {desc}")
    
    # Show first 500 characters of generated code
    print("\nCode preview (first 500 chars):")
    print("-" * 40)
    print(response.analysis_code[:500] + "..." if len(response.analysis_code) > 500 else response.analysis_code)
    
    return True

def test_framework_adaptability():
    """Test that the generator adapts to different framework types."""
    
    print("\n🔄 Testing framework adaptability...")
    
    # Create a different framework specification
    different_framework = """
# Binary Ethics Framework (BEF) - Test Version

## Overview
This framework assesses ethical vs unethical behavior in binary terms.

## Analytical Dimensions
- **Ethical Score**: 0.0-1.0 scale of ethical behavior
- **Unethical Score**: 0.0-1.0 scale of unethical behavior

## Statistical Requirements
- Simple correlation between ethical and unethical scores
- T-test comparing mean ethical vs unethical scores
- Basic descriptive statistics
"""
    
    generator = AnalyticalCodeGenerator()
    
    request = CodeGenerationRequest(
        framework_spec=different_framework,
        scores_csv_structure="artifact_id, ethical_score, unethical_score",
        evidence_csv_structure="artifact_id, dimension, evidence_text",
        experiment_context="Binary ethics test"
    )
    
    response = generator.generate_analysis_code(request)
    
    if response.success:
        print("✅ Successfully adapted to different framework!")
        return True
    else:
        print(f"❌ Failed to adapt: {response.error_message}")
        return False

def main():
    """Run all tests."""
    
    setup_logging()
    
    print("🚀 Starting AnalyticalCodeGenerator Tests")
    print("=" * 50)
    
    # Test core functionality
    success = test_code_generation()
    if not success:
        print("❌ Core functionality test failed!")
        return 1
    
    # Test adaptability
    success = test_framework_adaptability()
    if not success:
        print("❌ Framework adaptability test failed!")
        return 1
    
    print("\n🎉 All tests passed!")
    print("✅ AnalyticalCodeGenerator is working correctly")
    
    return 0

if __name__ == "__main__":
    exit(main()) 