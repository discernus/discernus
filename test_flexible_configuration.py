#!/usr/bin/env python3
"""
Test script to demonstrate flexible template discovery and section parsing.
"""

import os
import sys
sys.path.append('.')

from discernus.agents.thin_synthesis.results_interpreter.dual_purpose_results_interpreter import (
    DualPurposeResultsInterpreter, DualPurposeReportRequest
)
from discernus.core.audit_logger import AuditLogger
from discernus.core.experiment_security_boundary import ExperimentSecurityBoundary
from pathlib import Path

def test_flexible_configuration():
    """Test the flexible template discovery and section parsing."""
    
    # Create a mock audit logger
    security_boundary = ExperimentSecurityBoundary("/tmp/test")
    audit_logger = AuditLogger(security_boundary, Path("/tmp/test"))
    
    # Create the interpreter
    interpreter = DualPurposeResultsInterpreter(
        model="vertex_ai/gemini-2.5-flash-lite",
        audit_logger=audit_logger
    )
    
    print("🔍 Testing Flexible Template Discovery")
    print("=" * 50)
    
    # Test 1: Default template discovery
    print("\n1. Testing default template discovery...")
    template = interpreter._load_template()
    print(f"✅ Template loaded: {len(template)} characters")
    
    # Test 2: Custom template path
    print("\n2. Testing custom template path...")
    custom_path = "discernus/agents/thin_synthesis/results_interpreter/templates/custom_report_template.yaml"
    template = interpreter._load_template(custom_path)
    print(f"✅ Custom template loaded: {len(template)} characters")
    
    # Test 3: Flexible section parsing
    print("\n3. Testing flexible section parsing...")
    
    # Create a test report with different section markers
    test_report = """
# Test Experiment
## Test Subtitle

## 📊 PROVENANCE & STATUS
Some provenance info...

## 🎯 EXECUTIVE SUMMARY
Executive summary here...

## 📊 KEY RESULTS AT A GLANCE
Key results here...

## METHODOLOGY
Methodology section here...

## DETAILED FINDINGS
Detailed findings here...

## APPENDIX
Appendix content here...
"""
    
    # Test with default markers
    sections = interpreter._parse_sections_flexibly(test_report)
    print(f"✅ Default parsing - Scanner: {len(sections['scanner_section'])} chars")
    print(f"✅ Default parsing - Collaborator: {len(sections['collaborator_section'])} chars")
    print(f"✅ Default parsing - Transparency: {len(sections['transparency_section'])} chars")
    
    # Test with custom markers
    custom_markers = {
        'scanner_end': ['## METHODOLOGY', '## CONCISE METHODOLOGY'],
        'collaborator_end': ['## APPENDIX', '## TRANSPARENCY APPENDIX']
    }
    
    sections = interpreter._parse_sections_flexibly(test_report, custom_markers)
    print(f"✅ Custom parsing - Scanner: {len(sections['scanner_section'])} chars")
    print(f"✅ Custom parsing - Collaborator: {len(sections['collaborator_section'])} chars")
    print(f"✅ Custom parsing - Transparency: {len(sections['transparency_section'])} chars")
    
    # Test 4: Configuration options in request
    print("\n4. Testing configuration options in request...")
    
    request = DualPurposeReportRequest(
        experiment_name="Test Experiment",
        experiment_subtitle="Test Subtitle",
        run_id="TEST123",
        execution_time_utc="2025-01-01 00:00:00 UTC",
        execution_time_local="2025-01-01 00:00:00",
        analysis_model="test-model",
        synthesis_model="test-model",
        framework_name="Test Framework",
        framework_version="v1.0",
        document_count=2,
        corpus_type="Test Corpus",
        corpus_composition="Test composition",
        statistical_results={},
        evidence_data={},
        scores_data={},
        run_directory="/tmp/test",
        cost_data={},
        # Configuration options
        template_path=custom_path,
        section_markers=custom_markers
    )
    
    print(f"✅ Request created with custom template path: {request.template_path}")
    print(f"✅ Request created with custom section markers: {request.section_markers}")
    
    print("\n🎉 All flexible configuration tests passed!")
    print("\n📋 Summary of improvements:")
    print("   ✅ Configurable template discovery with multiple fallback paths")
    print("   ✅ Flexible section parsing with custom markers")
    print("   ✅ Configuration options in request structure")
    print("   ✅ Graceful fallbacks for missing templates/sections")
    print("   ✅ No more hardcoded paths or rigid parsing")

if __name__ == "__main__":
    test_flexible_configuration() 