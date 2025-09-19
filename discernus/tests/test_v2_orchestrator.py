#!/usr/bin/env python3
"""
Tests for V2 Orchestrator
=========================

Test the V2 orchestrator core functionality, execution strategies,
and configuration system.
"""

import pytest
import json
from unittest.mock import Mock, patch
from datetime import datetime, timezone

from discernus.core.v2_orchestrator import V2Orchestrator, V2OrchestratorConfig
from discernus.core.execution_strategies import (
    ExecutionStrategy, ExperimentResult, FullExperimentStrategy,
    AnalysisOnlyStrategy, StatisticalPrepStrategy, ResumeFromStatsStrategy
)
from discernus.core.experiment_run_config import (
    ExperimentRunConfig, ExecutionMode, VerificationLevel,
    ModelConfig, CacheConfig, VerificationConfig, ResumeConfig
)
from discernus.core.run_context import RunContext
from discernus.core.agent_result import AgentResult
from discernus.core.standard_agent import StandardAgent


class MockAgent(StandardAgent):
    """Mock agent for testing"""
    
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


class TestV2OrchestratorConfig:
    """Test V2OrchestratorConfig"""
    
    def test_config_creation(self):
        """Test basic config creation"""
        config = V2OrchestratorConfig(
            experiment_id="test_exp",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus",
            output_dir="/test/output"
        )
        
        assert config.experiment_id == "test_exp"
        assert config.framework_path == "/test/framework.yaml"
        assert config.corpus_path == "/test/corpus"
        assert config.output_dir == "/test/output"
        assert config.resume_from_phase is None
        assert config.verification_enabled is True
        assert config.cache_enabled is True
        assert config.debug_mode is False


