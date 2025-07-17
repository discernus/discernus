#!/usr/bin/env python3
"""
Workflow Orchestrator - THIN, Registry-Aware Workflow Engine
============================================================

THIN Principle: This orchestrator is a simple, dumb loop. It reads a workflow
defined in an experiment.md file and executes a sequence of agents as defined
in the central agent_registry.yaml. All intelligence resides in the experiment
definition and the agents themselves, not in the orchestrator.
"""

import sys
import asyncio
import json
import yaml
import importlib
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import os
import re

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.gateway.model_registry import ModelRegistry
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.base_gateway import BaseGateway
from discernus.core.conversation_logger import ConversationLogger
from discernus.core.project_chronolog import get_project_chronolog, log_project_event

# No longer need to import specific agents, they will be loaded dynamically
# from discernus.agents.analysis_agent import AnalysisAgent
# from discernus.agents.statistical_analysis_agent import StatisticalAnalysisAgent
# from discernus.agents.statistical_interpretation_agent import StatisticalInterpretationAgent
# from discernus.agents.experiment_conclusion_agent import ExperimentConclusionAgent
# from discernus.agents.methodological_overwatch_agent import MethodologicalOverwatchAgent

class WorkflowOrchestrator:
    """
    Executes a dynamic, multi-step experiment workflow defined in experiment.md.
    """

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.results_path = self.project_path / "results"
        self.results_path.mkdir(exist_ok=True)
        
        # Core components
        self.model_registry = ModelRegistry()
        self.gateway: BaseGateway = LLMGateway(self.model_registry)
        self._load_agent_registry()
        
        self.logger = None
        self.session_id = None
        self.workflow_state = {}

    def _load_agent_registry(self):
        """Loads the agent registry from YAML."""
        registry_path = project_root / "discernus" / "core" / "agent_registry.yaml"
        if not registry_path.exists():
            raise FileNotFoundError(f"Agent registry not found at: {registry_path}")
        with open(registry_path, 'r') as f:
            registry_data = yaml.safe_load(f)
        self.agent_registry = {agent['name']: agent for agent in registry_data['agents']}
        print("✅ WorkflowOrchestrator initialized with Agent Registry.")

    def execute_workflow(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Primary execution method for running a defined workflow.
        """
        self._init_session_logging()
        self._log_system_event("WORKFLOW_EXECUTION_STARTED", {"session_id": self.session_id})

        try:
            workflow_steps = initial_state.get('workflow')

            if not workflow_steps:
                raise ValueError("No 'workflow' definition found in the initial state.")

            # Prime the initial state
            self.workflow_state = initial_state
            self.workflow_state['session_results_path'] = str(self.session_results_path)
            self.workflow_state['conversation_id'] = self.conversation_id

            for i, step_config in enumerate(workflow_steps):
                agent_name = step_config.get('agent')
                if not agent_name:
                    raise ValueError(f"Workflow step {i} is missing the 'agent' key.")
                
                self._log_system_event("WORKFLOW_STEP_STARTED", {"step": i + 1, "agent": agent_name})
                
                step_output = self._execute_step(agent_name, step_config)
                
                # Update the master workflow state with the output
                if step_output:
                    self.workflow_state.update(step_output)
                
                self._log_system_event("WORKFLOW_STEP_COMPLETED", {"step": i + 1, "agent": agent_name, "output_keys": list(step_output.keys()) if step_output else []})
                self._save_state_snapshot(f"state_after_step_{i+1}_{agent_name}.json")

            self._log_system_event("WORKFLOW_EXECUTION_COMPLETED", {"session_id": self.session_id})
            
            # The final state contains all the results and paths to artifacts.
            return {"status": "success", "session_id": self.session_id, "final_state": self.workflow_state}

        except Exception as e:
            self._log_system_event("WORKFLOW_EXECUTION_ERROR", {"error": str(e)})
            raise e

    def _execute_step(self, agent_name: str, step_config: Dict[str, Any]) -> Dict[str, Any]:
        """Dynamically loads and executes a single agent step."""
        agent_def = self.agent_registry.get(agent_name)
        if not agent_def:
            raise ValueError(f"Agent '{agent_name}' not found in the registry.")

        agent_instance = self._create_agent_instance(agent_def)
        
        # The agent's execution method is defined in the registry (e.g., "execute")
        execution_method_name = agent_def.get('execution_method', 'execute')
        execution_method = getattr(agent_instance, execution_method_name)
        
        # Pass the whole state and the step config to the agent.
        # The agent is responsible for pulling what it needs.
        result = execution_method(self.workflow_state, step_config)

        # Per the new architecture, agents are responsible for returning a dictionary
        # that can be directly used to update the workflow state.
        if isinstance(result, dict):
            return result
        else:
            print(f"⚠️  Warning: Agent '{agent_name}' did not return a dictionary. Output will be ignored.")
            return {}
    
    def _create_agent_instance(self, agent_def: Dict[str, Any]) -> Any:
        """Dynamically creates an instance of an agent class."""
        module_path = agent_def['module']
        class_name = agent_def['class']
        
        try:
            module = importlib.import_module(module_path)
            agent_class = getattr(module, class_name)
            
            # The new agent design: some need the gateway, some don't.
            # We can inspect the constructor (__init__) to decide what to pass.
            init_params = agent_class.__init__.__code__.co_varnames
            
            if 'gateway' in init_params:
                # Pass the orchestrator's gateway instance (which could be real or mock)
                return agent_class(gateway=self.gateway)
            else:
                return agent_class()

        except (ImportError, AttributeError) as e:
            raise ImportError(f"Could not create agent '{class_name}' from module '{module_path}': {e}")

    def _init_session_logging(self):
        """Initializes logging for the current session."""
        timestamp = datetime.now()
        self.session_id = f"session_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        self.conversation_id = f"conversation_{timestamp.strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
        
        # The CLI now creates the session directory, so we just need to use it.
        # This resolves the chicken-and-egg problem.
        if 'session_results_path' not in self.workflow_state or not self.workflow_state['session_results_path']:
             timestamp_str = timestamp.strftime('%Y-%m-%d_%H-%M-%S')
             self.session_results_path = self.results_path / timestamp_str
             self.session_results_path.mkdir(exist_ok=True)
        else:
            self.session_results_path = Path(self.workflow_state['session_results_path'])
        
        self.logger = ConversationLogger(str(self.project_path))

    def _save_state_snapshot(self, filename: str):
        """Saves the current workflow_state to a file for debugging."""
        snapshot_path = self.session_results_path / filename
        try:
            with open(snapshot_path, 'w', encoding='utf-8') as f:
                # We need a custom default handler for non-serializable objects like Path
                json.dump(self.workflow_state, f, indent=2, default=str)
        except Exception as e:
            print(f"⚠️  Warning: Could not save state snapshot to {snapshot_path}: {e}")

    def _log_system_event(self, event_type: str, event_data: Dict[str, Any]):
        """Logs a system event to both the session log and the project chronolog."""
        # Log to the session-specific conversation log
        if self.logger:
            self.logger.log_llm_message(
                conversation_id=self.conversation_id,
                speaker="system",
                message=f"{event_type}: {json.dumps(event_data, default=str)}",
                metadata={"type": "workflow_event", "event_type": event_type}
            )
        
        # Log to the persistent, tamper-evident project chronolog
        if self.session_id:
            try:
                log_project_event(
                    project_path=str(self.project_path),
                    event_type=event_type.upper(), # Chronolog expects uppercase event types
                    session_id=self.session_id,
                    data=event_data
                )
            except Exception as e:
                print(f"⚠️ Chronolog logging failed for event {event_type}: {e}") 