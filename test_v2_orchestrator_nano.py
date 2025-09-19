#!/usr/bin/env python3
"""
Test V2 Orchestrator with Nano Experiment
=========================================

This script demonstrates the V2 orchestrator working with the nano test experiment.
It shows how the V2 orchestrator can execute experiments using the new agent architecture.
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
from discernus.agents.analysis_agent.main import AnalysisAgent
from discernus.agents.statistical_agent.main import StatisticalAgent
from discernus.agents.unified_synthesis_agent.v2_unified_synthesis_agent import V2UnifiedSynthesisAgent
from discernus.agents.evidence_retriever_agent.v2_evidence_retriever_agent import V2EvidenceRetrieverAgent
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry


def create_v2_agents(experiment_path: str):
    """Create V2 agents for the experiment"""
    
    # Create security boundary
    security = ExperimentSecurityBoundary(Path(experiment_path))
    
    # Create run folder for this test
    run_folder = Path(experiment_path) / "session" / "v2_test_run"
    run_folder.mkdir(parents=True, exist_ok=True)
    
    # Create storage and audit
    storage = LocalArtifactStorage(security, run_folder)
    audit = AuditLogger(security, run_folder)
    
    # Create model registry and gateway
    model_registry = ModelRegistry()
    gateway = EnhancedLLMGateway(model_registry)
    
    # Create V2 agents
    agents = {}
    
    # Analysis Agent (legacy but compatible)
    try:
        analysis_agent = AnalysisAgent(
            security_boundary=security,
            audit_logger=audit,
            artifact_storage=storage
        )
        agents["analysis"] = analysis_agent
        print("✅ Analysis Agent created")
    except Exception as e:
        print(f"❌ Analysis Agent failed: {e}")
    
    # Statistical Agent (legacy but compatible)
    try:
        statistical_agent = StatisticalAgent(
            security=security,
            storage=storage,
            audit=audit
        )
        agents["statistical"] = statistical_agent
        print("✅ Statistical Agent created")
    except Exception as e:
        print(f"❌ Statistical Agent failed: {e}")
    
    # V2 Evidence Retriever Agent
    try:
        evidence_agent = V2EvidenceRetrieverAgent(
            security=security,
            storage=storage,
            audit=audit
        )
        agents["evidence"] = evidence_agent
        print("✅ V2 Evidence Retriever Agent created")
    except Exception as e:
        print(f"❌ V2 Evidence Retriever Agent failed: {e}")
    
    # V2 Synthesis Agent
    try:
        synthesis_agent = V2UnifiedSynthesisAgent(
            security=security,
            storage=storage,
            audit=audit
        )
        agents["synthesis"] = synthesis_agent
        print("✅ V2 Synthesis Agent created")
    except Exception as e:
        print(f"❌ V2 Synthesis Agent failed: {e}")
    
    return agents, security, storage, audit


def test_v2_orchestrator():
    """Test V2 orchestrator with nano experiment"""
    
    print("🚀 Testing V2 Orchestrator with Nano Experiment")
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
    
    # Create agents
    print("🤖 Creating V2 Agents...")
    agents, security, storage, audit = create_v2_agents(experiment_path)
    print()
    
    if not agents:
        print("❌ No agents created successfully. Exiting.")
        return
    
    # Create V2 orchestrator
    print("🎯 Creating V2 Orchestrator...")
    orchestrator = V2Orchestrator(
        config=config,
        security=security,
        storage=storage,
        audit=audit
    )
    
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
    
    # Test Full Experiment Strategy (if we have all agents)
    if len(agents) >= 3:  # analysis, statistical, synthesis
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
    else:
        print("⚠️  Skipping Full Experiment Strategy - not enough agents available")
    
    print()
    print("🎉 V2 Orchestrator test completed!")


if __name__ == "__main__":
    test_v2_orchestrator()
