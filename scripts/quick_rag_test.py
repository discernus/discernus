#!/usr/bin/env python3
"""
Quick RAG Synthesis Test
=======================

Fast synthesis testing using known good cached artifacts.
Tests the synthesis pipeline in isolation without full experiment runs.
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from discernus.agents.thin_synthesis.orchestration.pipeline import (
    ProductionThinSynthesisPipeline,
    ProductionPipelineRequest
)
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.core.security_boundary import ExperimentSecurityBoundary

def quick_synthesis_test():
    """Test synthesis using known good cached artifacts."""
    
    print("🧪 Quick RAG Synthesis Test")
    
    # Use known good artifacts from our successful runs
    project_dir = project_root / "projects" / "simple_test"
    artifacts_dir = project_dir / "shared_cache" / "artifacts"
    
    # Known good artifacts (from our earlier successful runs)
    scores_hash = "combined_analysis_v6_41323de5"
    evidence_hash = "combined_evidence_v6_779c7d47" 
    framework_file = "cff_v7.3_f79cf2b2.md"
    corpus_hash = "combined_corpus_text_61fd1028"
    
    # Verify artifacts exist
    required_artifacts = [scores_hash, evidence_hash, framework_file]
    for artifact in required_artifacts:
        if not (artifacts_dir / artifact).exists():
            print(f"❌ Missing required artifact: {artifact}")
            return False
    
    # Load framework content
    with open(artifacts_dir / framework_file, 'r') as f:
        framework_content = f.read()
    
    print(f"📊 Using scores: {scores_hash}")
    print(f"📋 Using evidence: {evidence_hash}")
    print(f"🧭 Using framework: {framework_file}")
    print()
    
    # Set up minimal infrastructure for testing
    security_boundary = ExperimentSecurityBoundary(project_dir)
    test_run_dir = project_dir / "quick_synthesis_test"
    test_run_dir.mkdir(exist_ok=True)
    
    storage = LocalArtifactStorage(security_boundary, test_run_dir)
    audit_logger = AuditLogger(security_boundary, test_run_dir)
    
    # Create compatible storage wrapper
    class TestStorage:
        def __init__(self, shared_dir):
            self.shared_dir = shared_dir
            
        def get_artifact(self, hash_id: str):
            artifact_file = self.shared_dir / hash_id
            if artifact_file.exists():
                return artifact_file.read_bytes()
            raise FileNotFoundError(f"Test artifact not found: {hash_id}")
            
        def artifact_exists(self, hash_id: str):
            return (self.shared_dir / hash_id).exists()
            
        def put_artifact(self, content: bytes):
            # For testing, we don't need to store new artifacts
            return "test_artifact_hash"
    
    test_storage = TestStorage(artifacts_dir)
    
    # Initialize synthesis pipeline
    try:
        pipeline = ProductionThinSynthesisPipeline(
            artifact_client=test_storage,
            audit_logger=audit_logger,
            model="vertex_ai/gemini-2.5-pro"
        )
        print("🏭 Synthesis pipeline initialized")
        
        # Create synthesis request
        request = ProductionPipelineRequest(
            framework_spec=framework_content,
            scores_artifact_hash=scores_hash,
            evidence_artifact_hash=evidence_hash,
            corpus_artifact_hash=corpus_hash,
            experiment_context="Quick synthesis test",
            framework_hash=framework_file.replace('.md', ''),
            framework_name="cff_v7.3"
        )
        
        print("🚀 Running synthesis in isolation...")
        
        # Run synthesis
        response = pipeline.run(request)
        
        if response.success:
            print(f"✅ Synthesis completed successfully!")
            
            # Check what attributes are available
            print(f"📋 Response attributes: {[attr for attr in dir(response) if not attr.startswith('_')]}")
            
            # Access synthesis report (using correct attribute name)
            if response.narrative_report:
                print(f"   Report length: {len(response.narrative_report)} chars")
                print(f"   Executive summary length: {len(response.executive_summary)} chars") 
                print(f"   Key findings: {len(response.key_findings)} items")
                print(f"   Statistical summary: {response.statistical_summary[:100]}...")
                
                output_file = test_run_dir / "synthesis_report.md"
                with open(output_file, 'w') as f:
                    f.write(f"# Synthesis Report\n\n{response.narrative_report}\n\n")
                    f.write(f"## Executive Summary\n\n{response.executive_summary}\n\n")
                    f.write(f"## Key Findings\n\n")
                    for i, finding in enumerate(response.key_findings, 1):
                        f.write(f"{i}. {finding}\n")
                print(f"📄 Report saved: {output_file}")
                
                # Show preview
                print(f"\n📄 Report Preview (first 500 chars):")
                print("-" * 60)
                preview = response.narrative_report[:500]
                if len(response.narrative_report) > 500:
                    preview += "..."
                print(preview)
                print("-" * 60)
            
            # Show artifact hashes for further testing
            print(f"\n📊 Artifact Hashes for Further Testing:")
            print(f"   Statistical results: {response.statistical_results_hash}")
            print(f"   Curated evidence: {response.curated_evidence_hash}")
            print(f"   Analysis plan: {response.analysis_plan_hash}")
                
            return True
            
        else:
            print(f"❌ Synthesis failed: {response.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_synthesis_test()
    sys.exit(0 if success else 1)
