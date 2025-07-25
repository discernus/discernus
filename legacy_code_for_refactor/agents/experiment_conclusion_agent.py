#!/usr/bin/env python3
"""
Experiment Conclusion Agent
===========================

THIN Principle: This agent acts as a final, automated peer reviewer. It consumes
the *entire* context of a completed experiment—from initial plans to final
statistical results and logs—to produce a holistic methodological audit. It embodies
the principle of applying maximum intelligence to the full context to reduce
researcher burden.
"""

import sys
from pathlib import Path
import json
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.gateway.llm_gateway import LLMGateway
    from discernus.gateway.model_registry import ModelRegistry
    from discernus.core.agent_roles import get_expert_prompt
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"ExperimentConclusionAgent dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class ExperimentConclusionAgent:
    """
    Performs a final, holistic audit of a completed experiment.
    """

    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Could not import required dependencies for ExperimentConclusionAgent")
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)
        self.role = "methodological_auditor"

    def generate_final_audit(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> str:
        """
        Reads all experiment artifacts and generates a final methodological audit.
        The agent is responsible for finding its own data in the workflow_state
        using the keys provided in the step_config.
        """
        params = step_config.get('params', {})
        project_path = Path(workflow_state.get('project_path', '.'))
        
        # Use params to find the content/paths in the workflow state
        report_content = workflow_state.get(params.get('report_content_key', '')) or ""
        critique_content = workflow_state.get(params.get('critique_key', ''))
        stats_file_path = workflow_state.get('stats_file_path')

        # Fallback to reading from files if content isn't directly in the state
        if not report_content and 'report_file_path' in workflow_state:
            report_content = Path(workflow_state['report_file_path']).read_text()

        if not stats_file_path:
            return "## Methodological Audit\n\n**Error:** Could not perform final audit. `stats_file_path` not found in workflow state."

        # Gather all artifacts
        try:
            experiment_md = (project_path / "experiment.md").read_text()
            framework_md = (project_path / "framework.md").read_text()
            stats_json = json.loads(Path(stats_file_path).read_text())
            chronolog_entries = self._read_last_n_lines_of_chronolog(project_path, 100)

        except FileNotFoundError as e:
            return f"## Methodological Audit\n\n**Error:** Could not perform final audit. Missing required file: {e.filename}"
        except Exception as e:
            return f"## Methodological Audit\n\n**Error:** Could not perform final audit. Failed to read artifact files: {e}"

        # Combine the report and critique for the LLM call
        final_report_context = report_content
        if critique_content:
            final_report_context += "\n\n--- CRITIQUE FOR REVISION ---\n" + str(critique_content)

        return self._call_audit_llm(experiment_md, framework_md, final_report_context, stats_json, chronolog_entries)

    def _read_last_n_lines_of_chronolog(self, project_path: Path, n: int) -> List[Dict]:
        """Reads the last N JSONL entries from the main project chronolog."""
        # Correctly point to the main project chronolog at the project root
        chronolog_path = project_path / "project_chronolog.jsonl"
        
        if not chronolog_path.exists():
            return []
        
        try:
            with open(chronolog_path, 'r') as f:
                lines = f.readlines()
            
            last_n_lines = lines[-n:]
            entries = [json.loads(line) for line in last_n_lines if line.strip()]
            return entries
        except Exception:
            return [] # Return empty if any error occurs

    def _call_audit_llm(self, experiment_md: str, framework_md: str, final_report: str, stats_json: Dict, chronolog_entries: List) -> str:
        """Calls a top-tier LLM to perform the final audit."""
        prompt = get_expert_prompt(
            self.role,
            experiment_md=experiment_md,
            framework_md=framework_md,
            final_report=final_report,
            stats_json=json.dumps(stats_json, indent=2),
            chronolog_entries=json.dumps(chronolog_entries, indent=2)
        )
        
        # Use a top-tier model for this highly complex synthesis and audit task.
        model_name = self.model_registry.get_model_for_task('synthesis')
        if not model_name:
            # Fallback to a known powerful model if the registry lookup fails
            model_name = "anthropic/claude-3.5-sonnet"

        try:
            audit_text, _ = self.gateway.execute_call(model=model_name, prompt=prompt)
            return audit_text if audit_text else "## Methodological Audit\n\nThe audit model returned an empty response."
        except Exception as e:
            return f"## Methodological Audit\n\n**Error:** The final audit could not be completed due to an error calling the LLM: {e}" 