#!/usr/bin/env python3
"""
CSV Statistical Results Writer for the Discernus Platform.

Handles the deterministic generation of statistical_results.csv files.
"""

import csv
import os
import logging
from typing import Dict, Any

from ..agent import ExportOptions

logger = logging.getLogger(__name__)


def generate_statistical_results_csv(
    statistical_results: Dict[str, Any],
    export_path: str,
    export_options: ExportOptions,
) -> str:
    """Generate statistical_results.csv with ANOVA, correlations, t-tests, etc."""
    filename = "statistical_results.csv"
    filepath = os.path.join(export_path, filename)

    # Extract statistical test results from the nested structure
    # Handle both direct results and nested synthesis results
    results = {}

    if 'results' in statistical_results:
        results = statistical_results['results']
    elif 'stage_2_derived_metrics' in statistical_results:
        # Handle synthesis pipeline format
        stage_2_results = statistical_results['stage_2_derived_metrics'].get('results', {})
        results = stage_2_results
    elif statistical_results and any(statistical_results.values()):
        # Handle direct statistical results format
        results = statistical_results
    else:
        raise ValueError(f"No statistical results data provided to CSV export. "
                       f"Received: {statistical_results}")

    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow([
            'test_name', 'test_type', 'statistic_name', 'statistic_value',
            'p_value', 'effect_size', 'degrees_of_freedom', 'sample_size',
            'dependent_variable', 'grouping_variable', 'significance_level',
            'interpretation', 'notes'
        ])

        # Process each statistical test result
        for test_name, test_data in results.items():
            if isinstance(test_data, dict):
                test_type = test_data.get('type', 'unknown')

                if test_type == 'one_way_anova':
                    # ANOVA results
                    writer.writerow([
                        test_name, test_type, 'F_statistic',
                        test_data.get('f_statistic', ''), test_data.get('p_value', ''),
                        test_data.get('effect_size', ''), test_data.get('degrees_of_freedom', ''),
                        test_data.get('sample_size', ''), test_data.get('dependent_variable', ''),
                        test_data.get('grouping_variable', ''),
                        'p < 0.05' if test_data.get('p_value', 1.0) < 0.05 else 'p >= 0.05',
                        test_data.get('interpretation', ''), test_data.get('notes', '')
                    ])

                elif test_type == 'correlation' or 'correlation' in test_type:
                    # Correlation results
                    corr_matrix = test_data.get('correlation_matrix', {})
                    for var1, correlations in corr_matrix.items():
                        if isinstance(correlations, dict):
                            for var2, corr_value in correlations.items():
                                if var1 != var2:  # Skip self-correlations
                                    writer.writerow([
                                        f"{test_name}_{var1}_{var2}", test_type, 'correlation_coefficient',
                                        corr_value, '', '', '', '',
                                        f"{var1} vs {var2}", '',
                                        'significant' if abs(float(corr_value)) > 0.5 else 'not_significant',
                                        f"Correlation between {var1} and {var2}", ''
                                    ])

                elif test_type == 't_test':
                    # T-test results
                    writer.writerow([
                        test_name, test_type, 't_statistic',
                        test_data.get('t_statistic', ''), test_data.get('p_value', ''),
                        test_data.get('effect_size', ''), test_data.get('degrees_of_freedom', ''),
                        test_data.get('sample_size', ''), test_data.get('dependent_variable', ''),
                        test_data.get('grouping_variable', ''),
                        'p < 0.05' if test_data.get('p_value', 1.0) < 0.05 else 'p >= 0.05',
                        test_data.get('interpretation', ''), test_data.get('notes', '')
                    ])

                else:
                    # Generic statistical result
                    writer.writerow([
                        test_name, test_type, 'result_value',
                        str(test_data), '', '', '', '', '', '', '',
                        f"Generic {test_type} result", ''
                    ])

    logger.info(f"Generated statistical_results.csv with {len(results)} test results")
    return filename
