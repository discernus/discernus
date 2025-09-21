#!/usr/bin/env python3
"""
Debug script to isolate the IntelligentEvidenceRetrievalAgent error
"""

import sys
import os
import json
import traceback
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from discernus.agents.intelligent_evidence_retriever import IntelligentEvidenceRetrievalAgent
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.core.run_context import RunContext

def debug_evidence_agent():
    """Debug the evidence agent to find the unhashable type error."""
    
    print("=== Debugging IntelligentEvidenceRetrievalAgent ===")
    
    # Use existing nano experiment with real artifacts
    nano_dir = Path("/Volumes/code/discernus/projects/nano_test_experiment")
    nano_run_dir = nano_dir / "runs" / "20250920_223951"  # Use working run
    
    security = ExperimentSecurityBoundary(nano_dir)
    storage = LocalArtifactStorage(security, nano_run_dir)
    audit = AuditLogger(security, nano_run_dir)
    
    # Create agent
    agent = IntelligentEvidenceRetrievalAgent(security, storage, audit)
    
    # Create mock RunContext with real data
    artifacts_dir = nano_run_dir / "artifacts"
    registry_file = artifacts_dir / "artifact_registry.json"
    
    with open(registry_file, 'r') as f:
        registry = json.load(f)
    artifact_hashes = list(registry.keys())
    
    # Create RunContext
    run_context = RunContext(
        experiment_id="nano_test_experiment",
        framework_path=nano_dir / "sentiment_binary_v1.md", 
        corpus_path=nano_dir / "corpus.md"
    )
    run_context.analysis_artifacts = artifact_hashes
    
    # Add mock statistical results
    run_context.statistical_results = {
        "correlations": {
            "positive_negative_sentiment": -1.0
        },
        "descriptive_stats": {
            "positive_sentiment": {"mean": 0.5, "std": 0.707},
            "negative_sentiment": {"mean": 0.5, "std": 0.707}
        }
    }
    
    try:
        print("\n1. Testing evidence inventory...")
        evidence_count, evidence_size_mb = agent.count_evidence_artifacts(run_context)
        print(f"✅ Evidence inventory: {evidence_count} artifacts, {evidence_size_mb:.3f} MB")
        
        print("\n2. Testing strategic curation planning...")
        curation_plan = agent.generate_curation_plan(run_context, evidence_count, evidence_size_mb)
        print(f"✅ Strategic planning: {curation_plan['strategy']} with {len(curation_plan['iterations'])} iterations")
        
        print("\n3. Testing dynamic model selection...")
        execution_model = agent.select_execution_model(evidence_count, evidence_size_mb, curation_plan)
        print(f"✅ Model selection: {execution_model}")
        
        print("\n4. Testing full execute method...")
        result = agent.execute(run_context)
        print(f"✅ Execute result: success={result.success}, artifacts={len(result.artifacts)}")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print(f"Error type: {type(e).__name__}")
        print("\nFull traceback:")
        traceback.print_exc()
        
        # Try to identify the problematic line
        tb = traceback.extract_tb(e.__traceback__)
        for frame in tb:
            if 'intelligent_evidence_retriever_agent.py' in frame.filename:
                print(f"\nError in agent at line {frame.lineno}: {frame.line}")

if __name__ == "__main__":
    debug_evidence_agent()