class TestV2Orchestrator:
    """Test V2Orchestrator core functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.config = V2OrchestratorConfig(
            experiment_id="test_exp",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus",
            output_dir="/test/output"
        )
        
        self.mock_security = Mock()
        self.mock_storage = Mock()
        self.mock_audit = Mock()
        
        self.orchestrator = V2Orchestrator(
            config=self.config,
            security=self.mock_security,
            storage=self.mock_storage,
            audit=self.mock_audit
        )
    
    def test_orchestrator_initialization(self):
        """Test orchestrator initialization"""
        assert self.orchestrator.config == self.config
        assert self.orchestrator.security == self.mock_security
        assert self.orchestrator.storage == self.mock_storage
        assert self.orchestrator.audit == self.mock_audit
        assert self.orchestrator.agents == {}
    
    def test_register_agent(self):
        """Test agent registration"""
        agent = MockAgent("test_agent")
        
        self.orchestrator.register_agent("test_agent", agent)
        
        assert "test_agent" in self.orchestrator.agents
        assert self.orchestrator.agents["test_agent"] == agent
    
    def test_get_agent(self):
        """Test getting registered agent"""
        agent = MockAgent("test_agent")
        self.orchestrator.register_agent("test_agent", agent)
        
        retrieved_agent = self.orchestrator.get_agent("test_agent")
        assert retrieved_agent == agent
        
        # Test non-existent agent
        assert self.orchestrator.get_agent("non_existent") is None
    
    def test_list_agents(self):
        """Test listing agents"""
        agent1 = MockAgent("agent1")
        agent2 = MockAgent("agent2")
        
        self.orchestrator.register_agent("agent1", agent1)
        self.orchestrator.register_agent("agent2", agent2)
        
        agent_list = self.orchestrator.list_agents()
        assert set(agent_list) == {"agent1", "agent2"}
    
    def test_get_agent_capabilities(self):
        """Test getting agent capabilities"""
        agent1 = MockAgent("agent1")
        agent2 = MockAgent("agent2")
        
        self.orchestrator.register_agent("agent1", agent1)
        self.orchestrator.register_agent("agent2", agent2)
        
        capabilities = self.orchestrator.get_agent_capabilities()
        assert capabilities["agent1"] == ["agent1_capability"]
        assert capabilities["agent2"] == ["agent2_capability"]
    
    def test_create_resume_manifest(self):
        """Test creating resume manifest"""
        run_context = RunContext(
            experiment_id="test_exp",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus"
        )
        run_context.current_phase = "analysis"
        run_context.completed_phases = ["coherence"]
        run_context.artifact_hashes = {"artifact1": "hash1"}
        
        manifest = self.orchestrator.create_resume_manifest(run_context)
        
        assert manifest["experiment_id"] == "test_exp"
        assert manifest["current_phase"] == "analysis"
        assert manifest["completed_phases"] == ["coherence"]
        assert manifest["artifact_hashes"] == {"artifact1": "hash1"}
        assert manifest["orchestrator_version"] == "v2"
    
    def test_load_resume_manifest(self):
        """Test loading resume manifest"""
        manifest_data = {
            "experiment_id": "test_exp",
            "orchestrator_version": "v2",
            "current_phase": "analysis"
        }
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(json.dumps(manifest_data))):
            manifest = self.orchestrator.load_resume_manifest("/test/manifest.json")
            
            assert manifest["experiment_id"] == "test_exp"
            assert manifest["orchestrator_version"] == "v2"
    
    def test_resume_from_manifest(self):
        """Test resuming from manifest"""
        manifest = {
            "experiment_id": "test_exp",
            "framework_path": "/test/framework.yaml",
            "corpus_path": "/test/corpus",
            "current_phase": "analysis",
            "completed_phases": ["coherence"],
            "artifact_hashes": {"artifact1": "hash1"}
        }
        
        run_context = self.orchestrator.resume_from_manifest(manifest)
        
        assert run_context.experiment_id == "test_exp"
        assert run_context.current_phase == "analysis"
        assert run_context.completed_phases == ["coherence"]
        assert run_context.artifact_hashes == {"artifact1": "hash1"}


class TestExecutionStrategies:
    """Test execution strategies"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_storage = Mock()
        self.mock_audit = Mock()
        self.run_context = RunContext(
            experiment_id="test_exp",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus"
        )
    
    def test_full_experiment_strategy_success(self):
        """Test full experiment strategy with success"""
        agents = {
            "coherence": MockAgent("coherence"),
            "analysis": MockAgent("analysis"),
            "statistical": MockAgent("statistical"),
            "evidence": MockAgent("evidence"),
            "synthesis": MockAgent("synthesis")
        }
        
        strategy = FullExperimentStrategy()
        result = strategy.execute(agents, self.run_context, self.mock_storage, self.mock_audit)
        
        assert result.success is True
        assert "coherence" in result.phases_completed
        assert "analysis" in result.phases_completed
        assert "statistical" in result.phases_completed
        assert "evidence" in result.phases_completed
        assert "synthesis" in result.phases_completed
        assert len(result.artifacts) == 5  # One artifact per agent
    
    def test_full_experiment_strategy_failure(self):
        """Test full experiment strategy with failure"""
        agents = {
            "coherence": MockAgent("coherence"),
            "analysis": MockAgent("analysis", success=False, error_message="Analysis failed"),
            "statistical": MockAgent("statistical"),
            "evidence": MockAgent("evidence"),
            "synthesis": MockAgent("synthesis")
        }
        
        strategy = FullExperimentStrategy()
        result = strategy.execute(agents, self.run_context, self.mock_storage, self.mock_audit)
        
        assert result.success is False
        assert "coherence" in result.phases_completed
        assert "analysis" not in result.phases_completed
        assert "Analysis failed" in result.error_message
    
    def test_analysis_only_strategy(self):
        """Test analysis-only strategy"""
        agents = {
            "coherence": MockAgent("coherence"),
            "analysis": MockAgent("analysis")
        }
        
        strategy = AnalysisOnlyStrategy()
        result = strategy.execute(agents, self.run_context, self.mock_storage, self.mock_audit)
        
        assert result.success is True
        assert "coherence" in result.phases_completed
        assert "analysis" in result.phases_completed
        assert "statistical" not in result.phases_completed
        assert len(result.artifacts) == 2
    
    def test_statistical_prep_strategy(self):
        """Test statistical prep strategy"""
        agents = {
            "coherence": MockAgent("coherence"),
            "analysis": MockAgent("analysis"),
            "statistical": MockAgent("statistical")
        }
        
        strategy = StatisticalPrepStrategy()
        result = strategy.execute(agents, self.run_context, self.mock_storage, self.mock_audit)
        
        assert result.success is True
        assert "coherence" in result.phases_completed
        assert "analysis" in result.phases_completed
        assert "statistical" in result.phases_completed
        assert "evidence" not in result.phases_completed
        assert len(result.artifacts) == 3
    
    def test_resume_from_stats_strategy(self):
        """Test resume from stats strategy"""
        # Set up run context with statistical results
        self.run_context.statistical_results = {"test": "data"}
        
        agents = {
            "evidence": MockAgent("evidence"),
            "synthesis": MockAgent("synthesis")
        }
        
        strategy = ResumeFromStatsStrategy()
        result = strategy.execute(agents, self.run_context, self.mock_storage, self.mock_audit)
        
        assert result.success is True
        assert "evidence" in result.phases_completed
        assert "synthesis" in result.phases_completed
        assert len(result.artifacts) == 2
    
    def test_resume_from_stats_strategy_no_stats(self):
        """Test resume from stats strategy with no statistical results"""
        agents = {
            "evidence": MockAgent("evidence"),
            "synthesis": MockAgent("synthesis")
        }
        
        strategy = ResumeFromStatsStrategy()
        result = strategy.execute(agents, self.run_context, self.mock_storage, self.mock_audit)
        
        assert result.success is False
        assert "No statistical results found for resume" in result.error_message


