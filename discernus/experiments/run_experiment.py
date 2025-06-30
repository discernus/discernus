#!/usr/bin/env python3
"""
Simple Experiment Runner for Discernus Reboot
=============================================

Executes experiments based on YAML configuration files without requiring
manual curl commands or ad-hoc parameter construction.

Usage:
    python3 run_experiment.py experiment_config.yaml

Examples:
    python3 run_experiment.py flagship_model_statistical_comparison.yaml
    python3 run_experiment.py reboot_mft_experiment.yaml
"""

import sys
import asyncio
import yaml
import json
import aiohttp
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ExperimentRunner:
    """
    Clean experiment execution based on YAML configuration.
    
    Implements the architectural decision to move from implicit curl commands
    to explicit YAML-driven experiment execution.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        # Set longer timeout for corpus-based experiments that can take 20+ minutes
        timeout = aiohttp.ClientTimeout(total=30*60)  # 30 minutes
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def execute_experiment(self, yaml_path: str) -> Dict[str, Any]:
        """
        Execute experiment based on YAML configuration.
        
        Args:
            yaml_path: Path to experiment YAML file
            
        Returns:
            Experiment results dictionary
        """
        # Load experiment definition
        experiment_def = self._load_experiment_definition(yaml_path)
        
        # Determine experiment type and route accordingly
        experiment_meta = experiment_def.get('experiment_meta', {})
        study_design = experiment_meta.get('study_design', {})
        comparison_type = study_design.get('comparison_type')
        
        logger.info(f"🚀 Starting experiment: {experiment_meta.get('display_name', 'Unknown')}")
        logger.info(f"📊 Comparison type: {comparison_type}")
        
        if comparison_type == 'multi_model':
            return await self._execute_multi_model_comparison(experiment_def, yaml_path)
        else:
            raise ValueError(f"Unsupported comparison type: {comparison_type}")
    
    def _load_experiment_definition(self, yaml_path: str) -> Dict[str, Any]:
        """Load and validate experiment definition from YAML file"""
        yaml_file = Path(yaml_path)
        
        if not yaml_file.exists():
            # Try relative to experiments directory
            experiments_dir = Path(__file__).parent
            yaml_file = experiments_dir / yaml_path
            
        if not yaml_file.exists():
            raise FileNotFoundError(f"Experiment file not found: {yaml_path}")
        
        logger.info(f"📋 Loading experiment: {yaml_file}")
        
        with open(yaml_file, 'r') as f:
            experiment_def = yaml.safe_load(f)
            
        # Basic validation
        required_sections = ['experiment_meta', 'models']
        for section in required_sections:
            if section not in experiment_def:
                raise ValueError(f"Missing required section in experiment YAML: {section}")
        
        return experiment_def
    
    async def _execute_multi_model_comparison(self, experiment_def: Dict[str, Any], yaml_path: str) -> Dict[str, Any]:
        """Execute multi-model statistical comparison"""
        
        # Extract configuration
        models_config = experiment_def.get('models', {})
        corpus_config = experiment_def.get('corpus')
        statistical_config = experiment_def.get('statistical_analysis', {})
        
        # Resolve the YAML file path (same logic as _load_experiment_definition)
        yaml_file = Path(yaml_path)
        if not yaml_file.exists():
            experiments_dir = Path(__file__).parent
            yaml_file = experiments_dir / yaml_path
        
        # Build request payload with resolved path
        request_payload = {
            "comparison_type": "multi_model",
            "experiment_file_path": str(yaml_file.resolve()),
            "statistical_methods": self._extract_statistical_methods(statistical_config)
        }
        
        # Add models if specified
        enabled_models = self._extract_enabled_models(models_config)
        if enabled_models:
            request_payload["models"] = enabled_models
            
        logger.info(f"🔬 Models to compare: {', '.join(enabled_models)}")
        logger.info(f"📈 Statistical methods: {', '.join(request_payload['statistical_methods'])}")
        
        if corpus_config:
            total_texts = self._estimate_corpus_size(corpus_config)
            total_analyses = len(enabled_models) * total_texts
            logger.info(f"📚 Corpus-based analysis: ~{total_texts} texts × {len(enabled_models)} models = {total_analyses} analyses")
        
        # Execute experiment
        logger.info("⚡ Sending request to statistical comparison API...")
        
        async with self.session.post(
            f"{self.base_url}/compare-statistical",
            json=request_payload,
            headers={"Content-Type": "application/json"}
        ) as response:
            
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(f"API request failed ({response.status}): {error_text}")
            
            result = await response.json()
            
        logger.info(f"✅ Experiment complete! Job ID: {result.get('job_id', 'unknown')}")
        
        # Display results summary
        self._display_results_summary(result, experiment_def)
        
        return result
    
    def _extract_statistical_methods(self, statistical_config: Dict[str, Any]) -> list:
        """Extract enabled statistical methods from configuration"""
        # STRATEGIC DECISION: Defer all statistical analysis to Stage 6 notebooks
        # Statistical configuration is preserved in YAML for experimental context
        # but not executed during runtime for better research workflow flexibility
        return []
    
    def _extract_enabled_models(self, models_config: Dict[str, Any]) -> list:
        """Extract enabled models from configuration"""
        flagship_models = models_config.get('flagship_models', {})
        enabled_models = []
        
        for model_key, model_info in flagship_models.items():
            if model_info.get('enabled', True):  # Default to enabled
                enabled_models.append(model_info['model_id'])
        
        return enabled_models
    
    def _estimate_corpus_size(self, corpus_config: Dict[str, Any]) -> int:
        """Estimate number of texts in corpus"""
        file_path = corpus_config.get('file_path')
        pattern = corpus_config.get('pattern', '**/*.txt')
        
        if not file_path:
            return 0
            
        corpus_path = Path(file_path)
        if not corpus_path.exists():
            return 0
            
        text_files = list(corpus_path.glob(pattern))
        return len(text_files)
    
    def _display_results_summary(self, result: Dict[str, Any], experiment_def: Dict[str, Any]):
        """Display a summary of experiment results"""
        print("\n" + "="*60)
        print("📊 EXPERIMENT RESULTS SUMMARY")
        print("="*60)
        
        # Basic info
        job_id = result.get('job_id', 'unknown')
        comparison_type = result.get('comparison_type', 'unknown')
        classification = result.get('similarity_classification', 'unknown')
        
        print(f"Job ID: {job_id}")
        print(f"Comparison Type: {comparison_type}")
        print(f"Similarity Classification: {classification}")
        
        # Model results
        condition_results = result.get('condition_results', [])
        if condition_results:
            print(f"\n🤖 MODEL RESULTS ({len(condition_results)} models):")
            for condition in condition_results:
                model = condition.get('condition_identifier', 'unknown')
                centroid = condition.get('centroid', (0, 0))
                print(f"  • {model}: centroid ({centroid[0]:.3f}, {centroid[1]:.3f})")
        
        # Statistical metrics
        statistical_metrics = result.get('statistical_metrics', {})
        if statistical_metrics:
            print(f"\n📈 STATISTICAL ANALYSIS:")
            
            # Geometric similarity
            geometric = statistical_metrics.get('geometric_similarity', {})
            if geometric:
                mean_distance = geometric.get('mean_distance', 0)
                print(f"  • Mean Distance: {mean_distance:.4f}")
            
            # Correlation
            correlation = statistical_metrics.get('dimensional_correlation', {})
            if correlation:
                correlation_matrix = correlation.get('correlation_matrix', [])
                if correlation_matrix and len(correlation_matrix) > 1:
                    # Calculate average correlation (excluding diagonal)
                    correlations = []
                    for i in range(len(correlation_matrix)):
                        for j in range(len(correlation_matrix[i])):
                            if i != j:
                                correlations.append(correlation_matrix[i][j])
                    if correlations:
                        avg_correlation = sum(correlations) / len(correlations)
                        print(f"  • Average Correlation: {avg_correlation:.4f}")
        
        # Report URL
        report_url = result.get('report_url')
        if report_url:
            print(f"\n📋 DETAILED REPORT:")
            print(f"  View results: http://localhost:8000{report_url}")
        
        print("="*60)


def main():
    """Main entry point for experiment runner"""
    if len(sys.argv) != 2:
        print("Usage: python3 run_experiment.py <experiment_yaml_file>")
        print("\nExamples:")
        print("  python3 run_experiment.py flagship_model_statistical_comparison.yaml")
        print("  python3 run_experiment.py reboot_mft_experiment.yaml")
        sys.exit(1)
    
    yaml_path = sys.argv[1]
    
    async def run_experiment():
        async with ExperimentRunner() as runner:
            try:
                start_time = datetime.now()
                result = await runner.execute_experiment(yaml_path)
                end_time = datetime.now()
                duration = end_time - start_time
                
                print(f"\n⏱️  Total execution time: {duration}")
                
                # STAGE 5→6 HANDOFF: Auto-generate analysis notebook
                try:
                    from discernus.stage6.handoff_orchestrator import trigger_stage6_handoff
                    
                    print("\n🔄 Generating Stage 6 analysis notebook...")
                    experiment_def = runner._load_experiment_definition(yaml_path)
                    notebook_path = trigger_stage6_handoff(result, yaml_path, experiment_def)
                    
                    print(f"✅ Stage 6 notebook generated: {notebook_path}")
                    print(f"🚀 Ready for interactive analysis: jupyter lab {notebook_path}")
                    
                except Exception as e:
                    logger.warning(f"⚠️  Stage 6 handoff failed: {e}")
                    print(f"⚠️  Notebook generation failed, but experiment completed successfully")
                
                return result
                
            except Exception as e:
                logger.error(f"❌ Experiment failed: {e}")
                raise
    
    # Run the experiment
    try:
        asyncio.run(run_experiment())
        print("\n🎉 Experiment completed successfully!")
    except KeyboardInterrupt:
        print("\n⏹️  Experiment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Experiment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 