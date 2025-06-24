import logging
from typing import Dict, Any, List
import pandas as pd

from .icc import calculate_icc
from .cronbach import calculate_cronbach_alpha
from .descriptive import (
    calculate_pairwise_correlations,
    calculate_coefficient_of_variation,
    detect_outliers,
    analyze_systematic_bias,
    calculate_descriptive_reliability_stats,
    calculate_internal_consistency,
    generate_reliability_summary,
)

logger = logging.getLogger(__name__)


class InterraterReliabilityAnalyzer:
    """Thin wrapper that composes reliability utilities."""

    def __init__(self) -> None:
        self.reliability_results: Dict[str, Any] = {}

    def analyze_reliability(self, structured_results: Dict) -> Dict[str, Any]:
        logger.info("🔍 Starting interrater reliability analysis...")
        df: pd.DataFrame = structured_results.get('structured_data')
        metadata = structured_results.get('metadata', {})
        if df is None or df.empty:
            logger.error("No structured data available for reliability analysis")
            return {'error': 'No data available'}

        well_columns = [c for c in df.columns if c.startswith('well_')]
        if not well_columns:
            logger.error("No well score columns found in data")
            return {'error': 'No well scores found'}

        models = df['model'].unique() if 'model' in df.columns else []
        if len(models) < 2:
            logger.warning(
                f"Only {len(models)} model(s) found - reliability analysis requires multiple raters"
            )
            return self._single_rater_analysis(df, well_columns, metadata)

        logger.info(
            f"🎯 Analyzing reliability with {len(models)} models and {len(well_columns)} wells"
        )

        reliability_results = {
            'metadata': {
                'models_analyzed': list(models),
                'well_count': len(well_columns),
                'sample_size': len(df),
                'analysis_timestamp': pd.Timestamp.now().isoformat(),
            },
            'icc_analysis': calculate_icc(df, well_columns),
            'cronbach_alpha': calculate_cronbach_alpha(df, well_columns),
            'pairwise_correlations': calculate_pairwise_correlations(df, well_columns, models),
            'coefficient_of_variation': calculate_coefficient_of_variation(df, well_columns),
            'outlier_analysis': detect_outliers(df, well_columns),
            'systematic_bias_analysis': analyze_systematic_bias(df, well_columns, models),
            'reliability_summary': {},
        }
        reliability_results['reliability_summary'] = generate_reliability_summary(reliability_results)
        logger.info("✅ Interrater reliability analysis completed")
        return reliability_results

    def _single_rater_analysis(self, df: pd.DataFrame, well_columns: List[str], metadata: Dict) -> Dict[str, Any]:
        logger.info("📊 Performing single-rater descriptive analysis...")
        return {
            'analysis_type': 'single_rater_descriptive',
            'metadata': {
                'model_count': 1,
                'well_count': len(well_columns),
                'sample_size': len(df),
                'analysis_timestamp': pd.Timestamp.now().isoformat(),
            },
            'descriptive_statistics': calculate_descriptive_reliability_stats(df, well_columns),
            'internal_consistency': calculate_internal_consistency(df, well_columns),
            'message': 'Single rater detected - full reliability analysis requires multiple raters',
        }
