#!/usr/bin/env python3
"""
Test script for Extended Analysis Agent

Tests the 5-step THIN approach:
1. Composite Analysis Generation (Flash)
2. Evidence Extraction (Flash Lite)  
3. Score Extraction (Flash Lite)
4. Derived Metrics Generation (Flash Lite)
5. Verification (Flash Lite)
"""

import json
from pathlib import Path
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from extended_analysis_agent import ExtendedAnalysisAgent


def main():
    """Test the extended analysis agent."""
    
    # Set up paths
    experiment_dir = Path("/Volumes/code/discernus/tmp")
    framework_path = experiment_dir / "framework" / "pdaf_v10_0_2.md"
    document_path = experiment_dir / "corpus" / "Trump_SOTU_2020.txt"
    
    # Initialize components
    security = ExperimentSecurityBoundary(experiment_dir)
    audit = AuditLogger(security, experiment_dir / "logs")
    storage = LocalArtifactStorage(security, experiment_dir / "artifacts")
    
    # Create extended analysis agent
    agent = ExtendedAnalysisAgent(security, audit, storage)
    
    # Load framework
    with open(framework_path, 'r') as f:
        framework_content = f.read()
    
    # Load document
    with open(document_path, 'r') as f:
        document_content = f.read()
    
    # Prepare corpus documents
    corpus_documents = [{
        'filename': 'Trump_SOTU_2020.txt',
        'content': document_content
    }]
    
    # Experiment config
    experiment_config = {
        'name': 'extended_analysis_test',
        'description': 'Test of 5-step THIN analysis approach'
    }
    
    print("=== Testing Extended Analysis Agent ===")
    print("5-Step THIN Approach:")
    print("1. Composite Analysis Generation (Flash)")
    print("2. Evidence Extraction (Flash Lite)")
    print("3. Score Extraction (Flash Lite)")
    print("4. Derived Metrics Generation (Flash Lite)")
    print("5. Verification (Flash Lite)")
    print()
    
    # Run extended analysis
    results = agent.analyze_documents_extended(
        framework_content=framework_content,
        corpus_documents=corpus_documents,
        experiment_config=experiment_config,
        model="vertex_ai/gemini-2.5-flash"
    )
    
    # Print results summary
    print(f"\n=== Analysis Complete ===")
    print(f"Analysis ID: {results['analysis_metadata']['analysis_id']}")
    print(f"Result Hash: {results['result_hash']}")
    print()
    
    # Print step results
    for step_name, step_result in results.items():
        if step_name in ['composite_analysis', 'evidence_extraction', 'score_extraction', 'derived_metrics', 'verification']:
            print(f"{step_name.upper()}:")
            print(f"  Model: {step_result.get('model_used', 'unknown')}")
            print(f"  Artifact Hash: {step_result.get('artifact_hash', 'none')}")
            if step_name == 'verification':
                verified = step_result.get('verified', False)
                status = "✓ Verified" if verified else "✗ Not Verified"
                print(f"  Status: {status}")
            print()
    
    # Save detailed results
    with open(experiment_dir / "artifacts" / "extended_analysis_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Detailed results saved to: {experiment_dir / 'artifacts' / 'extended_analysis_results.json'}")
    
    # Show verification status
    verified = results.get('verification', {}).get('verified', False)
    status = "✓ Verified" if verified else "✗ Not Verified"
    print(f"\nFinal Verification Status: {status}")


if __name__ == "__main__":
    main()
