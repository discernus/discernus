#!/usr/bin/env python3
"""
Inspect Show Your Work Artifacts
===============================

Run a quick analysis and then inspect the actual artifacts saved to disk.
"""

import tempfile
import os
import json
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from discernus.agents.EnhancedAnalysisAgent.agent_multi_tool import EnhancedAnalysisAgentMultiTool
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry

def main():
    # Create temporary experiment directory
    temp_dir = tempfile.mkdtemp()
    print(f"🔍 Using temp directory: {temp_dir}")
    
    # Create required experiment.md file
    experiment_path = os.path.join(temp_dir, "experiment.md")
    with open(experiment_path, "w") as f:
        f.write("# Test Experiment\n")
    
    try:
        # Create real dependencies
        security = ExperimentSecurityBoundary(Path(temp_dir))
        run_folder = Path(temp_dir) / "run_001"
        run_folder.mkdir(exist_ok=True)
        audit = AuditLogger(security, run_folder)
        storage = LocalArtifactStorage(security, run_folder)
        llm_gateway = EnhancedLLMGateway(ModelRegistry())
        
        # Create agent
        agent = EnhancedAnalysisAgentMultiTool(
            security_boundary=security,
            audit_logger=audit,
            storage=storage,
            llm_gateway=llm_gateway
        )
        
        # Simple framework
        simple_framework = """
        # Simple Test Framework v1.0
        
        ## Purpose
        Test framework for artifact inspection
        
        ## Dimensions
        - populism: Measures populist rhetoric
        - authoritarianism: Measures authoritarian tendencies
        
        ## Scoring
        Each dimension scored 0.0-1.0 with confidence and salience
        """
        
        document_content = """
        The people are being betrayed by the elite establishment. 
        We need to restore power to the working class and drain the swamp.
        The crisis is real and only I can fix it.
        """
        
        print(f"\n=== Running Analysis ===")
        print(f"Document: {document_content.strip()}")
        
        # Run analysis
        result = agent.analyze_document(
            document_content=document_content,
            framework_content=simple_framework,
            document_id="inspection_doc"
        )
        
        print(f"\n=== Analysis Result ===")
        print(f"Success: {result['success']}")
        print(f"Scores artifact: {result['scores_artifact']}")
        print(f"Evidence artifact: {result['evidence_artifact']}")
        print(f"Work artifact: {result['work_artifact']}")
        
        # Inspect artifacts
        print(f"\n=== Inspecting Artifacts ===")
        
        # 1. Analysis Scores
        if result['scores_artifact']:
            print(f"\n📊 ANALYSIS SCORES ARTIFACT:")
            scores_bytes = storage.get_artifact(result['scores_artifact'])
            scores_data = json.loads(scores_bytes.decode('utf-8'))
            print(json.dumps(scores_data, indent=2))
        else:
            print(f"\n📊 ANALYSIS SCORES ARTIFACT: None")
        
        # 2. Evidence Quotes
        if result['evidence_artifact']:
            print(f"\n📝 EVIDENCE QUOTES ARTIFACT:")
            evidence_bytes = storage.get_artifact(result['evidence_artifact'])
            evidence_data = json.loads(evidence_bytes.decode('utf-8'))
            print(json.dumps(evidence_data, indent=2))
        else:
            print(f"\n📝 EVIDENCE QUOTES ARTIFACT: None")
        
        # 3. Computational Work
        if result['work_artifact']:
            print(f"\n🔧 COMPUTATIONAL WORK ARTIFACT:")
            work_bytes = storage.get_artifact(result['work_artifact'])
            work_data = json.loads(work_bytes.decode('utf-8'))
            print(json.dumps(work_data, indent=2))
        else:
            print(f"\n🔧 COMPUTATIONAL WORK ARTIFACT: None")
        
        print(f"\n=== Artifact Files on Disk ===")
        artifacts_dir = run_folder / "artifacts"
        if artifacts_dir.exists():
            for artifact_file in artifacts_dir.iterdir():
                print(f"📁 {artifact_file.name} ({artifact_file.stat().st_size} bytes)")
        
    finally:
        # Don't clean up - let user inspect
        print(f"\n🔍 Artifacts preserved in: {temp_dir}")
        print(f"   Run folder: {run_folder}")
        print(f"   Artifacts: {run_folder / 'artifacts'}")

if __name__ == "__main__":
    main()
