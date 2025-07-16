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
from discernus.core.project_chronolog import get_project_chronolog, log_project_event

# Dynamically import all agent classes for runtime instantiation
from discernus.agents.analysis_agent import AnalysisAgent
from discernus.agents.statistical_analysis_agent import StatisticalAnalysisAgent
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
            workflow_steps = initial_state.get('workflow')

            if not workflow_steps:
                raise ValueError("No 'workflow' definition found in the initial state.")

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

        # For all agents, use the dynamic loading mechanism
        # Special case: if the agent is this orchestrator itself, use self instead of creating new instance
        if agent_def.get('class') == 'WorkflowOrchestrator':
            agent_instance = self
        else:
            agent_instance = self._create_agent_instance(agent_def)
        execution_method = getattr(agent_instance, agent_def['execution_method'])
        
        # The new pattern: pass the whole state and the step config to the agent.
        # The agent is responsible for pulling what it needs.
        if asyncio.iscoroutinefunction(execution_method):
            result = await execution_method(self.workflow_state, step_config)
        else:
            result = execution_method(self.workflow_state, step_config)

        # CRITICAL: Ensure the output is always a dictionary that can be used
        # to update the workflow state. The agent's declared output key from the
        # registry is used as the key in the state dictionary.
        output_def = agent_def.get('outputs', [])
        if not output_def:
            return {} # Agent has no declared outputs, return empty dict.

        output_key = list(output_def[0].keys())[0]
        
        # If the agent already returned a dictionary with the correct key, use it directly.
        if isinstance(result, dict) and output_key in result:
             return result

        # Otherwise, wrap the raw result in the expected output dictionary.
        return {output_key: result}
    
    async def _call_llm_async(self, prompt: str, agent_id: str, model_name: str) -> str:
        """Helper to call LLM with logging."""
        self._log_system_event("LLM_CALL_STARTED", {"agent_id": agent_id, "model_name": model_name})
        
        content, metadata = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.gateway.execute_call(model=model_name, prompt=prompt)
        )
        
        if not metadata.get("success"):
            error_msg = f"LLM call failed for {agent_id}: {metadata.get('error')}"
            self._log_system_event("LLM_CALL_FAILED", {"agent_id": agent_id, "error": error_msg})
            raise Exception(error_msg)
            
        self._log_system_event("LLM_CALL_COMPLETED", {"agent_id": agent_id})
        return content

    async def _run_single_analysis(self, agent_id: str, corpus_file: str, instructions: str, model_name: str, run_num: int) -> Dict[str, Any]:
        """Runs a single analysis agent on one corpus text."""
        self._log_system_event("ANALYSIS_AGENT_SPAWNED", {"agent_id": agent_id, "corpus_file": Path(corpus_file).name})
        
        corpus_text = Path(corpus_file).read_text()
        
        analysis_prompt = f"""You are {agent_id}, a framework analysis specialist.

ANALYSIS INSTRUCTIONS:
{instructions}

TEXT TO ANALYZE:
File: {Path(corpus_file).name}
Content:
{corpus_text}

TASK: Apply the framework systematically to this text. Provide a thorough analysis with specific evidence and clear reasoning for your assessments.
"""
        response = await self._call_llm_async(analysis_prompt, agent_id, model_name)
        
        # --- Enhanced Debugging ---
        self._log_system_event("ANALYSIS_AGENT_RAW_RESPONSE", {"agent_id": agent_id, "raw_response": response})

        # THIN Principle: Just pass the analysis text through, don't try to parse it
        # If structured data is needed, a separate agent should extract it
        return {
            "agent_id": agent_id,
            "corpus_file": corpus_file,
            "file_name": Path(corpus_file).name,
            "model_name": model_name,
            "run_num": run_num,
            "analysis_response": response,  # Pass through as text - let other agents parse if needed
        }

    def _create_agent_instance(self, agent_def: Dict[str, Any]) -> Any:
        """Dynamically creates an instance of an agent class."""
        module_path = agent_def['module']
        class_name = agent_def['class']
        
        module = importlib.import_module(module_path)
        agent_class = getattr(module, class_name)
        return agent_class()

    async def _run_analysis_agent(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Executes a pre-computed analysis plan from the ExecutionPlannerAgent.
        This method iterates through the schedule, respects delays, and runs analysis in batches.
        """
        schedule = workflow_state.get('execution_plan', [])
        num_runs = workflow_state.get('num_runs', 1)

        if not schedule:
            raise ValueError("Execution plan is empty or missing. Cannot proceed.")

        all_results: List[Any] = []
        for i, step in enumerate(schedule):
            self._log_system_event("EXECUTING_PLAN_STEP", {
                "step": i + 1, "total_steps": len(schedule), "model": step.get('model'),
                "batch_size": len(step.get('file_batch', [])), "delay": step.get('delay_after_seconds', 0)
            })

            # Create a list of analysis tasks for the current batch, for each run
            batch_tasks = []
            for run_num in range(1, num_runs + 1):
                for corpus_filename in step.get('file_batch', []):
                    # Construct the full path to the corpus file
                    corpus_file_path = self.project_path / "corpus" / corpus_filename
                    
                    # We need a unique agent_id for each task
                    agent_id = f"analysis_agent_{step.get('model', 'model').replace('/', '_')}_{Path(corpus_filename).stem}_run{run_num}"
                    task = self._run_single_analysis(
                        agent_id=agent_id,
                        corpus_file=str(corpus_file_path),
                        instructions=workflow_state.get('analysis_agent_instructions', ''),
                        model_name=step.get('model', ''),
                        run_num=run_num
                    )
                    batch_tasks.append(task)
            
            # Execute the batch in parallel
            if batch_tasks:
                batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
                all_results.extend(batch_results)

            # Honor the calculated delay to respect rate limits
            if step.get('delay_after_seconds', 0) > 0:
                await asyncio.sleep(step['delay_after_seconds'])

        # Process results
        successful_results: List[Dict[str, Any]] = []
        for res in all_results:
            if isinstance(res, Exception):
                self._log_system_event("ANALYSIS_AGENT_ERROR", {"error": str(res)})
            elif isinstance(res, dict):
                successful_results.append(res)
                
        print(f"INFO: Analysis complete. {len(successful_results)} successful, {len(all_results) - len(successful_results)} failed.")
        return successful_results

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
        
        # --- Restore Critical Chronolog Functionality ---
        if self.session_id:
            try:
                chronolog = get_project_chronolog(str(self.project_path))
                
                chronolog_result = chronolog.create_run_chronolog(
                    session_id=self.session_id,
                    results_directory=str(self.session_results_path)
                )
                
                if chronolog_result.get('created', False):
                    run_log_path = chronolog_result['run_chronolog_file']
                    print(f"📝 Run chronolog created: {run_log_path}")
                    
                    # Merge the run log into the main project chronolog
                    print(f"Merging run log into master project chronolog...")
                    chronolog.merge_run_log(run_log_path)
                    
            except Exception as e:
                print(f"⚠️ Failed to create or merge run chronolog: {e}")
        else:
            print("⚠️ No session_id available, skipping run chronolog creation")

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