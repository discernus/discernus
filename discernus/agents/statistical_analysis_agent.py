#!/usr/bin/env python3
"""
Statistical Analysis Agent
==========================

THIN Principle: This agent performs statistical calculations on structured
data produced by other agents. It uses robust, well-vetted libraries for its
calculations and produces machine-readable output.
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
        """
        analysis_results = workflow_state.get('analysis_results', [])
        session_results_path = workflow_state.get('session_results_path')

        if not session_results_path:
            raise ValueError("`session_results_path` not found in workflow_state.")
        
        statistical_plan = workflow_state.get('statistical_plan', {})
        required_tests = statistical_plan.get('required_tests', [])

        results_path = Path(session_results_path)
        results_path.mkdir(parents=True, exist_ok=True)

        # New multi-anchor data structure
        # Reorganize results for multi-anchor analysis
        anchor_data = {}
        for result in analysis_results:
            scores = result.get('all_scores', {})
            for anchor, score in scores.items():
                if anchor not in anchor_data:
                    anchor_data[anchor] = []
                anchor_data[anchor].append({
                    "score": score,
                    "file_name": result.get("file_name"),
                    "run_num": result.get("run_num")
                })
        
        # --- Perform analysis for each anchor ---
        final_statistics = {}
        for anchor, results in anchor_data.items():
            all_scores = [res.get('score') for res in results if res.get('score') is not None]

            # --- Basic Statistical Summary (always included) ---
            statistical_summary = {
                'num_observations': len(all_scores),
                'mean_score': np.mean(all_scores) if all_scores else 0,
                'std_dev': np.std(all_scores) if all_scores else 0,
                'min_score': min(all_scores) if all_scores else 0,
                'max_score': max(all_scores) if all_scores else 0,
            }

            # --- Execute tests from the statistical plan ---
            for test in required_tests:
                test_name = test.get('test_name')
                if test_name == 'cronbach_alpha':
                    # Pass the filtered results for the current anchor to the calculation
                    statistical_summary['cronbachs_alpha'] = self._calculate_cronbachs_alpha(results)
            
            final_statistics[anchor] = statistical_summary

        # --- Save Results ---
        stats_file_path = results_path / "statistical_analysis_results.json"
        with open(stats_file_path, 'w') as f:
            json.dump(final_statistics, f, indent=2)

        return {'stats_file_path': str(stats_file_path)}

    def _calculate_cronbachs_alpha(self, analysis_results: List[Dict[str, Any]]) -> float:
        """
        Calculates Cronbach's Alpha for inter-run reliability.
        """
        data = []
        for res in analysis_results:
            score = res.get('score')
            if score is not None:
                data.append({
                    'item': res.get('file_name'),
                    'rater': res.get('run_num', 1),
                    'score': score
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