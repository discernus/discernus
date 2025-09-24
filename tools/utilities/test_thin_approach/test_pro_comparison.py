#!/usr/bin/env python3
"""
Test Pro model with both original and enhanced approaches
"""

import json
import sys
from pathlib import Path
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage

# Add the parent directory to the path
sys.path.append('/Volumes/code/discernus')

from test_thin_approach.extended_analysis_agent import ExtendedAnalysisAgent
from test_thin_approach.enhanced_analysis_agent import EnhancedAnalysisAgent


def test_original_pro():
    """Test original 5-step approach with Pro."""
    print("=== Testing Original 5-Step Approach with Pro ===")
    
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
        'name': 'original_pro_test',
        'description': 'Test original approach with Pro'
    }
    
    # Create agent and run analysis
    agent = ExtendedAnalysisAgent(security, audit, storage)
    
    results = agent.analyze_documents_extended(
        framework_content=framework_content,
        corpus_documents=corpus_documents,
        experiment_config=experiment_config,
        model="vertex_ai/gemini-2.5-pro"
    )
    
    # Save results
    with open(experiment_dir / "artifacts" / "original_pro_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Original Pro results saved to: {experiment_dir / 'artifacts' / 'original_pro_results.json'}")
    return results


def test_enhanced_pro():
    """Test enhanced 6-step approach with Pro."""
    print("=== Testing Enhanced 6-Step Approach with Pro ===")
    
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
        'name': 'enhanced_pro_test',
        'description': 'Test enhanced approach with Pro'
    }
    
    # Create agent and run analysis
    agent = EnhancedAnalysisAgent(security, audit, storage)
    
    results = agent.run_enhanced_analysis(
        framework_content=framework_content,
        corpus_documents=corpus_documents,
        experiment_config=experiment_config,
        model="vertex_ai/gemini-2.5-pro"
    )
    
    # Save results
    with open(experiment_dir / "artifacts" / "enhanced_pro_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Enhanced Pro results saved to: {experiment_dir / 'artifacts' / 'enhanced_pro_results.json'}")
    return results


def main():
    """Run both tests and compare results."""
    print("Testing Pro model with both approaches...")
    print()
    
    # Test original approach with Pro
    original_results = test_original_pro()
    print()
    
    # Test enhanced approach with Pro
    enhanced_results = test_enhanced_pro()
    print()
    
    # Show verification status
    orig_verified = original_results.get('verification', {}).get('verified', False)
    enh_verified = enhanced_results.get('verification', {}).get('verified', False)
    
    print("=== VERIFICATION STATUS ===")
    print(f"Original Pro: {'✓ Verified' if orig_verified else '✗ Not Verified'}")
    print(f"Enhanced Pro: {'✓ Verified' if enh_verified else '✗ Not Verified'}")
    
    # Show markup status
    print()
    print("=== MARKUP STATUS ===")
    markup_available = enhanced_results.get('markup_extraction', {}).get('marked_up_document', '')
    if markup_available:
        print(f"✓ Marked-up document available ({len(markup_available)} characters)")
    else:
        print("✗ No marked-up document available")


if __name__ == "__main__":
    main()
