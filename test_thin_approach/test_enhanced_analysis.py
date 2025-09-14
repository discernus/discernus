#!/usr/bin/env python3
"""
Test script for Enhanced Analysis Agent with Integrated Markup
"""

import json
from pathlib import Path
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from enhanced_analysis_agent import EnhancedAnalysisAgent


def main():
    # Setup experiment environment
    experiment_dir = Path("/Volumes/code/discernus/tmp")
    
    # Initialize components
    security = ExperimentSecurityBoundary(experiment_dir)
    audit = AuditLogger(security, experiment_dir / "logs")
    storage = LocalArtifactStorage(security, experiment_dir / "artifacts")
    
    # Load framework
    framework_path = experiment_dir / "framework" / "pdaf_v10_0_2.md"
    with open(framework_path, 'r') as f:
        framework_content = f.read()
    
    # Load document
    doc_path = experiment_dir / "corpus" / "Trump_SOTU_2020.txt"
    with open(doc_path, 'r') as f:
        doc_content = f.read()
    
    # Prepare documents
    corpus_documents = [{
        'name': 'Trump_SOTU_2020.txt',
        'content': doc_content
    }]
    
    # Minimal experiment config
    experiment_config = {
        'name': 'enhanced_analysis_test',
        'description': 'Test enhanced analysis with integrated markup'
    }
    
    # Create agent and run analysis
    agent = EnhancedAnalysisAgent(security, audit, storage)
    
    print("=== Testing Enhanced Analysis Agent ===")
    print("6-Step THIN Approach with Integrated Markup:")
    print("1. Enhanced Composite Analysis with Markup (Flash)")
    print("2. Evidence Extraction (Flash Lite)")
    print("3. Score Extraction (Flash Lite)")
    print("4. Derived Metrics Generation (Flash Lite)")
    print("5. Verification (Flash Lite)")
    print("6. Markup Extraction (Flash Lite)")
    print()
    
    results = agent.run_enhanced_analysis(
        framework_content=framework_content,
        corpus_documents=corpus_documents,
        experiment_config=experiment_config,
        model="vertex_ai/gemini-2.5-flash"
    )
    
    # Print step results
    for step_name, step_result in results.items():
        if step_name in ['composite_analysis', 'evidence_extraction', 'score_extraction', 'derived_metrics', 'verification', 'markup_extraction']:
            print(f"{step_name.upper()}:")
            print(f"  Model: {step_result.get('model_used', 'unknown')}")
            print(f"  Artifact Hash: {step_result.get('artifact_hash', 'none')}")
            if step_name == 'verification':
                verified = step_result.get('verified', False)
                status = "✓ Verified" if verified else "✗ Not Verified"
                print(f"  Status: {status}")
            print()
    
    # Save detailed results
    with open(experiment_dir / "artifacts" / "enhanced_analysis_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Detailed results saved to: {experiment_dir / 'artifacts' / 'enhanced_analysis_results.json'}")
    
    # Show verification status
    verified = results.get('verification', {}).get('verified', False)
    status = "✓ Verified" if verified else "✗ Not Verified"
    print(f"\nFinal Verification Status: {status}")
    
    # Show markup status
    markup_available = results.get('markup_extraction', {}).get('marked_up_document', '')
    if markup_available:
        print(f"✓ Marked-up document extracted ({len(markup_available)} characters)")
    else:
        print("✗ No marked-up document extracted")


if __name__ == "__main__":
    main()
