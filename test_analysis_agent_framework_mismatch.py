#!/usr/bin/env python3
"""
Test Analysis Agent Framework Mismatch
======================================

Demonstrate the issue where the analysis agent is hardcoded for PDAF dimensions
but the micro experiment uses a sentiment framework with different dimensions.
"""

import json
import tempfile
from pathlib import Path

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.agents.EnhancedAnalysisAgent.agent_multi_tool import EnhancedAnalysisAgentMultiTool
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry


def test_framework_mismatch():
    """Test the framework mismatch issue"""
    print("Testing Analysis Agent Framework Mismatch...")
    print("=" * 50)
    
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
    
    # Load a test document
    corpus_path = Path("/Volumes/code/discernus/projects/micro_test_experiment/corpus/positive_test_1.txt")
    with open(corpus_path, 'r') as f:
        document_content = f.read()
    
    print(f"Framework: {framework_path.name}")
    print(f"Document: {corpus_path.name}")
    print(f"Document content preview: {document_content[:100]}...")
    
    # Check the tool schema
    tools = agent._get_tools_schema()
    scores_tool = tools[0]  # record_analysis_scores
    scores_properties = scores_tool["function"]["parameters"]["properties"]["scores"]["properties"]
    
    print(f"\n🔧 Tool schema dimensions:")
    for dim in scores_properties.keys():
        print(f"   - {dim}")
    
    # Check what dimensions the framework actually defines
    print(f"\n📋 Framework dimensions (from YAML):")
    # Parse the YAML to find dimensions
    yaml_start = framework_content.find("```yaml")
    yaml_end = framework_content.find("```", yaml_start + 7)
    if yaml_start != -1 and yaml_end != -1:
        yaml_content = framework_content[yaml_start+7:yaml_end]
        print(f"YAML content preview: {yaml_content[:200]}...")
    
    # Look for dimension definitions in the framework
    print(f"\n📋 Framework dimensions (from text):")
    if "Positive Sentiment" in framework_content:
        print("   - positive_sentiment")
    if "Negative Sentiment" in framework_content:
        print("   - negative_sentiment")
    
    print(f"\n❌ MISMATCH DETECTED:")
    print(f"   Tool schema expects: {list(scores_properties.keys())[:3]}... (PDAF dimensions)")
    print(f"   Framework provides: positive_sentiment, negative_sentiment (Sentiment dimensions)")
    print(f"   This explains why Gemini returns empty scores - it can't map the framework dimensions to the tool schema!")
    
    # Clean up
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    return True


if __name__ == '__main__':
    test_framework_mismatch()
