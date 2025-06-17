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
import json

# Add project root to Python path for src imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.narrative_gravity.utils.statistical_logger import StatisticalLogger
from src.narrative_gravity.utils.database import get_database_url
from src.narrative_gravity.framework_manager import FrameworkManager

# Add production database imports
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from src.narrative_gravity.models.models import Experiment, Run
    DATABASE_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Production database imports not available: {e}")
    DATABASE_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExperimentResultsExtractor:
    def __init__(self):
        """Initialize the extractor using both StatisticalLogger and production database."""
        self.logger = StatisticalLogger()
        self.framework_manager = FrameworkManager()
        
        # Initialize production database connection
        if DATABASE_AVAILABLE:
            try:
                self.engine = create_engine(get_database_url())
                self.Session = sessionmaker(bind=self.engine)
                self.production_db_available = True
                logger.info("✅ Production database connection established")
            except Exception as e:
                logger.warning(f"Production database not available: {e}")
                self.production_db_available = False
        else:
            self.production_db_available = False
        
    def extract_results(self, execution_results: Dict) -> Dict:
        """
        Extract and structure experiment results for enhanced analysis pipeline.
        
        Args:
            execution_results: Dictionary containing execution summary from orchestrator
            
        Returns:
            Dictionary containing structured results for statistical analysis
        """
        try:
            # Extract experiment metadata from execution results
            total_analyses = execution_results.get('total_analyses', 0)
            successful_analyses = execution_results.get('successful_analyses', 0)
            results_list = execution_results.get('results', [])
            
            logger.info(f"📊 Processing {len(results_list)} results for enhanced analysis")
            
            if not results_list:
                logger.warning("No results to process")
                return {'structured_data': pd.DataFrame(), 'metadata': {}}
            
            # Convert results list to structured data
            structured_data = []
            
            for i, result in enumerate(results_list):
                try:
                    # Extract well scores
                    well_scores = result.get('well_scores', {})
                    if not well_scores and 'raw_scores' in result:
                        well_scores = result['raw_scores']
                    
                    # Create structured record
                    record = {
                        'analysis_id': result.get('analysis_id', f'analysis_{i}'),
                        'text_id': result.get('text_id', f'text_{i}'),
                        'framework': result.get('framework', 'unknown'),
                        'model': result.get('llm_model', 'unknown'),
                        'success': result.get('success', True),
                        'api_cost': result.get('api_cost', 0.0),
                        'duration_seconds': result.get('duration_seconds', 0.0),
                        'quality_score': result.get('framework_fit_score', 0.0),
                        'narrative_position_x': result.get('narrative_position_x', 0.0),
                        'narrative_position_y': result.get('narrative_position_y', 0.0),
                        'timestamp': result.get('timestamp', pd.Timestamp.now().isoformat())
                    }
                    
                    # Add well scores as separate columns
                    for well_name, score in well_scores.items():
                        # Clean well name for column usage
                        clean_well_name = well_name.lower().replace(' ', '_').replace('-', '_')
                        record[f'well_{clean_well_name}'] = score
                    
                    structured_data.append(record)
                    
                except Exception as e:
                    logger.warning(f"Could not process result {i}: {e}")
                    continue
            
            # Convert to DataFrame
            df = pd.DataFrame(structured_data)
            
            # Create metadata summary
            metadata = {
                'total_analyses': total_analyses,
                'successful_analyses': successful_analyses,
                'failed_analyses': total_analyses - successful_analyses,
                'total_cost': execution_results.get('total_cost', 0.0),
                'cost_efficiency': execution_results.get('cost_efficiency', 0.0),
                'extraction_timestamp': pd.Timestamp.now().isoformat(),
                'well_columns': [col for col in df.columns if col.startswith('well_')],
                'frameworks_used': df['framework'].unique().tolist() if 'framework' in df.columns else [],
                'models_used': df['model'].unique().tolist() if 'model' in df.columns else []
            }
            
            logger.info(f"✅ Structured {len(df)} records with {len(metadata['well_columns'])} wells")
            
            return {
                'structured_data': df,
                'metadata': metadata,
                'raw_execution_results': execution_results
            }
            
        except Exception as e:
            logger.error(f"Error in extract_results: {str(e)}")
            raise

    def extract_experiment_results_by_name(self, experiment_name: str) -> pd.DataFrame:
        """
        Extract experiment results by experiment name from production database.
        
        Args:
            experiment_name: Name of the experiment (e.g., "IDITI_Framework_Validation_Study")
            
        Returns:
            DataFrame containing experiment results
        """
        if not self.production_db_available:
            logger.error("Production database not available")
            return pd.DataFrame()
        
        session = self.Session()
        try:
            # Find experiment by name
            experiment = session.query(Experiment).filter(
                Experiment.name == experiment_name
            ).first()
            
            if not experiment:
                logger.warning(f"No experiment found with name: {experiment_name}")
                return pd.DataFrame()
            
            logger.info(f"Found experiment: {experiment.name} (ID: {experiment.id})")
            
            # Get all runs for this experiment
            runs = session.query(Run).filter(
                Run.experiment_id == experiment.id
            ).all()
            
            if not runs:
                logger.warning(f"No runs found for experiment: {experiment_name}")
                return pd.DataFrame()
            
            logger.info(f"Found {len(runs)} runs for experiment")
            
            # Convert runs to structured data
            structured_data = []
            
            for run in runs:
                try:
                    # Parse raw_scores if it's a JSON string
                    if isinstance(run.raw_scores, str):
                        raw_scores = json.loads(run.raw_scores)
                    else:
                        raw_scores = run.raw_scores or {}
                    
                    # Create structured record
                    record = {
                        'run_id': run.id,
                        'experiment_id': run.experiment_id,
                        'run_number': run.run_number,
                        'text_id': run.text_id,
                        'framework': experiment.framework_config_id,
                        'model_name': run.llm_model,
                        'success': run.success,
                        'api_cost': run.api_cost or 0.0,
                        'duration_seconds': run.duration_seconds or 0.0,
                        'framework_fit_score': run.framework_fit_score or 0.0,
                        'narrative_x': run.narrative_position_x or 0.0,
                        'narrative_y': run.narrative_position_y or 0.0,
                        'narrative_elevation': run.narrative_elevation or 0.0,
                        'polarity': run.polarity or 0.0,
                        'coherence': run.coherence or 0.0,
                        'directional_purity': run.directional_purity or 0.0,
                        'timestamp': run.execution_time.isoformat() if run.execution_time else pd.Timestamp.now().isoformat(),
                        'text_content': run.text_content,
                        'input_length': run.input_length
                    }
                    
                    # Add well scores as separate columns
                    for well_name, score in raw_scores.items():
                        # Clean well name for column usage
                        clean_well_name = well_name.lower().replace(' ', '_').replace('-', '_')
                        record[f'well_{clean_well_name}'] = score
                    
                    structured_data.append(record)
                    
                except Exception as e:
                    logger.warning(f"Could not process run {run.id}: {e}")
                    continue
            
            # Convert to DataFrame
            df = pd.DataFrame(structured_data)
            
            logger.info(f"✅ Extracted {len(df)} records from production database")
            
            return df
            
        except Exception as e:
            logger.error(f"Error extracting experiment results: {str(e)}")
            raise
        finally:
            session.close()
        
    def extract_experiment_results(self, experiment_id: str) -> pd.DataFrame:
        """
        Extract experiment results using StatisticalLogger (legacy method).
        
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
            'run_id', 'text_id', 'framework', 'model_name'
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
        well_columns = [col for col in df.columns if col.startswith('well_')]
        if well_columns:
            for col in well_columns:
                invalid_scores = df[col].apply(lambda x: not isinstance(x, (int, float)) or x < 0 or x > 1)
                if invalid_scores.any():
                    issues.append(f"Invalid scores found in {col}")
        
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
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract experiment results from database")
    parser.add_argument('--experiment-name', type=str, help='Name of experiment to extract')
    parser.add_argument('--experiment-id', type=str, help='ID of experiment to extract (legacy)')
    
    args = parser.parse_args()
    
    try:
        # Initialize extractor
        extractor = ExperimentResultsExtractor()
        
        # Extract experiment results
        if args.experiment_name:
            logger.info(f"Extracting results for experiment: {args.experiment_name}")
            results_df = extractor.extract_experiment_results_by_name(args.experiment_name)
        elif args.experiment_id:
            logger.info(f"Extracting results for experiment ID: {args.experiment_id}")
            results_df = extractor.extract_experiment_results(args.experiment_id)
        else:
            # Try to extract IDITI experiment by default
            logger.info("No experiment specified, trying IDITI_Framework_Validation_Study")
            results_df = extractor.extract_experiment_results_by_name("IDITI_Framework_Validation_Study")
        
        if results_df.empty:
            logger.warning("No experimental data found in database")
            return
        
        # Show summary
        logger.info(f"Found {len(results_df)} runs in experiment")
        if 'framework' in results_df.columns:
            frameworks = results_df['framework'].unique()
            logger.info(f"Frameworks: {list(frameworks)}")
        if 'model_name' in results_df.columns:
            models = results_df['model_name'].unique()
            logger.info(f"Models: {list(models)}")
        
        # Show well columns
        well_columns = [col for col in results_df.columns if col.startswith('well_')]
        logger.info(f"Well columns found: {well_columns}")
        
        # Validate data
        is_valid, issues = extractor.validate_data_completeness(results_df)
        if not is_valid:
            logger.warning("Data validation issues found:")
            for issue in issues:
                logger.warning(f"- {issue}")
        else:
            logger.info("✅ Data validation passed")
        
        # Export results
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        experiment_name = args.experiment_name or args.experiment_id or "unknown_experiment"
        output_path = f"exports/analysis_results/extracted_results_{experiment_name}_{timestamp}.csv"
        extractor.export_to_csv(results_df, output_path)
        
        logger.info(f"✅ Extraction complete. {len(results_df)} records exported to {output_path}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 