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

    def generate_final_audit(self, project_path: str, report_file_path: str, stats_file_path: str) -> str:
        """
        Reads all experiment artifacts and generates a final methodological audit.
        """
        project_path_obj = Path(project_path)
        
        # Gather all artifacts
        try:
            experiment_md = (project_path_obj / "experiment.md").read_text()
            framework_md = (project_path_obj / "framework.md").read_text()
            final_report = Path(report_file_path).read_text()
            stats_json = json.loads(Path(stats_file_path).read_text())
            # Read the last 100 lines of the chronolog to keep context manageable
            chronolog_entries = self._read_last_n_lines_of_chronolog(project_path_obj, 100)

        except FileNotFoundError as e:
            return f"## Methodological Audit\n\n**Error:** Could not perform final audit. Missing required file: {e.filename}"
        except Exception as e:
            return f"## Methodological Audit\n\n**Error:** Could not perform final audit. Failed to read artifact files: {e}"

        return self._call_audit_llm(experiment_md, framework_md, final_report, stats_json, chronolog_entries)

    def _read_last_n_lines_of_chronolog(self, project_path: Path, n: int) -> List[Dict]:
        """Reads the last N JSONL entries from the project chronolog."""
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
        prompt = f"""
You are the Chief Methodologist and lead peer reviewer for a computational social science project. Your task is to conduct a final, holistic audit of the entire research process and write a concluding "Methodological Audit" section for the final report.

You have been given all the project artifacts. Your job is to look for incoherencies, potential issues, and limitations that a human researcher might miss.

**1. Original Experiment Plan (`experiment.md`):**
---
{experiment_md}
---

**2. Analytical Framework (`framework.md`):**
---
{framework_md}
---

**3. Final Report (including qualitative synthesis and statistical interpretation):**
---
{final_report}
---

**4. Raw Statistical Results (`statistical_analysis_results.json`):**
---
{json.dumps(stats_json, indent=2)}
---

**5. Recent Process Log (`project_chronolog.jsonl` excerpt):**
---
{json.dumps(chronolog_entries, indent=2)}
---

**Your Task:**
Write a new markdown-formatted "## Methodological Audit" section. In this section, critically assess the project's execution against its original goals. Consider the following questions:

-   **Goal Alignment:** Does the final report's conclusion directly address the research questions from the original `experiment.md`? Were the hypotheses from the experiment adequately tested by the statistical analysis?
-   **Result Coherence:** Are there any apparent discrepancies between the raw statistical results and the human-readable interpretation written in the final report? Does the qualitative synthesis seem to gloss over any outliers or surprising findings present in the data?
-   **Process Integrity:** Based on the process log, were there any system errors, model fallbacks, or other unexpected events that could have influenced the results? (For example, if a less-capable model was used as a fallback, this could be a limitation).
-   **Limitations & Alternative Interpretations:** What are the primary limitations of this study, based on all available information? Are there any alternative interpretations of the findings that the main report did not consider?

Your tone should be constructive and critical, like a good peer reviewer. Your goal is to increase the final report's credibility by transparently acknowledging its potential weaknesses.

Begin the new section now:
"""
        
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