#!/usr/bin/env python3
"""
Test V2 Orchestrator with Nano Experiment
=========================================

This script tests the V2 orchestrator with the nano_test_experiment using
available V2 agents and mock agents for missing functionality.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import Mock, patch

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from discernus.core.v2_orchestrator import V2Orchestrator
from discernus.core.execution_strategies import FullExperimentStrategy
from discernus.core.experiment_run_config import ExperimentRunConfig
from discernus.core.run_context import RunContext
from discernus.core.agent_result import AgentResult
from discernus.core.standard_agent import StandardAgent
from discernus.core.agent_config import AgentConfig
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.agents.evidence_retriever_agent.v2_evidence_retriever_agent import V2EvidenceRetrieverAgent
from discernus.agents.unified_synthesis_agent.v2_unified_synthesis_agent import V2UnifiedSynthesisAgent


class MockV2AnalysisAgent(StandardAgent):
    """Mock V2 Analysis Agent for testing"""
    
    def __init__(self, security, storage, audit, config=None):
        super().__init__(security, storage, audit, config)
        self.agent_name = "MockV2AnalysisAgent"
    
    def execute(self, run_context: RunContext = None, **kwargs) -> AgentResult:
        """Mock analysis execution"""
        print(f"🔍 Mock Analysis Agent executing...")
        
        # Simulate analysis results
        analysis_results = {
            "document_1": {
                "sentiment_score": 0.8,
                "confidence": 0.9,
                "evidence": "This is a positive sentiment document"
            },
            "document_2": {
                "sentiment_score": 0.2,
                "confidence": 0.85,
                "evidence": "This is a negative sentiment document"
            }
        }
        
        derived_metrics = {
            "average_sentiment": 0.5,
            "sentiment_variance": 0.18,
            "positive_documents": 1,
            "negative_documents": 1
        }
        
        # Update run context
        if run_context:
            run_context.analysis_results = analysis_results
            run_context.derived_metrics = derived_metrics
            run_context.analysis_artifacts = ["analysis_artifact_1", "analysis_artifact_2"]
        
        return AgentResult(
            success=True,
            artifacts=[
                {
                    "type": "analysis_results",
                    "content": analysis_results,
                    "metadata": {"phase": "analysis", "timestamp": "2024-12-19T10:00:00Z"}
                },
                {
                    "type": "derived_metrics", 
                    "content": derived_metrics,
                    "metadata": {"phase": "analysis", "timestamp": "2024-12-19T10:00:00Z"}
                }
            ],
            metadata={"phase": "analysis", "documents_analyzed": 2, "agent_name": self.agent_name}
        )
    
    def get_capabilities(self) -> List[str]:
        return ["analysis", "derived_metrics"]


class MockV2StatisticalAgent(StandardAgent):
    """Mock V2 Statistical Agent for testing"""
    
    def __init__(self, security, storage, audit, config=None):
        super().__init__(security, storage, audit, config)
        self.agent_name = "MockV2StatisticalAgent"
    
    def execute(self, run_context: RunContext = None, **kwargs) -> AgentResult:
        """Mock statistical execution"""
        print(f"📊 Mock Statistical Agent executing...")
        
        # Simulate statistical results
        statistical_results = {
            "descriptive_stats": {
                "mean_sentiment": 0.5,
                "std_sentiment": 0.42,
                "min_sentiment": 0.2,
                "max_sentiment": 0.8
            },
            "correlation_analysis": {
                "sentiment_confidence_correlation": 0.75
            },
            "significance_tests": {
                "sentiment_difference_p_value": 0.15
            }
        }
        
        # Update run context
        if run_context:
            run_context.statistical_results = statistical_results
        
        return AgentResult(
            success=True,
            artifacts=[
                {
                    "type": "statistical_results",
                    "content": statistical_results,
                    "metadata": {"phase": "statistical", "timestamp": "2024-12-19T10:01:00Z"}
                }
            ],
            metadata={"phase": "statistical", "tests_performed": 3, "agent_name": self.agent_name}
        )
    
    def get_capabilities(self) -> List[str]:
        return ["statistical_analysis", "significance_testing"]


class MockV2EvidenceAgent(StandardAgent):
    """Mock V2 Evidence Agent for testing"""
    
    def __init__(self, security, storage, audit, config=None):
        super().__init__(security, storage, audit, config)
        self.agent_name = "MockV2EvidenceAgent"
    
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


class MockV2SynthesisAgent(StandardAgent):
    """Mock V2 Synthesis Agent for testing"""
    
    def __init__(self, security, storage, audit, config=None):
        super().__init__(security, storage, audit, config)
        self.agent_name = "MockV2SynthesisAgent"
    
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
    """Test V2 orchestrator with nano experiment"""
    print("🚀 Testing V2 Orchestrator with Nano Experiment")
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
        run_folder = experiment_path / "session" / "v2_nano_test"
        run_folder.mkdir(parents=True, exist_ok=True)
        storage = LocalArtifactStorage(security, run_folder)
        audit = AuditLogger(security, run_folder)
        
        print(f"🛡️ Security: Boundary established for experiment '{security.experiment_name}'")
        print(f"🛡️ Security: Allowed root = {security.experiment_root}")
        print(f"🗄️ Local artifact storage initialized: {storage.artifacts_dir}")
        print(f"📋 Audit logging initialized: {audit.logs_dir}")
        
        # Create V2 orchestrator config
        print("\n🎯 Creating V2 Orchestrator...")
        from discernus.core.v2_orchestrator import V2OrchestratorConfig
        orchestrator_config = V2OrchestratorConfig(
            experiment_id=security.experiment_name,
            framework_path=str(framework_path),
            corpus_path=str(corpus_path),
            output_dir=str(run_folder)
        )
        orchestrator = V2Orchestrator(orchestrator_config, security, storage, audit)
        
        # Create agents
        print("🤖 Creating V2 Agents...")
        config = AgentConfig()
        
        # Create V2 agents
        analysis_agent = MockV2AnalysisAgent(security, storage, audit, config)
        statistical_agent = MockV2StatisticalAgent(security, storage, audit, config)
        evidence_agent = MockV2EvidenceAgent(security, storage, audit, config)
        synthesis_agent = MockV2SynthesisAgent(security, storage, audit, config)
        
        # Register agents
        orchestrator.register_agent("analysis", analysis_agent)
        orchestrator.register_agent("statistical", statistical_agent)
        orchestrator.register_agent("evidence", evidence_agent)
        orchestrator.register_agent("synthesis", synthesis_agent)
        
        print(f"📊 Registered {len(orchestrator.agents)} agents")
        
        # Create run context
        run_context = RunContext(
            experiment_id=security.experiment_name,
            framework_path=framework_path,
            corpus_path=corpus_path,
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
        print("\n🧪 Testing Full Experiment Strategy...")
        strategy = FullExperimentStrategy()
        
        result = orchestrator.execute_strategy(strategy)
        
        if result.success:
            print("✅ Full Experiment Strategy succeeded!")
            print(f"   Phases completed: {result.phases_completed}")
            print(f"   Artifacts generated: {len(result.artifacts)}")
            print(f"   Execution time: {result.execution_time_seconds:.2f} seconds")
            
            # Show some artifacts
            print("\n📋 Generated Artifacts:")
            for i, artifact in enumerate(result.artifacts[:3]):  # Show first 3
                print(f"   {i+1}. {artifact.get('type', 'unknown')} - {artifact.get('metadata', {}).get('phase', 'unknown')}")
            
            if len(result.artifacts) > 3:
                print(f"   ... and {len(result.artifacts) - 3} more artifacts")
            
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
        print("\n🎉 V2 Orchestrator nano experiment test completed successfully!")
    else:
        print("\n💥 V2 Orchestrator nano experiment test failed!")
        sys.exit(1)
