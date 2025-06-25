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
# This will be handled by the main application's entry point
# project_root = Path(__file__).parent.parent
# sys.path.insert(0, str(project_root))

from ..utils.statistical_logger import StatisticalLogger
from ..utils.database import get_database_url
from ..framework_manager import FrameworkManager

# Add production database imports
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from ..models.models import Experiment, Run
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
        
    def _get_framework_wells(self, framework_name: str) -> List[str]:
        """Get the list of wells defined for a specific framework."""
        try:
            import yaml
            
            # First try YAML frameworks (modern approach)
            framework_path = self._get_framework_yaml_path(framework_name)
            if framework_path:
                with open(framework_path, 'r', encoding='utf-8') as f:
                    framework_data = yaml.safe_load(f)
                
                # Extract wells from axes (v3.1+) or dipoles (legacy)
                wells = []
                
                # Try new axes format first (v3.1+) - label-agnostic extraction
                axes = framework_data.get('axes', {})
                if axes:
                    for axis_name, axis_data in axes.items():
                        if isinstance(axis_data, dict):
                            # Extract all anchors from this axis regardless of organizational labels
                            for label, anchor_config in axis_data.items():
                                if isinstance(anchor_config, dict) and 'name' in anchor_config:
                                    wells.append(anchor_config['name'])
                    logger.info(f"✅ Loaded {len(wells)} wells for {framework_name} from YAML (v3.1 axes, label-agnostic): {wells}")
                else:
                    # Fall back to legacy dipoles format
                    dipoles = framework_data.get('dipoles', [])
                    for dipole in dipoles:
                        if isinstance(dipole, dict):
                            if 'positive' in dipole and 'name' in dipole['positive']:
                                wells.append(dipole['positive']['name'])
                            if 'negative' in dipole and 'name' in dipole['negative']:
                                wells.append(dipole['negative']['name'])
                    logger.info(f"✅ Loaded {len(wells)} wells for {framework_name} from YAML (legacy dipoles): {wells}")
                
                return wells
            
            # Fallback to old JSON format for legacy frameworks
            framework_path = Path("frameworks") / framework_name / "framework_consolidated.json"
            
            if framework_path.exists():
                with open(framework_path, 'r') as f:
                    framework_data = json.load(f)
                
                # Extract wells from dipoles
                wells = []
                dipoles = framework_data.get('dipoles', [])
                for dipole in dipoles:
                    if isinstance(dipole, dict):
                        if 'positive' in dipole and 'name' in dipole['positive']:
                            wells.append(dipole['positive']['name'])
                        if 'negative' in dipole and 'name' in dipole['negative']:
                            wells.append(dipole['negative']['name'])
                
                logger.info(f"✅ Loaded {len(wells)} wells for {framework_name} (JSON): {wells}")
                return wells
            
            # Last resort: old dipoles format
            framework_dir = Path("frameworks") / framework_name
            dipoles_file = framework_dir / "dipoles.json"
            
            if dipoles_file.exists():
                with open(dipoles_file, 'r') as f:
                    dipoles_data = json.load(f)
                
                wells = []
                dipoles = dipoles_data.get('dipoles', [])
                for dipole in dipoles:
                    if isinstance(dipole, dict):
                        if 'positive' in dipole and 'name' in dipole['positive']:
                            wells.append(dipole['positive']['name'])
                        if 'negative' in dipole and 'name' in dipole['negative']:
                            wells.append(dipole['negative']['name'])
                
                logger.info(f"✅ Loaded {len(wells)} wells for {framework_name} (legacy): {wells}")
                return wells
            
            logger.warning(f"Framework {framework_name} has no configuration files in any format")
            return []
            
        except Exception as e:
            logger.warning(f"Could not load framework {framework_name}: {e}")
            return []
    
    def _get_framework_yaml_path(self, framework_name: str) -> Optional[str]:
        """
        Map framework name to its YAML file path.
        """
        # Normalize framework name
        framework_name = framework_name.replace('_', '').lower()
        
        # Framework name mappings
        framework_mappings = {
            'moralfoundationstheory': 'moral_foundations_theory',
            'mft': 'moral_foundations_theory',
            'moralfoundations': 'moral_foundations_theory',
            'civicvirtue': 'civic_virtue',
            'iditi': 'iditi'
        }
        
        # Get canonical framework name
        canonical_name = framework_mappings.get(framework_name, framework_name)
        
        # Search paths in order of preference
        search_paths = [
            # Research workspace (primary)
            f"research_workspaces/june_2025_research_dev_workspace/frameworks/{canonical_name}/{canonical_name}_framework.yaml",
            f"research_workspaces/june_2025_research_dev_workspace/frameworks/{canonical_name}/framework.yaml",
            # Main frameworks directory (fallback)  
            f"frameworks/{canonical_name}/framework.yaml",
            f"frameworks/{canonical_name}/{canonical_name}_framework.yaml",
        ]
        
        for path in search_paths:
            # This needs to be adjusted to look relative to project root, not current file
            project_root = Path().resolve() # A bit of a hack
            if (project_root / path).exists():
                return str(project_root / path)
        
        return None

    def extract_results(self, execution_results: Dict) -> Dict:
        """
        Extract and structure experiment results for enhanced analysis.
        
        Args:
            execution_results: Raw experiment execution results
            
        Returns:
            Dictionary containing structured data and metadata
        """
        logger.info("📊 Processing execution results for enhanced analysis...")
        
        try:
            results_list = execution_results.get('results', [])
            total_analyses = len(results_list)
            successful_analyses = len([r for r in results_list if r.get('success', False)])
            
            logger.info(f"📊 Processing {total_analyses} analyses...")
            
            structured_data = []
            
            for i, result in enumerate(results_list):
                try:
                    # Extract well scores
                    well_scores = result.get('well_scores', {})
                    if not well_scores and 'raw_scores' in result:
                        well_scores = result['raw_scores']
                    
                    # Get framework-specific wells
                    framework_name = result.get('framework', 'unknown')
                    framework_wells = self._get_framework_wells(framework_name)
                    
                    # Create structured record
                    record = {
                        'analysis_id': result.get('analysis_id', f'analysis_{i}'),
                        'text_id': result.get('text_id', f'text_{i}'),
                        'framework': framework_name,
                        'model': result.get('llm_model', 'unknown'),
                        'success': result.get('success', True),
                        'api_cost': result.get('api_cost', 0.0),
                        'duration_seconds': result.get('duration_seconds', 0.0),
                        'quality_score': result.get('framework_fit_score', 0.0),
                        'narrative_position_x': result.get('narrative_position_x', 0.0),
                        'narrative_position_y': result.get('narrative_position_y', 0.0),
                        'timestamp': result.get('timestamp', pd.Timestamp.now().isoformat())
                    }
                    
                    # Add well scores ONLY for wells defined in the framework
                    if framework_wells:
                        for well_name in framework_wells:
                            # Look for the well score in various formats
                            score = None
                            if well_name in well_scores:
                                score = well_scores[well_name]
                            elif well_name.lower() in well_scores:
                                score = well_scores[well_name.lower()]
                            elif well_name.title() in well_scores:
                                score = well_scores[well_name.title()]
                            
                            if score is not None:
                                clean_well_name = well_name.lower().replace(' ', '_').replace('-', '_')
                                record[f'well_{clean_well_name}'] = score
                    else:
                        # Fallback: if no framework wells defined, extract all
                        logger.warning(f"No framework wells defined for {framework_name}, extracting all scores")
                        for well_name, score in well_scores.items():
                            clean_well_name = well_name.lower().replace(' ', '_').replace('-', '_')
                            record[f'well_{clean_well_name}'] = score
                    
                    structured_data.append(record)
                    
                except Exception as e:
                    logger.warning(f"Could not process result {i}: {e}")
                    continue
            
            # Convert to DataFrame
            df = pd.DataFrame(structured_data)
            
            # Get framework-aware well columns
            well_columns = [col for col in df.columns if col.startswith('well_')]
            
            # Create metadata summary
            metadata = {
                'total_analyses': total_analyses,
                'successful_analyses': successful_analyses,
                'failed_analyses': total_analyses - successful_analyses,
                'total_cost': execution_results.get('total_cost', 0.0),
                'cost_efficiency': execution_results.get('cost_efficiency', 0.0),
                'extraction_timestamp': pd.Timestamp.now().isoformat(),
                'well_columns': well_columns,
                'frameworks_used': df['framework'].unique().tolist() if 'framework' in df.columns else [],
                'models_used': df['model'].unique().tolist() if 'model' in df.columns else []
            }
            
            logger.info(f"✅ Structured {len(df)} records with {len(metadata['well_columns'])} framework-defined wells")
            
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