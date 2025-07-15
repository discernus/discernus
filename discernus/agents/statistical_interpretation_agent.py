#!/usr/bin/env python3
"""
Statistical Interpretation Agent
================================

THIN Principle: This agent translates the sterile, quantitative output from the
SecureCodeExecutor into a human-readable, qualitative interpretation suitable
for an academic publication. It bridges the gap between numbers and meaning.
"""

import sys
from pathlib import Path
import json
from typing import Dict, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.gateway.llm_gateway import LLMGateway
    from discernus.gateway.model_registry import ModelRegistry
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"StatisticalInterpretationAgent dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class StatisticalInterpretationAgent:
    """
    Takes raw statistical results and interprets them in the context of the main analysis report.
    """

    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Could not import required dependencies for StatisticalInterpretationAgent")
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)

    def interpret_statistical_results(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> str:
        """
        Reads statistical results and generates a human-readable interpretation.
        The agent finds its own data in the workflow_state.
        """
        project_path = Path(workflow_state.get('project_path', '.'))
        stats_file_path = workflow_state.get('stats_file_path')

        if not stats_file_path:
            return "Error: `stats_file_path` not found in workflow_state."

        stats_path = Path(stats_file_path)
        
        # For context, we'll use the experiment.md file from the project path.
        context_content = ""
        context_source = ""
        context_path = project_path / "experiment.md"
        if context_path.exists():
            context_source = f"Experiment Definition ({context_path.name})"
            context_content = context_path.read_text()

        if not stats_path.exists():
            return "Error: Statistical results file not found."
        
        try:
            stats_data = json.loads(stats_path.read_text())
        except Exception as e:
            return f"Error reading input files: {e}"

        return self._call_interpretation_llm(stats_data, context_content, context_source)

    def _call_interpretation_llm(self, stats_data: Dict[str, Any], context_content: str, context_source: str) -> str:
        """Calls an LLM to generate the interpretation."""
        prompt = f"""
You are an expert in computational social science methodology and statistics, specializing in explaining complex quantitative results to a non-expert academic audience.

Your task is to write a new "Statistical Analysis" section for a research paper. You will be given the raw JSON output from a statistical analysis and contextual information from the project. You must synthesize these sources to provide a clear, concise, and meaningful interpretation of the statistical findings.

**Contextual Information ({context_source}):**
---
{context_content}
---

**Raw Statistical Results (JSON):**
---
{json.dumps(stats_data, indent=2)}
---

**Your Task:**
Write a markdown-formatted "Statistical Analysis" section that:
1.  **Starts with a `## Statistical Analysis` header.**
2.  Clearly explains the purpose and outcome of each statistical test (e.g., "Inter-run reliability was assessed using Cronbach's Alpha...").
3.  Interprets the results in plain English (e.g., "A score of 0.85 indicates high reliability between analysis runs.").
4.  Connects the statistical findings back to the main research questions and hypotheses in the provided context.
5.  Is written in a clear, academic tone suitable for publication.

**Do NOT simply repeat the JSON data. Your value is in the interpretation and synthesis.**

Begin the new section now:
"""
        
        # Use a powerful model for this nuanced interpretation task.
        model_name = self.model_registry.get_model_for_task('synthesis')
        if not model_name:
            # Fallback to a powerful default if no suitable model is found in the registry
            print("⚠️ No suitable synthesis model found in registry, using claude-3.5-sonnet as fallback.")
            model_name = 'anthropic/claude-3.5-sonnet'

        try:
            interpretation, _ = self.gateway.execute_call(model=model_name, prompt=prompt)
            return interpretation if interpretation else "The interpretation model returned an empty response."
        except Exception as e:
            return f"Error calling LLM for interpretation: {e}" 