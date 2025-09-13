#!/usr/bin/env python3
"""
Test Dimension Extraction
========================

Test the dimension extraction logic for the sentiment framework.
"""

import tempfile
from pathlib import Path

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.agents.EnhancedAnalysisAgent.agent_multi_tool import EnhancedAnalysisAgentMultiTool
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry


def test_dimension_extraction():
    """Test dimension extraction from sentiment framework"""
    print("Testing Dimension Extraction...")
    print("=" * 40)
    
    # Set up test environment
    temp_dir = Path(tempfile.mkdtemp())
    
    # Create required experiment.md file for security boundary
    experiment_file = temp_dir / "experiment.md"
    experiment_file.write_text("# Test Experiment\n\nThis is a test experiment for unit testing.")
    
    security = ExperimentSecurityBoundary(experiment_path=temp_dir)
    audit = AuditLogger(security, temp_dir)
    storage = LocalArtifactStorage(security, temp_dir)
    
    # Initialize the analysis agent
    llm_gateway = EnhancedLLMGateway(ModelRegistry())
    agent = EnhancedAnalysisAgentMultiTool(security, audit, storage, llm_gateway, "vertex_ai/gemini-2.5-pro")
    
    # Load the sentiment framework
    framework_path = Path("/Volumes/code/discernus/projects/micro_test_experiment/sentiment_binary_v1.md")
    with open(framework_path, 'r') as f:
        framework_content = f.read()
    
    print("Framework content preview:")
    print(framework_content[:500])
    print("...")
    
    # Test dimension extraction
    print(f"\n🔍 Testing dimension extraction...")
    dimensions = agent._extract_framework_dimensions(framework_content)
    print(f"Extracted dimensions: {dimensions}")
    
    # Test tool schema generation
    print(f"\n🔧 Testing tool schema generation...")
    tools = agent._get_tools_schema(framework_content)
    scores_tool = tools[0]  # record_analysis_scores
    scores_properties = scores_tool["function"]["parameters"]["properties"]["scores"]["properties"]
    
    print(f"Tool schema dimensions:")
    for dim in scores_properties.keys():
        print(f"   - {dim}")
    
    # Clean up
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    return dimensions


if __name__ == '__main__':
    test_dimension_extraction()
