#!/usr/bin/env python3
"""
Statistical Analysis Agent
==========================

THIN Principle: This agent performs statistical calculations on structured
data produced by other agents. It uses robust, well-vetted libraries for its
calculations and produces machine-readable output. It does not contain
natural language processing or interpretation logic.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.core.llm_response_parser import LLMResponseParser

class StatisticalAnalysisAgent:
    """
    Performs statistical analysis on a set of analysis results.
    """

    def __init__(self):
        """Initializes the agent."""
        pass

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

        # --- Data Preparation ---
        # The analysis_results contain JSON strings in the 'analysis_response' field.
        # We need to parse these to extract the scores.
        all_scores = []
        for result in analysis_results:
            analysis_response = result.get('analysis_response', '')
            score = LLMResponseParser.extract_score_from_analysis(analysis_response)
            
            if score is not None:
                all_scores.append(score)
            else:
                print(f"Warning: Could not extract score from analysis_response: {analysis_response[:100]}...")
                continue
        
        # Filter out None values that may have been appended
        all_scores = [s for s in all_scores if s is not None]

        # --- Cronbach's Alpha Calculation ---
        # Note: This is a simplified calculation. A real implementation would need
        # to handle the data structure (items vs. raters) more robustly.
        # Here we treat each run as a "rater" and each speech as an "item".
        # This requires reshaping the data.
        
        # For this placeholder, we'll assume a simple list of scores and calculate variance.
        # A full implementation requires more structure.
        
        statistical_summary = {
            'num_observations': len(all_scores),
            'mean_score': np.mean(all_scores) if all_scores else 0,
            'std_dev': np.std(all_scores) if all_scores else 0,
            'min_score': min(all_scores) if all_scores else 0,
            'max_score': max(all_scores) if all_scores else 0,
            'cronbachs_alpha': self._calculate_cronbachs_alpha(analysis_results)
        }
        
        # --- Save Results ---
        stats_file_path = results_path / "statistical_analysis_results.json"
        with open(stats_file_path, 'w') as f:
            json.dump(statistical_summary, f, indent=2)

        return {'stats_file_path': str(stats_file_path)}

    def _calculate_cronbachs_alpha(self, analysis_results: List[Dict[str, Any]]) -> float:
        """
        Calculates Cronbach's Alpha for inter-run reliability.
        
        Assumes `analysis_results` is structured with identifiable runs and items.
        """
        # Data needs to be in a matrix of items x raters (or corpus_file x run_num)
        
        # 1. Create a DataFrame
        data = []
        for res in analysis_results:
            analysis_response = res.get('analysis_response', '')
            score = LLMResponseParser.extract_score_from_analysis(analysis_response)
            
            if score is not None:
                data.append({
                    'item': res.get('file_name'),
                    'rater': res.get('run_num'), # This assumes run_num is available
                    'score': score
                })
            else:
                continue
        
        if not data:
            return 0.0

        df = pd.DataFrame(data)

        # The planner in the orchestrator doesn't currently support multiple runs,
        # so we will likely only have one "rater". Cronbach's alpha requires > 1.
        # For now, we return a placeholder if we don't have enough data.
        if 'rater' not in df.columns or df['rater'].nunique() < 2:
            return -1.0 # Indicate not computable

        # 2. Pivot to get items x raters matrix
        pivot_df = df.pivot(index='item', columns='rater', values='score')
        
        # 3. Calculate Cronbach's Alpha
        # Drop items with missing ratings
        pivot_df = pivot_df.dropna()
        
        if pivot_df.shape[0] < 2:
            return -2.0 # Not enough items to calculate variance

        k = pivot_df.shape[1]  # Number of raters
        item_variances = pivot_df.var(axis=1, ddof=1)
        total_variance = pivot_df.sum(axis=0).var(ddof=1)
        
        if total_variance == 0:
            return 1.0 # Perfect agreement, no variance in totals

        alpha = (k / (k - 1)) * (1 - item_variances.sum() / total_variance)
        return alpha 