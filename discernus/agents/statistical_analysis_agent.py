#!/usr/bin/env python3
"""
Statistical Analysis Agent
==========================

THIN Principle: This agent performs statistical calculations on structured
data produced by other agents. It uses robust, well-vetted libraries for its
calculations and produces machine-readable output. It does not contain
natural language processing or interpretation logic.

REFACTORED: Now uses the hybrid intelligence pattern.
1. An LLM designs a Python script to extract scores from natural language.
2. The SecureCodeExecutor runs the script to get structured data.
3. Standard statistical libraries perform calculations on the structured data.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import pandas as pd
import re

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.core.secure_code_executor import SecureCodeExecutor
from discernus.gateway.model_registry import ModelRegistry

class StatisticalAnalysisAgent:
    """
    Performs statistical analysis on a set of analysis results.
    """

    def __init__(self):
        """Initializes the agent."""
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)
        self.code_executor = SecureCodeExecutor()

    def calculate_statistics(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates statistics from analysis results and saves them to a file.
        The agent finds its own data in the workflow_state.
        """
        analysis_results = workflow_state.get('analysis_results', [])
        session_results_path = workflow_state.get('session_results_path')

        if not session_results_path:
            raise ValueError("`session_results_path` not found in workflow_state.")

        results_path = Path(session_results_path)
        if not results_path.exists():
            results_path.mkdir(parents=True, exist_ok=True)

        # --- Data Preparation (Hybrid Intelligence Pattern) ---
        
        # 1. LLM Designs a Scoring Script
        scoring_script_design = self._design_scoring_script(analysis_results)
        
        # 2. Secure Code Executor runs the script
        execution_globals = {'analysis_results': analysis_results}
        all_scores = self.code_executor.execute_code(scoring_script_design, execution_globals)

        if not isinstance(all_scores, list):
            raise TypeError(f"Scoring script was expected to return a list, but returned {type(all_scores)}")

        # Filter out None values that may have been appended
        all_scores = [s for s in all_scores if isinstance(s, (int, float))]

        # --- Basic Statistical Summary ---
        statistical_summary = {
            'num_observations': len(all_scores),
            'mean_score': np.mean(all_scores) if all_scores else 0,
            'std_dev': np.std(all_scores) if all_scores else 0,
            'min_score': min(all_scores) if all_scores else 0,
            'max_score': max(all_scores) if all_scores else 0,
            'cronbachs_alpha': self._calculate_cronbachs_alpha(analysis_results, all_scores)
        }
        
        # --- Save Results ---
        stats_file_path = results_path / "statistical_analysis_results.json"
        with open(stats_file_path, 'w') as f:
            json.dump(statistical_summary, f, indent=2)

        return {'stats_file_path': str(stats_file_path)}

    def _design_scoring_script(self, analysis_results: List[Dict[str, Any]]) -> str:
        """
        Uses an LLM to design a Python script that extracts scores from
        natural language analysis responses.
        """
        model_name = self.model_registry.get_model_for_task('code_generation')
        if not model_name:
            model_name = "anthropic/claude-3-haiku-20240307"

        sample_responses = [res['analysis_response'] for res in analysis_results[:2]]

        prompt = f"""
You are a Python expert specializing in data extraction.
Your task is to write a Python script that extracts a numerical score from a list of natural language analysis reports.

The script will have access to a global variable named `analysis_results`, which is a list of dictionaries. Each dictionary has a key 'analysis_response' containing the natural language text.

Here is a sample of the analysis responses:
---
SAMPLE 1:
{sample_responses[0] if len(sample_responses) > 0 else "No sample available."}
---
SAMPLE 2:
{sample_responses[1] if len(sample_responses) > 1 else "No sample available."}
---

Write a Python script that:
1. Iterates through the `analysis_results` list.
2. For each `analysis_response`, uses regular expressions or other string manipulation to find and extract the primary numerical score. The score might be labeled as 'Tone Score', 'Main Idea Score', or just be a number.
3. Appends each extracted score as a float to a new list called `extracted_scores`.
4. If no score can be found, it should append `None`.
5. At the end, the script must return the `extracted_scores` list directly.

**IMPORTANT**: The final line of your script must be `extracted_scores` and nothing else.

Provide ONLY the Python code inside a single ```python ... ``` block. Do not include any explanation or surrounding text.
The script should be ready to be executed by a secure code executor.
"""
        
        response, _ = self.gateway.execute_call(model_name, prompt)
        
        code_match = re.search(r'```python\n(.*?)```', response, re.DOTALL)
        if not code_match:
            raise ValueError("LLM did not return a Python code block for scoring.")
            
        return code_match.group(1)

    def _calculate_cronbachs_alpha(self, analysis_results: List[Dict[str, Any]], all_scores: List[Any]) -> float:
        """
        Calculates Cronbach's Alpha. This is a placeholder and needs a more
        robust implementation based on structured data.
        """
        if len(analysis_results) != len(all_scores):
             return -1.0 # Error condition

        data = []
        for i, res in enumerate(analysis_results):
            data.append({
                'item': res.get('file_name'),
                'rater': res.get('run_num', 1),
                'score': all_scores[i]
            })

        if not data:
            return 0.0

        df = pd.DataFrame(data)

        if 'rater' not in df.columns or df['rater'].nunique() < 2:
            return -1.0 # Not computable

        pivot_df = df.pivot(index='item', columns='rater', values='score').dropna()
        
        if pivot_df.shape[0] < 2:
            return -2.0

        k = pivot_df.shape[1]
        item_variances = pivot_df.var(axis=1, ddof=1)
        total_variance = pivot_df.sum(axis=0).var(ddof=1)
        
        if total_variance == 0:
            return 1.0

        alpha = (k / (k - 1)) * (1 - item_variances.sum() / total_variance)
        return alpha 