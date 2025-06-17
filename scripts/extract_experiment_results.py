#!/usr/bin/env python3
"""
Extract and parse experiment results from the database.
Integrates with existing StatisticalLogger and framework systems.
"""

import os
import sys
from pathlib import Path
import logging
import pandas as pd
from typing import Dict, List, Tuple, Optional

# Add project root to Python path for src imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.narrative_gravity.utils.statistical_logger import StatisticalLogger
from src.narrative_gravity.utils.database import get_database_url
from src.narrative_gravity.framework_manager import FrameworkManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExperimentResultsExtractor:
    def __init__(self):
        """Initialize the extractor using existing StatisticalLogger and FrameworkManager."""
        self.logger = StatisticalLogger()
        self.framework_manager = FrameworkManager()
        
    def extract_experiment_results(self, experiment_id: str) -> pd.DataFrame:
        """
        Extract experiment results using StatisticalLogger.
        
        Args:
            experiment_id: Unique identifier for the experiment
            
        Returns:
            DataFrame containing experiment results
        """
        try:
            # Use StatisticalLogger to get runs data frame
            df = self.logger._get_runs_dataframe(include_raw_responses=True)
            
            # Filter for specific experiment
            if experiment_id:
                df = df[df['experiment_id'] == experiment_id]
            
            if df.empty:
                logger.warning(f"No results found for experiment {experiment_id}")
                return pd.DataFrame()
            
            # Get framework information for validation
            frameworks = df['framework'].unique()
            for framework_name in frameworks:
                try:
                    framework = self.framework_manager.load_framework(framework_name)
                    logger.info(f"Validated framework: {framework.name} v{framework.version}")
                except Exception as e:
                    logger.warning(f"Could not validate framework {framework_name}: {e}")
            
            # Dynamic column validation based on actual data
            required_columns = [
                'run_id', 'text_id', 'framework', 'llm_model'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                logger.warning(f"Missing columns in results: {missing_columns}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error extracting experiment results: {str(e)}")
            raise

    def validate_data_completeness(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate data completeness and quality.
        
        Args:
            df: DataFrame containing experiment results
            
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        if df.empty:
            issues.append("No data found")
            return False, issues
        
        # Check for required columns
        required_columns = [
            'run_id', 'text_id', 'framework', 'llm_model'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            issues.append(f"Missing required columns: {missing_columns}")
        
        # Check for null values in critical columns
        critical_columns = ['text_id', 'framework']
        for col in critical_columns:
            if col in df.columns and df[col].isnull().any():
                issues.append(f"Null values found in {col}")
        
        # Validate well scores if present
        if 'raw_scores' in df.columns:
            for idx, scores in df['raw_scores'].items():
                if pd.isna(scores):
                    continue
                    
                if not isinstance(scores, dict):
                    issues.append(f"Invalid well scores format at index {idx}")
                    continue
                
                for well, score in scores.items():
                    if not isinstance(score, (int, float)):
                        issues.append(f"Invalid score type for {well} at index {idx}")
                    elif score < 0 or score > 1:
                        issues.append(f"Score out of range for {well} at index {idx}")
        
        return len(issues) == 0, issues

    def export_to_csv(self, df: pd.DataFrame, output_path: str):
        """
        Export results to CSV file.
        
        Args:
            df: DataFrame to export
            output_path: Path to save CSV file
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Export to CSV
            df.to_csv(output_path, index=False)
            logger.info(f"Exported results to {output_path}")
            
        except Exception as e:
            logger.error(f"Error exporting results: {str(e)}")
            raise

def main():
    """Main execution function."""
    try:
        # Initialize extractor
        extractor = ExperimentResultsExtractor()
        
        # Get available experiments from StatisticalLogger
        experiment_id = None  # Extract all experiments by default
        results_df = extractor.extract_experiment_results(experiment_id)
        
        if results_df.empty:
            logger.warning("No experimental data found in database")
            return
        
        # Show available experiments
        if 'experiment_id' in results_df.columns:
            experiments = results_df['experiment_id'].unique()
            logger.info(f"Found experiments: {list(experiments)}")
        
        # Validate data
        is_valid, issues = extractor.validate_data_completeness(results_df)
        if not is_valid:
            logger.warning("Data validation issues found:")
            for issue in issues:
                logger.warning(f"- {issue}")
        
        # Export results
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"exports/analysis_results/extracted_results_{timestamp}.csv"
        extractor.export_to_csv(results_df, output_path)
        
        logger.info(f"Extraction complete. {len(results_df)} records exported.")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 