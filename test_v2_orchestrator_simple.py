#!/usr/bin/env python3
"""
Simple V2 Orchestrator Test
===========================

This script demonstrates the V2 orchestrator working with mock agents
to show the core functionality without requiring full agent implementations.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from discernus.core.v2_orchestrator import V2Orchestrator, V2OrchestratorConfig
from discernus.core.execution_strategies import FullExperimentStrategy, AnalysisOnlyStrategy
from discernus.core.experiment_run_config import ExperimentRunConfig, ExecutionMode
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.run_context import RunContext
from discernus.core.agent_result import AgentResult
from discernus.core.standard_agent import StandardAgent


class MockV2Agent(StandardAgent):
    """Mock V2 agent for testing"""
    
    def __init__(self, name: str, success: bool = True, error_message: str = None):
        super().__init__(
            security=Mock(),
            storage=Mock(),
            audit=Mock(),
            config=None
        )
        self.name = name
        self.success = success
        self.error_message = error_message
    
    def execute(self, run_context: RunContext = None, **kwargs) -> AgentResult:
        """Mock execute method"""
        if self.success:
            return AgentResult(
                success=True,
                artifacts=[{"type": f"{self.name}_artifact", "id": f"{self.name}_123"}],
                metadata={"agent": self.name}
            )
        else:
            return AgentResult(
                success=False,
                artifacts=[],
                metadata={},
                error_message=self.error_message or f"{self.name} failed"
            )
    
    def get_capabilities(self) -> list:
        """Mock capabilities"""
        return [f"{self.name}_capability"]


class Mock:
    """Simple mock class for testing"""
    
    def log_agent_event(self, *args, **kwargs):
        """Mock log_agent_event method - accepts any arguments"""
        pass
    
    def get_logger(self, name):
        """Mock get_logger method"""
        return Mock()


def test_v2_orchestrator_simple():
    """Test V2 orchestrator with mock agents"""
    
    print("🚀 Testing V2 Orchestrator with Mock Agents")
    print("=" * 60)
    
    # Set up experiment path
    experiment_path = "/Volumes/code/discernus/projects/nano_test_experiment"
    
    # Create V2 orchestrator config
    config = V2OrchestratorConfig(
        experiment_id="nano_test_experiment",
        framework_path=f"{experiment_path}/sentiment_binary_v1.md",
        corpus_path=f"{experiment_path}/corpus.md",
        output_dir=f"{experiment_path}/v2_output",
        verification_enabled=True,
        cache_enabled=True,
        debug_mode=True
    )
    
    print(f"📁 Experiment Path: {experiment_path}")
    print(f"📋 Framework: {config.framework_path}")
    print(f"📚 Corpus: {config.corpus_path}")
    print()
    
    # Create security boundary
    security = ExperimentSecurityBoundary(Path(experiment_path))
    
    # Create run folder for this test
    run_folder = Path(experiment_path) / "session" / "v2_simple_test"
    run_folder.mkdir(parents=True, exist_ok=True)
    
    # Create storage and audit
    storage = LocalArtifactStorage(security, run_folder)
    audit = AuditLogger(security, run_folder)
    
    # Create V2 orchestrator
    print("🎯 Creating V2 Orchestrator...")
    orchestrator = V2Orchestrator(
        config=config,
        security=security,
        storage=storage,
        audit=audit
    )
    
    # Create mock agents
    print("🤖 Creating Mock V2 Agents...")
    agents = {
        "coherence": MockV2Agent("coherence"),
        "analysis": MockV2Agent("analysis"),
        "statistical": MockV2Agent("statistical"),
        "evidence": MockV2Agent("evidence"),
        "synthesis": MockV2Agent("synthesis")
    }
    
    # Register agents
    for name, agent in agents.items():
        orchestrator.register_agent(name, agent)
    
    print(f"📊 Registered {len(orchestrator.agents)} agents")
    print(f"🔧 Agent capabilities: {orchestrator.get_agent_capabilities()}")
    print()
    
    # Test Analysis Only Strategy
    print("🧪 Testing Analysis Only Strategy...")
    try:
        strategy = AnalysisOnlyStrategy()
        result = orchestrator.execute_strategy(strategy)
        
        if result.success:
            print("✅ Analysis Only Strategy succeeded!")
            print(f"   Phases completed: {result.phases_completed}")
            print(f"   Artifacts generated: {len(result.artifacts)}")
            if result.execution_time_seconds:
                print(f"   Execution time: {result.execution_time_seconds:.2f} seconds")
        else:
            print(f"❌ Analysis Only Strategy failed: {result.error_message}")
            
    except Exception as e:
        print(f"❌ Analysis Only Strategy error: {e}")
    
    print()
    
    # Test Full Experiment Strategy
    print("🧪 Testing Full Experiment Strategy...")
    try:
        strategy = FullExperimentStrategy()
        result = orchestrator.execute_strategy(strategy)
        
        if result.success:
            print("✅ Full Experiment Strategy succeeded!")
            print(f"   Phases completed: {result.phases_completed}")
            print(f"   Artifacts generated: {len(result.artifacts)}")
            if result.execution_time_seconds:
                print(f"   Execution time: {result.execution_time_seconds:.2f} seconds")
        else:
            print(f"❌ Full Experiment Strategy failed: {result.error_message}")
            
    except Exception as e:
        print(f"❌ Full Experiment Strategy error: {e}")
    
    print()
    print("🎉 V2 Orchestrator test completed!")


if __name__ == "__main__":
    test_v2_orchestrator_simple()