class TestExperimentRunConfig:
    """Test ExperimentRunConfig"""
    
    def test_config_creation(self):
        """Test basic config creation"""
        config = ExperimentRunConfig(
            experiment_id="test_exp",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus",
            output_dir="/test/output"
        )
        
        assert config.experiment_id == "test_exp"
        assert config.execution_mode == ExecutionMode.FULL_EXPERIMENT
        assert config.debug_mode is False
        assert config.dry_run is False
    
    def test_config_serialization(self):
        """Test config serialization to dict"""
        config = ExperimentRunConfig(
            experiment_id="test_exp",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus",
            output_dir="/test/output"
        )
        
        config_dict = config.to_dict()
        
        assert config_dict["experiment_id"] == "test_exp"
        assert config_dict["execution_mode"] == "full_experiment"
        assert config_dict["debug_mode"] is False
    
    def test_config_deserialization(self):
        """Test config deserialization from dict"""
        config_dict = {
            "experiment_id": "test_exp",
            "framework_path": "/test/framework.yaml",
            "corpus_path": "/test/corpus",
            "output_dir": "/test/output",
            "execution_mode": "analysis_only",
            "debug_mode": True
        }
        
        config = ExperimentRunConfig.from_dict(config_dict)
        
        assert config.experiment_id == "test_exp"
        assert config.execution_mode == ExecutionMode.ANALYSIS_ONLY
        assert config.debug_mode is True
    
    def test_get_agent_model(self):
        """Test getting agent model"""
        config = ExperimentRunConfig(
            experiment_id="test_exp",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus",
            output_dir="/test/output"
        )
        
        assert config.get_agent_model("analysis") == "vertex_ai/gemini-2.5-flash"
        assert config.get_agent_model("verification") == "vertex_ai/gemini-2.5-flash-lite"
        assert config.get_agent_model("unknown") == "vertex_ai/gemini-2.5-flash"
    
    def test_should_verify_phase(self):
        """Test phase verification check"""
        config = ExperimentRunConfig(
            experiment_id="test_exp",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus",
            output_dir="/test/output"
        )
        
        assert config.should_verify_phase("analysis") is True
        assert config.should_verify_phase("statistical") is True
        assert config.should_verify_phase("evidence") is False
        assert config.should_verify_phase("synthesis") is False
    
    def test_is_resume_enabled(self):
        """Test resume enabled check"""
        config = ExperimentRunConfig(
            experiment_id="test_exp",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus",
            output_dir="/test/output"
        )
        
        assert config.is_resume_enabled() is False
        
        config.resume.enabled = True
        config.resume.resume_from_phase = "analysis"
        assert config.is_resume_enabled() is True
    
    def test_validate_config(self):
        """Test config validation"""
        config = ExperimentRunConfig(
            experiment_id="test_exp",
            framework_path="/test/framework.yaml",
            corpus_path="/test/corpus",
            output_dir="/test/output"
        )
        
        # Mock file existence for validation
        with patch('pathlib.Path.exists', return_value=True):
            errors = config.validate()
            assert len(errors) == 0
        
        # Test with missing required fields
        config.experiment_id = ""
        errors = config.validate()
        assert "experiment_id is required" in errors


def mock_open(content):
    """Mock open function for file operations"""
    from unittest.mock import mock_open as _mock_open
    return _mock_open(read_data=content)


if __name__ == "__main__":
    pytest.main([__file__])
