#!/usr/bin/env python3
"""
RAG Synthesis Test Harness
==========================

Fast iteration testing for RAG synthesis components using cached artifacts.
Eliminates need for full experiment runs during synthesis development.

Usage:
    python3 scripts/test_rag_synthesis.py [--artifacts-from latest|specific_hash]
    
Benefits:
- Test synthesis in isolation (seconds not minutes)
- Iterate on synthesis prompts quickly
- Debug data flow between components  
- Test different statistical extraction approaches
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any
import argparse

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from discernus.agents.thin_synthesis.orchestration.pipeline import (
    ProductionThinSynthesisPipeline,
    ProductionPipelineRequest,
    ProductionPipelineResponse
)
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.core.security_boundary import ExperimentSecurityBoundary

def find_latest_artifacts(artifacts_dir: Path) -> Dict[str, str]:
    """Find the most recent complete set of artifacts."""
    artifacts = {}
    
    # Look for the most recent combined analysis
    analysis_files = list(artifacts_dir.glob("combined_analysis_v6_*"))
    if analysis_files:
        latest_analysis = max(analysis_files, key=lambda p: p.stat().st_mtime)
        artifacts['scores_artifact_hash'] = latest_analysis.name
        print(f"📊 Found latest analysis: {latest_analysis.name}")
    
    # Look for corresponding evidence  
    evidence_files = list(artifacts_dir.glob("combined_evidence_v6_*"))
    if evidence_files:
        latest_evidence = max(evidence_files, key=lambda p: p.stat().st_mtime)
        artifacts['evidence_artifact_hash'] = latest_evidence.name
        print(f"📋 Found latest evidence: {latest_evidence.name}")
    
    # Look for framework
    framework_files = list(artifacts_dir.glob("cff_v7.3_*.md"))
    if framework_files:
        latest_framework = max(framework_files, key=lambda p: p.stat().st_mtime)
        artifacts['framework_hash'] = latest_framework.name
        print(f"🧭 Found latest framework: {latest_framework.name}")
        
        # Load framework content
        with open(artifacts_dir / latest_framework.name, 'r') as f:
            artifacts['framework_spec'] = f.read()
    
    # Look for corpus
    corpus_files = list(artifacts_dir.glob("combined_corpus_text_*"))
    if corpus_files:
        latest_corpus = max(corpus_files, key=lambda p: p.stat().st_mtime)
        artifacts['corpus_artifact_hash'] = latest_corpus.name
        print(f"📚 Found latest corpus: {latest_corpus.name}")
    
    return artifacts

def test_synthesis_isolation(test_project: str = "simple_test", 
                           model: str = "vertex_ai/gemini-2.5-pro",
                           focus: str = "comprehensive") -> Dict[str, Any]:
    """Test synthesis pipeline in isolation using cached artifacts."""
    
    print(f"🧪 RAG Synthesis Isolation Test")
    print(f"   Project: {test_project}")
    print(f"   Model: {model}")
    print(f"   Focus: {focus}")
    print()
    
    # Set up paths
    project_dir = project_root / "projects" / test_project
    artifacts_dir = project_dir / "shared_cache" / "artifacts"
    
    if not artifacts_dir.exists():
        raise FileNotFoundError(f"Artifacts directory not found: {artifacts_dir}")
    
    # Find cached artifacts
    artifacts = find_latest_artifacts(artifacts_dir)
    
    if not all(k in artifacts for k in ['scores_artifact_hash', 'evidence_artifact_hash', 'framework_spec']):
        raise ValueError("Missing required cached artifacts for synthesis testing")
    
    # Set up infrastructure  
    security_boundary = ExperimentSecurityBoundary(project_dir)
    test_run_dir = project_dir / "test_synthesis_run"
    test_run_dir.mkdir(exist_ok=True)
    
    storage = LocalArtifactStorage(security_boundary, test_run_dir)
    audit_logger = AuditLogger(test_run_dir / "logs")
    
    # Create MinIO-compatible wrapper like in ThinOrchestrator  
    class MinIOCompatibleStorage:
        def __init__(self, local_storage, shared_artifacts_dir):
            self.local_storage = local_storage
            self.shared_artifacts_dir = shared_artifacts_dir
            
        def put_artifact(self, content: bytes):
            return self.local_storage.put_artifact(content, {})
            
        def get_artifact(self, hash_id: str):
            # Try local storage first, then shared cache
            try:
                return self.local_storage.get_artifact(hash_id)
            except:
                # Fallback to shared cache for testing
                shared_file = self.shared_artifacts_dir / hash_id
                if shared_file.exists():
                    return shared_file.read_bytes()
                raise
                
        def artifact_exists(self, hash_id: str):
            if self.local_storage.artifact_exists(hash_id):
                return True
            # Check shared cache
            shared_file = self.shared_artifacts_dir / hash_id
            return shared_file.exists()
    
    compatible_storage = MinIOCompatibleStorage(storage, artifacts_dir)
    
    # Initialize synthesis pipeline
    pipeline = ProductionThinSynthesisPipeline(
        artifact_client=compatible_storage,
        audit_logger=audit_logger,
        model=model
    )
    
    print(f"🏭 Synthesis pipeline initialized")
    
    # Create synthesis request
    request = ProductionPipelineRequest(
        framework_spec=artifacts['framework_spec'],
        scores_artifact_hash=artifacts['scores_artifact_hash'],
        evidence_artifact_hash=artifacts['evidence_artifact_hash'],
        corpus_artifact_hash=artifacts.get('corpus_artifact_hash'),
        experiment_context=f"Isolation test for {test_project}",
        interpretation_focus=focus,
        framework_hash=artifacts.get('framework_hash'),
        framework_name="cff_v7.3"
    )
    
    print(f"📋 Testing synthesis with cached artifacts...")
    print(f"   Scores: {request.scores_artifact_hash}")
    print(f"   Evidence: {request.evidence_artifact_hash}")
    print(f"   Framework: {request.framework_name}")
    print()
    
    # Run synthesis in isolation
    try:
        response = pipeline.run(request)
        
        print(f"✅ Synthesis completed successfully!")
        print(f"   Success: {response.success}")
        print(f"   Report length: {len(response.synthesis_report) if response.synthesis_report else 0} chars")
        print(f"   Statistical results: {len(response.statistical_results) if response.statistical_results else 0} items")
        print(f"   Evidence used: {len(response.curated_evidence) if response.curated_evidence else 0} pieces")
        
        if response.error_message:
            print(f"⚠️  Warnings: {response.error_message}")
            
        return {
            'success': response.success,
            'report': response.synthesis_report,
            'statistical_results': response.statistical_results,
            'evidence_count': len(response.curated_evidence) if response.curated_evidence else 0,
            'artifacts_used': artifacts
        }
        
    except Exception as e:
        print(f"❌ Synthesis failed: {e}")
        raise

def preview_synthesis_inputs(test_project: str = "simple_test") -> None:
    """Preview what data will be available to synthesis agents."""
    
    project_dir = project_root / "projects" / test_project
    artifacts_dir = project_dir / "shared_cache" / "artifacts"
    
    print(f"🔍 RAG Synthesis Input Preview")
    print(f"   Project: {test_project}")
    print()
    
    artifacts = find_latest_artifacts(artifacts_dir)
    
    # Set up storage to read cached artifacts
    security_boundary = ExperimentSecurityBoundary(project_dir)
    test_run_dir = project_dir / "test_synthesis_preview"
    test_run_dir.mkdir(exist_ok=True)
    storage = LocalArtifactStorage(security_boundary, test_run_dir)
    
    # Preview analysis scores by reading directly from shared cache
    if 'scores_artifact_hash' in artifacts:
        scores_file = artifacts_dir / artifacts['scores_artifact_hash'] 
        if scores_file.exists():
            with open(scores_file, 'r') as f:
                scores_data = json.load(f)
            print(f"📊 Analysis Scores Preview:")
            print(f"   Documents: {len(scores_data.get('document_analyses', []))}")
            if scores_data.get('document_analyses'):
                first_doc = scores_data['document_analyses'][0]
                print(f"   Sample scores: {len(first_doc.get('analysis_scores', {}))} dimensions")
                print(f"   Sample document: {first_doc.get('document_name', 'Unknown')}")
            print()
    
    # Preview evidence by reading directly from shared cache
    if 'evidence_artifact_hash' in artifacts:
        evidence_file = artifacts_dir / artifacts['evidence_artifact_hash']
        if evidence_file.exists():
            with open(evidence_file, 'r') as f:
                evidence_data = json.load(f)
            print(f"📋 Evidence Preview:")
            print(f"   Total evidence pieces: {len(evidence_data.get('evidence_items', []))}")
            if evidence_data.get('evidence_items'):
                dimensions = set(item.get('dimension') for item in evidence_data['evidence_items'])
                print(f"   Dimensions with evidence: {len(dimensions)}")
                print(f"   Sample dimensions: {list(dimensions)[:5]}")
            print()

def main():
    parser = argparse.ArgumentParser(description="Test RAG synthesis in isolation")
    parser.add_argument('--project', default='simple_test', help='Test project name')
    parser.add_argument('--model', default='vertex_ai/gemini-2.5-pro', help='LLM model to use')
    parser.add_argument('--focus', default='comprehensive', help='Interpretation focus')
    parser.add_argument('--preview-only', action='store_true', help='Only preview inputs, do not run synthesis')
    
    args = parser.parse_args()
    
    try:
        if args.preview_only:
            preview_synthesis_inputs(args.project)
        else:
            result = test_synthesis_isolation(args.project, args.model, args.focus)
            
            # Save test result for analysis
            output_file = f"test_synthesis_result_{args.project}.json"
            with open(output_file, 'w') as f:
                json.dump({
                    'timestamp': str(Path().cwd()),
                    'project': args.project,
                    'model': args.model,
                    'focus': args.focus,
                    'success': result['success'],
                    'report_length': len(result['report']) if result['report'] else 0,
                    'statistical_results_count': len(result['statistical_results']) if result['statistical_results'] else 0,
                    'evidence_count': result['evidence_count'],
                    'artifacts_used': result['artifacts_used']
                }, f, indent=2)
            
            print(f"📁 Test results saved to: {output_file}")
            
            # Show report preview
            if result['report']:
                print(f"\n📄 Synthesis Report Preview (first 500 chars):")
                print("-" * 60)
                print(result['report'][:500] + "..." if len(result['report']) > 500 else result['report'])
                print("-" * 60)
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
