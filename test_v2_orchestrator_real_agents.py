#!/usr/bin/env python3
"""
Test V2 Orchestrator with Real V2 Agents
=========================================

This script tests the V2 orchestrator with the nano_test_experiment using
real V2 agents (V2AnalysisAgent and V2StatisticalAgent) instead of mock agents.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import Mock, patch

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from discernus.core.v2_orchestrator import V2Orchestrator, V2OrchestratorConfig
from discernus.core.execution_strategies import FullExperimentStrategy
from discernus.core.experiment_run_config import ExperimentRunConfig
from discernus.core.run_context import RunContext
from discernus.core.agent_result import AgentResult
from discernus.core.agent_config import AgentConfig
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.agents.analysis_agent.v2_analysis_agent import V2AnalysisAgent
from discernus.agents.statistical_agent.v2_statistical_agent import V2StatisticalAgent
from discernus.agents.evidence_retriever_agent.v2_evidence_retriever_agent import V2EvidenceRetrieverAgent
from discernus.agents.unified_synthesis_agent.v2_unified_synthesis_agent import V2UnifiedSynthesisAgent


class MockV2EvidenceAgent:
    """Mock V2 Evidence Agent for testing (V2EvidenceRetrieverAgent has issues)"""
    
    def __init__(self, security, storage, audit, config=None):
        self.agent_name = "MockV2EvidenceAgent"
        self.security = security
        self.storage = storage
        self.audit = audit
        self.config = config or {}
    
    def execute(self, run_context: RunContext = None, **kwargs) -> AgentResult:
        """Mock evidence execution"""
        print(f"🔍 Mock Evidence Agent executing...")
        
        # Simulate evidence results
        evidence_results = {
            "evidence_quotes": [
                {
                    "quote": "This is a positive sentiment example",
                    "document_id": "document_1",
                    "relevance_score": 0.9
                },
                {
                    "quote": "This is a negative sentiment example", 
                    "document_id": "document_2",
                    "relevance_score": 0.8
                }
            ],
            "total_quotes_found": 2
        }
        
        # Update run context
        if run_context:
            run_context.evidence = evidence_results
        
        return AgentResult(
            success=True,
            artifacts=[
                {
                    "type": "evidence_results",
                    "content": evidence_results,
                    "metadata": {"phase": "evidence", "timestamp": "2024-12-19T10:02:00Z"}
                }
            ],
            metadata={"phase": "evidence", "quotes_found": 2, "agent_name": self.agent_name}
        )
    
    def get_capabilities(self) -> List[str]:
        return ["evidence_retrieval", "quote_extraction"]


class MockV2SynthesisAgent:
    """Mock V2 Synthesis Agent for testing (V2UnifiedSynthesisAgent has issues)"""
    
    def __init__(self, security, storage, audit, config=None):
        self.agent_name = "MockV2SynthesisAgent"
        self.security = security
        self.storage = storage
        self.audit = audit
        self.config = config or {}
    
    def execute(self, run_context: RunContext = None, **kwargs) -> AgentResult:
        """Mock synthesis execution"""
        print(f"📝 Mock Synthesis Agent executing...")
        
        # Simulate synthesis results
        synthesis_results = {
            "report_title": "Nano Test Experiment Results",
            "executive_summary": "This experiment successfully validated the V2 orchestrator pipeline.",
            "key_findings": [
                "Positive sentiment documents: 1",
                "Negative sentiment documents: 1", 
                "Average sentiment score: 0.5"
            ],
            "recommendations": [
                "Continue with V2 orchestrator development",
                "Implement additional test cases"
            ]
        }
        
        return AgentResult(
            success=True,
            artifacts=[
                {
                    "type": "synthesis_report",
                    "content": synthesis_results,
                    "metadata": {"phase": "synthesis", "timestamp": "2024-12-19T10:03:00Z"}
                }
            ],
            metadata={"phase": "synthesis", "report_sections": 4, "agent_name": self.agent_name}
        )
    
    def get_capabilities(self) -> List[str]:
        return ["report_generation", "synthesis"]


def main():
    """Test V2 orchestrator with real V2 agents"""
    print("🚀 Testing V2 Orchestrator with Real V2 Agents")
    print("=" * 60)
    
    # Setup paths
    experiment_path = Path("/Volumes/code/discernus/projects/nano_test_experiment")
    framework_path = experiment_path / "sentiment_binary_v1.md"
    corpus_path = experiment_path / "corpus.md"
    
    print(f"📁 Experiment Path: {experiment_path}")
    print(f"📋 Framework: {framework_path}")
    print(f"📚 Corpus: {corpus_path}")
    
    # Verify experiment exists
    if not experiment_path.exists():
        print(f"❌ Experiment path does not exist: {experiment_path}")
        return False
    
    if not framework_path.exists():
        print(f"❌ Framework file does not exist: {framework_path}")
        return False
    
    if not corpus_path.exists():
        print(f"❌ Corpus file does not exist: {corpus_path}")
        return False
    
    try:
        # Initialize security and storage
        print("\n🛡️ Initializing security and storage...")
        security = ExperimentSecurityBoundary(experiment_path)
        run_folder = experiment_path / "session" / "v2_real_test"
        run_folder.mkdir(parents=True, exist_ok=True)
        storage = LocalArtifactStorage(security, run_folder)
        audit = AuditLogger(security, run_folder)
        
        print(f"🛡️ Security: Boundary established for experiment '{security.experiment_name}'")
        print(f"🛡️ Security: Allowed root = {security.experiment_root}")
        print(f"🗄️ Local artifact storage initialized: {storage.artifacts_dir}")
        print(f"📋 Audit logging initialized: {audit.logs_dir}")
        
        # Create V2 orchestrator config
        print("\n🎯 Creating V2 Orchestrator...")
        orchestrator_config = V2OrchestratorConfig(
            experiment_id=security.experiment_name,
            framework_path=str(framework_path),
            corpus_path=str(corpus_path),
            output_dir=str(run_folder)
        )
        orchestrator = V2Orchestrator(orchestrator_config, security, storage, audit)
        
        # Create real V2 agents
        print("🤖 Creating Real V2 Agents...")
        config = AgentConfig()
        
        # Create real V2 agents
        analysis_agent = V2AnalysisAgent(security, storage, audit, config)
        statistical_agent = V2StatisticalAgent(security, storage, audit, config)
        evidence_agent = MockV2EvidenceAgent(security, storage, audit, config)  # Mock for now
        synthesis_agent = MockV2SynthesisAgent(security, storage, audit, config)  # Mock for now
        
        # Register agents
        orchestrator.register_agent("analysis", analysis_agent)
        orchestrator.register_agent("statistical", statistical_agent)
        orchestrator.register_agent("evidence", evidence_agent)
        orchestrator.register_agent("synthesis", synthesis_agent)
        
        print(f"📊 Registered {len(orchestrator.agents)} agents")
        
        # Create run context
        run_context = RunContext(
            experiment_id=security.experiment_name,
            framework_path=str(framework_path),
            corpus_path=str(corpus_path),
            metadata={
                "experiment_path": str(experiment_path),
                "test_run": True,
                "timestamp": "2024-12-19T10:00:00Z"
            }
        )
        
        # Create experiment config
        experiment_config = ExperimentRunConfig(
            experiment_id=security.experiment_name,
            framework_path=str(framework_path),
            corpus_path=str(corpus_path),
            output_dir=str(run_folder)
        )
        
        # Test full experiment strategy
        print("\n🧪 Testing Full Experiment Strategy with Real V2 Agents...")
        strategy = FullExperimentStrategy()
        
        result = orchestrator.execute_strategy(strategy)
        
        if result.success:
            print("✅ Full Experiment Strategy with Real V2 Agents succeeded!")
            print(f"   Phases completed: {result.phases_completed}")
            print(f"   Artifacts generated: {len(result.artifacts)}")
            print(f"   Execution time: {result.execution_time_seconds:.2f} seconds")
            
            # Show some artifacts
            print("\n📋 Generated Artifacts:")
            for i, artifact in enumerate(result.artifacts[:5]):  # Show first 5
                print(f"   {i+1}. {artifact.get('type', 'unknown')} - {artifact.get('metadata', {}).get('phase', 'unknown')}")
            
            if len(result.artifacts) > 5:
                print(f"   ... and {len(result.artifacts) - 5} more artifacts")
            
            return True
        else:
            print(f"❌ Full Experiment Strategy failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 V2 Orchestrator with Real V2 Agents test completed successfully!")
    else:
        print("\n💥 V2 Orchestrator with Real V2 Agents test failed!")
        sys.exit(1)
