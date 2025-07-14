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
from discernus.core.conversation_logger import ConversationLogger

# Dynamically import all agent classes for runtime instantiation
from discernus.agents.statistical_interpretation_agent import StatisticalInterpretationAgent
from discernus.agents.experiment_conclusion_agent import ExperimentConclusionAgent
from discernus.agents.methodological_overwatch_agent import MethodologicalOverwatchAgent

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
        self.gateway = LLMGateway(self.model_registry)
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

    async def execute_workflow(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Primary execution method for running a defined workflow.
        """
        self._init_session_logging()
        self._log_system_event("WORKFLOW_EXECUTION_STARTED", {"session_id": self.session_id})

        try:
            experiment_config = self._parse_experiment_config()
            workflow_steps = experiment_config.get('workflow')

            if not workflow_steps:
                raise ValueError("No 'workflow' definition found in experiment.md configuration.")

            # Prime the initial state
            self.workflow_state = initial_state
            self.workflow_state['project_path'] = str(self.project_path)
            self.workflow_state['session_results_path'] = str(self.session_results_path)

            for i, step_config in enumerate(workflow_steps):
                agent_name = step_config.get('agent')
                if not agent_name:
                    raise ValueError(f"Workflow step {i} is missing the 'agent' key.")
                
                self._log_system_event("WORKFLOW_STEP_STARTED", {"step": i + 1, "agent": agent_name})
                
                step_output = await self._execute_step(agent_name, step_config)
                
                # Update the master workflow state with the output
                if step_output:
                    self.workflow_state.update(step_output)

                self._log_system_event("WORKFLOW_STEP_COMPLETED", {"step": i + 1, "agent": agent_name, "output_keys": list(step_output.keys())})

            await self._save_final_artifacts()
            self._log_system_event("WORKFLOW_EXECUTION_COMPLETED", {"session_id": self.session_id})
            
            return {"status": "success", "session_id": self.session_id, "results_path": str(self.session_results_path)}

        except Exception as e:
            self._log_system_event("WORKFLOW_EXECUTION_ERROR", {"error": str(e)})
            raise e

    async def _execute_step(self, agent_name: str, step_config: Dict[str, Any]) -> Dict[str, Any]:
        """Dynamically loads and executes a single agent step."""
        agent_def = self.agent_registry.get(agent_name)
        if not agent_def:
            raise ValueError(f"Agent '{agent_name}' not found in the registry.")

        # Special handling for the first 'AnalysisAgent' step
        if agent_name == "AnalysisAgent":
            analysis_results = await self._run_parallel_analysis()
            return {'analysis_results': analysis_results}

        # For all other agents, use the dynamic loading mechanism
        agent_instance = self._create_agent_instance(agent_def)
        execution_method = getattr(agent_instance, agent_def['execution_method'])
        
        method_args = self._prepare_method_args(agent_def, step_config)

        if asyncio.iscoroutinefunction(execution_method):
            result = await execution_method(**method_args)
        else:
            result = execution_method(**method_args)
        
        output_keys = [list(o.keys())[0] for o in agent_def.get('outputs', [])]
        return {output_keys[0]: result}
    
    def _create_agent_instance(self, agent_def: Dict[str, Any]) -> Any:
        """Dynamically creates an instance of an agent class."""
        module_path = agent_def['module']
        class_name = agent_def['class']
        
        module = importlib.import_module(module_path)
        agent_class = getattr(module, class_name)
        return agent_class()

    def _prepare_method_args(self, agent_def: Dict[str, Any], step_config: Dict[str, Any]) -> Dict[str, Any]:
        """Prepares arguments for the agent's execution method from the workflow state."""
        method_args = {}
        for input_def in agent_def.get('inputs', []):
            for key, desc in input_def.items():
                if key in self.workflow_state:
                    method_args[key] = self.workflow_state[key]
        
        # Override with any specific params for this step
        method_args.update(step_config.get('params', {}))
        return method_args
    
    async def _run_parallel_analysis(self) -> List[Dict[str, Any]]:
        """Handles the special case of spawning multiple analysis agents in parallel."""
        # This logic is extracted and simplified from the old orchestrator
        experiment_config = self._parse_experiment_config()
        corpus_files = self.workflow_state.get('corpus_files', [])
        analysis_instructions = self.workflow_state.get('analysis_agent_instructions', '')
        models = experiment_config.get('models', [])
        num_runs = experiment_config.get('num_runs', 1)

        tasks = []
        for run in range(num_runs):
            for model_name in models:
                for corpus_file in corpus_files:
                    # In a real implementation, this would call a separate AnalysisAgent runner
                    # For now, we simulate this call.
                    pass # This part needs a dedicated runner function similar to the old orchestrator
        
        print("INFO: Skipping parallel analysis execution for this refactoring step.")
        # This would normally return a list of result dicts
        return self.workflow_state.get('analysis_results', []) # Return existing results if they exist for now

    def _parse_experiment_config(self) -> Dict[str, Any]:
        """Parses the YAML config block from the experiment.md file."""
        experiment_file = self.project_path / "experiment.md"
        if not experiment_file.exists():
            return {}
        try:
            content = experiment_file.read_text()
            match = re.search(r'```yaml\n(.*?)```', content, re.DOTALL)
            if match:
                return yaml.safe_load(match.group(1))
        except Exception as e:
            print(f"Warning: Could not parse experiment YAML. Error: {e}")
        return {}

    async def _save_final_artifacts(self):
        """Saves all final artifacts to the session results directory."""
        # Save the final human-readable report
        if 'final_report_content' in self.workflow_state:
            report_path = self.session_results_path / "final_report.md"
            report_path.write_text(self.workflow_state['final_report_content'])

        # Save the entire final workflow state for debugging and provenance
        state_path = self.session_results_path / "final_workflow_state.json"
        # Convert Path objects to strings for JSON serialization
        serializable_state = {k: str(v) if isinstance(v, Path) else v for k, v in self.workflow_state.items()}
        state_path.write_text(json.dumps(serializable_state, indent=2, default=str))

        # Save session metadata
        metadata = {
            "session_id": self.session_id,
            "timestamp": self.session_results_path.name,
            "project_path": str(self.project_path)
        }
        (self.session_results_path / "session_metadata.json").write_text(json.dumps(metadata, indent=2))
        
    def _init_session_logging(self):
        """Initializes logging for the current session."""
        timestamp = datetime.now()
        self.session_id = f"session_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        self.conversation_id = f"conversation_{timestamp.strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
        
        self.logger = ConversationLogger(str(self.project_path))
        
        timestamp_str = timestamp.strftime('%Y-%m-%d_%H-%M-%S')
        self.session_results_path = self.results_path / timestamp_str
        self.session_results_path.mkdir(exist_ok=True)

    def _log_system_event(self, event_type: str, event_data: Dict[str, Any]):
        """Logs a system event."""
        if self.logger:
            self.logger.log_llm_message(
                conversation_id=self.conversation_id,
                speaker="system",
                message=f"{event_type}: {json.dumps(event_data, default=str)}",
                metadata={"type": "workflow_event", "event_type": event_type}
            ) 