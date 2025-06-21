#!/usr/bin/env python3
"""
IDITI Experiment Results Analysis - Python Implementation
Analyzes yesterday's IDITI experimental data using native Python statistical capabilities.
Integrates with existing visualization engine and generates comprehensive reports.
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json
import logging
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import seaborn as sns
import matplotlib.pyplot as plt

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.narrative_gravity.utils.statistical_logger import StatisticalLogger
from src.narrative_gravity.visualization.engine import NarrativeGravityVisualizationEngine
from src.narrative_gravity.framework_manager import FrameworkManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class IDITIAnalysisEngine:
    """Python-based analysis engine for IDITI experimental results."""
    
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.data = None
        self.well_columns = []
        self.analysis_results = {}
        
        # Initialize existing system components
        self.stat_logger = StatisticalLogger()
        self.viz_engine = NarrativeGravityVisualizationEngine()
        self.framework_manager = FrameworkManager()
        
    def load_and_prepare_data(self) -> pd.DataFrame:
        """Load and prepare the experimental data for analysis."""
        logger.info(f"Loading data from {self.data_file}")
        
        try:
            self.data = pd.read_csv(self.data_file)
            logger.info(f"✅ Loaded {len(self.data)} records with {len(self.data.columns)} variables")
            
            # Identify well columns
            self.well_columns = [col for col in self.data.columns if col.startswith('well_')]
            logger.info(f"Found {len(self.well_columns)} narrative wells: {self.well_columns}")
            
            # Basic data cleaning
            self.data['cost'] = pd.to_numeric(self.data['cost'], errors='coerce')
            self.data['duration_seconds'] = pd.to_numeric(self.data['duration_seconds'], errors='coerce')
            
            # Convert timestamp
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
            
            return self.data
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def calculate_reliability_metrics(self) -> Dict:
        """Calculate reliability metrics using Python statistical functions."""
        logger.info("🔍 Calculating reliability metrics...")
        
        reliability_results = {
            'framework_reliability': {},
            'model_reliability': {},
            'well_reliability': {},
            'overall_metrics': {}
        }
        
        # Well score reliability analysis
        if self.well_columns:
            well_data = self.data[self.well_columns].dropna()
            
            if len(well_data) > 0:
                # Calculate coefficient of variation for each well
                well_stats = {}
                for well in self.well_columns:
                    scores = self.data[well].dropna()
                    if len(scores) > 1:
                        mean_score = scores.mean()
                        std_score = scores.std()
                        cv = std_score / mean_score if mean_score != 0 else np.inf
                        
                        well_stats[well] = {
                            'mean': mean_score,
                            'std': std_score,
                            'cv': cv,
                            'min': scores.min(),
                            'max': scores.max(),
                            'count': len(scores),
                            'reliability_score': 1 - min(cv, 1.0)  # Higher is better
                        }
                
                reliability_results['well_reliability'] = well_stats
                
                # Overall reliability metrics
                cv_values = [stats['cv'] for stats in well_stats.values() if not np.isinf(stats['cv'])]
                if cv_values:
                    reliability_results['overall_metrics'] = {
                        'mean_cv': np.mean(cv_values),
                        'median_cv': np.median(cv_values),
                        'std_cv': np.std(cv_values),
                        'reliability_threshold_rate': sum(1 for cv in cv_values if cv <= 0.20) / len(cv_values),
                        'high_reliability_wells': [well.replace('well_', '') for well, stats in well_stats.items() 
                                                 if not np.isinf(stats['cv']) and stats['cv'] <= 0.15]
                    }
        
        # Framework comparison
        if 'framework' in self.data.columns:
            framework_stats = {}
            for framework in self.data['framework'].unique():
                framework_data = self.data[self.data['framework'] == framework]
                if len(framework_data) > 1 and self.well_columns:
                    framework_wells = framework_data[self.well_columns].dropna()
                    if len(framework_wells) > 0:
                        # Calculate average CV across wells for this framework
                        framework_cvs = []
                        for well in self.well_columns:
                            scores = framework_data[well].dropna()
                            if len(scores) > 1:
                                mean_val = scores.mean()
                                if mean_val != 0:
                                    cv = scores.std() / mean_val
                                    framework_cvs.append(cv)
                        
                        if framework_cvs:
                            framework_stats[framework] = {
                                'mean_cv': np.mean(framework_cvs),
                                'reliability_rate': sum(1 for cv in framework_cvs if cv <= 0.20) / len(framework_cvs),
                                'n_analyses': len(framework_data),
                                'success_rate': framework_data['success'].mean() if 'success' in self.data.columns else 1.0
                            }
            
            reliability_results['framework_reliability'] = framework_stats
        
        # Model comparison
        if 'model_name' in self.data.columns:
            model_stats = {}
            for model in self.data['model_name'].unique():
                model_data = self.data[self.data['model_name'] == model]
                if len(model_data) > 1:
                    model_stats[model] = {
                        'n_analyses': len(model_data),
                        'avg_cost': model_data['cost'].mean() if 'cost' in model_data else 0,
                        'avg_duration': model_data['duration_seconds'].mean() if 'duration_seconds' in model_data else 0,
                        'success_rate': model_data['success'].mean() if 'success' in model_data else 1.0
                    }
            
            reliability_results['model_reliability'] = model_stats
        
        self.analysis_results['reliability'] = reliability_results
        return reliability_results
    
    def perform_correlation_analysis(self) -> Dict:
        """Perform correlation analysis on well scores."""
        logger.info("📊 Performing correlation analysis...")
        
        if not self.well_columns or len(self.well_columns) < 2:
            logger.warning("Insufficient well data for correlation analysis")
            return {}
        
        # Prepare well data
        well_data = self.data[self.well_columns].dropna()
        
        if len(well_data) < 3:
            logger.warning("Insufficient data points for correlation analysis")
            return {}
        
        # Calculate correlations
        correlation_results = {
            'pearson_correlations': well_data.corr(method='pearson').to_dict(),
            'spearman_correlations': well_data.corr(method='spearman').to_dict(),
            'significant_correlations': []
        }
        
        # Test for significant correlations
        well_names = [col.replace('well_', '') for col in self.well_columns]
        for i, well1 in enumerate(self.well_columns):
            for j, well2 in enumerate(self.well_columns[i+1:], i+1):
                try:
                    r_pearson, p_pearson = pearsonr(well_data[well1], well_data[well2])
                    r_spearman, p_spearman = spearmanr(well_data[well1], well_data[well2])
                    
                    if p_pearson < 0.05:  # Significant correlation
                        correlation_results['significant_correlations'].append({
                            'well1': well1.replace('well_', ''),
                            'well2': well2.replace('well_', ''),
                            'pearson_r': r_pearson,
                            'pearson_p': p_pearson,
                            'spearman_r': r_spearman,
                            'spearman_p': p_spearman,
                            'strength': 'strong' if abs(r_pearson) > 0.7 else 'moderate' if abs(r_pearson) > 0.4 else 'weak'
                        })
                except Exception as e:
                    logger.warning(f"Could not calculate correlation between {well1} and {well2}: {e}")
        
        self.analysis_results['correlations'] = correlation_results
        return correlation_results
    
    def perform_comparative_analysis(self) -> Dict:
        """Perform comparative analysis across frameworks and models."""
        logger.info("🔬 Performing comparative analysis...")
        
        comparative_results = {}
        
        # Framework comparison using ANOVA
        if 'framework' in self.data.columns and len(self.data['framework'].unique()) > 1:
            framework_comparison = {}
            
            for well in self.well_columns:
                well_scores_by_framework = []
                framework_labels = []
                
                for framework in self.data['framework'].unique():
                    framework_scores = self.data[self.data['framework'] == framework][well].dropna()
                    if len(framework_scores) > 0:
                        well_scores_by_framework.append(framework_scores)
                        framework_labels.append(framework)
                
                if len(well_scores_by_framework) > 1:
                    try:
                        f_stat, p_value = stats.f_oneway(*well_scores_by_framework)
                        framework_comparison[well.replace('well_', '')] = {
                            'f_statistic': f_stat,
                            'p_value': p_value,
                            'significant': p_value < 0.05,
                            'frameworks_compared': framework_labels
                        }
                    except Exception as e:
                        logger.warning(f"Could not perform ANOVA for {well}: {e}")
            
            comparative_results['framework_anova'] = framework_comparison
        
        # Cost-effectiveness analysis
        if 'cost' in self.data.columns and 'duration_seconds' in self.data.columns:
            cost_analysis = {
                'total_cost': self.data['cost'].sum(),
                'avg_cost_per_analysis': self.data['cost'].mean(),
                'avg_duration': self.data['duration_seconds'].mean(),
                'cost_efficiency': self.data['cost'].sum() / len(self.data),  # Cost per successful analysis
            }
            
            # Cost by model
            if 'model_name' in self.data.columns:
                cost_by_model = self.data.groupby('model_name').agg({
                    'cost': ['sum', 'mean', 'count'],
                    'duration_seconds': 'mean'
                }).round(4)
                cost_by_model.columns = ['total_cost', 'avg_cost', 'n_analyses', 'avg_duration']
                cost_analysis['by_model'] = cost_by_model.to_dict('index')
            
            comparative_results['cost_analysis'] = cost_analysis
        
        self.analysis_results['comparative'] = comparative_results
        return comparative_results
    
    def generate_visualizations(self) -> Dict[str, str]:
        """Generate visualizations using the existing visualization engine."""
        logger.info("📈 Generating visualizations...")
        
        viz_files = {}
        output_dir = Path('experiment_reports/analysis/visualizations')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Use existing visualization engine for narrative position plots
            if self.well_columns and len(self.data) > 0:
                # Prepare data for visualization engine
                viz_data = []
                for _, row in self.data.iterrows():
                    well_scores = {col.replace('well_', ''): row[col] for col in self.well_columns if pd.notna(row[col])}
                    if well_scores:
                        viz_data.append({
                            'id': row.get('run_id', 'unknown'),
                            'scores': well_scores,
                            'metadata': {
                                'framework': row.get('framework', 'unknown'),
                                'model': row.get('model_name', 'unknown'),
                                'cost': row.get('cost', 0)
                            }
                        })
                
                if viz_data:
                    # Generate narrative position visualization
                    viz_file = self.viz_engine.create_narrative_position_plot(
                        viz_data,
                        title="IDITI Experiment Results - Narrative Positions",
                        output_path=str(output_dir / 'narrative_positions.png')
                    )
                    if viz_file:
                        viz_files['narrative_positions'] = viz_file
            
            # Generate additional plots using matplotlib/seaborn
            plt.style.use('default')
            
            # Reliability by well plot
            if 'reliability' in self.analysis_results and self.analysis_results['reliability']['well_reliability']:
                well_stats = self.analysis_results['reliability']['well_reliability']
                well_names = [w.replace('well_', '') for w in well_stats.keys()]
                cv_values = [stats['cv'] for stats in well_stats.values() if not np.isinf(stats['cv'])]
                
                if well_names and cv_values:
                    plt.figure(figsize=(12, 6))
                    bars = plt.bar(well_names, cv_values)
                    plt.axhline(y=0.20, color='red', linestyle='--', label='Reliability Threshold (0.20)')
                    plt.xlabel('Narrative Wells')
                    plt.ylabel('Coefficient of Variation')
                    plt.title('Well Reliability Analysis - IDITI Experiment')
                    plt.xticks(rotation=45, ha='right')
                    plt.legend()
                    plt.tight_layout()
                    
                    reliability_plot = output_dir / 'well_reliability.png'
                    plt.savefig(reliability_plot, dpi=300, bbox_inches='tight')
                    plt.close()
                    viz_files['well_reliability'] = str(reliability_plot)
            
            # Correlation heatmap
            if self.well_columns and len(self.data) > 2:
                well_data = self.data[self.well_columns].dropna()
                if len(well_data) > 0:
                    plt.figure(figsize=(10, 8))
                    correlation_matrix = well_data.corr()
                    # Clean up column names for display
                    correlation_matrix.columns = [col.replace('well_', '') for col in correlation_matrix.columns]
                    correlation_matrix.index = [idx.replace('well_', '') for idx in correlation_matrix.index]
                    
                    sns.heatmap(correlation_matrix, annot=True, cmap='RdBu_r', center=0, 
                               square=True, fmt='.2f', cbar_kws={'label': 'Correlation Coefficient'})
                    plt.title('Well Score Correlations - IDITI Experiment')
                    plt.tight_layout()
                    
                    correlation_plot = output_dir / 'well_correlations.png'
                    plt.savefig(correlation_plot, dpi=300, bbox_inches='tight')
                    plt.close()
                    viz_files['well_correlations'] = str(correlation_plot)
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
        
        return viz_files
    
    def generate_comprehensive_report(self) -> Dict:
        """Generate comprehensive analysis report."""
        logger.info("📋 Generating comprehensive report...")
        
        report = {
            'meta': {
                'analysis_timestamp': datetime.now().isoformat(),
                'data_file': self.data_file,
                'total_records': len(self.data) if self.data is not None else 0,
                'analysis_engine': 'Python-based IDITI Analysis',
                'frameworks_analyzed': list(self.data['framework'].unique()) if 'framework' in self.data.columns else [],
                'models_analyzed': list(self.data['model_name'].unique()) if 'model_name' in self.data.columns else []
            },
            'executive_summary': self._generate_executive_summary(),
            'detailed_results': self.analysis_results,
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_executive_summary(self) -> Dict:
        """Generate executive summary of key findings."""
        summary = {
            'data_quality': 'Unknown',
            'key_findings': [],
            'reliability_assessment': 'Unknown'
        }
        
        if 'reliability' in self.analysis_results:
            reliability = self.analysis_results['reliability']
            
            # Data quality assessment
            if 'overall_metrics' in reliability:
                metrics = reliability['overall_metrics']
                reliability_rate = metrics.get('reliability_threshold_rate', 0)
                
                if reliability_rate > 0.8:
                    summary['data_quality'] = 'Excellent'
                elif reliability_rate > 0.6:
                    summary['data_quality'] = 'Good'
                elif reliability_rate > 0.4:
                    summary['data_quality'] = 'Fair'
                else:
                    summary['data_quality'] = 'Poor'
                
                summary['reliability_assessment'] = f"{reliability_rate:.1%} of wells meet reliability threshold"
                
                # Key findings
                if metrics.get('high_reliability_wells'):
                    summary['key_findings'].append(f"High reliability wells: {', '.join(metrics['high_reliability_wells'])}")
                
                if metrics.get('mean_cv'):
                    summary['key_findings'].append(f"Average coefficient of variation: {metrics['mean_cv']:.3f}")
        
        return summary
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis results."""
        recommendations = []
        
        if 'reliability' in self.analysis_results:
            reliability = self.analysis_results['reliability']
            
            if 'overall_metrics' in reliability:
                metrics = reliability['overall_metrics']
                reliability_rate = metrics.get('reliability_threshold_rate', 0)
                
                if reliability_rate < 0.6:
                    recommendations.append("Consider increasing sample size or refining prompts to improve reliability")
                
                if 'high_reliability_wells' in metrics and len(metrics['high_reliability_wells']) > 0:
                    recommendations.append(f"Focus on high-reliability wells: {', '.join(metrics['high_reliability_wells'])}")
        
        if 'comparative' in self.analysis_results:
            comparative = self.analysis_results['comparative']
            
            if 'cost_analysis' in comparative:
                cost = comparative['cost_analysis']
                if cost.get('avg_cost_per_analysis', 0) > 0.05:  # More than 5 cents per analysis
                    recommendations.append("Consider cost optimization strategies for large-scale deployment")
        
        if not recommendations:
            recommendations.append("Data analysis complete - proceed with confidence to multi-LLM validation")
        
        return recommendations

def main():
    """Main analysis pipeline."""
    logger.info("🚀 Starting IDITI Experiment Analysis")
    
    # Initialize analysis engine
    data_file = "exports/analysis_results/extracted_results_20250617_081917.csv"
    
    if not Path(data_file).exists():
        logger.error(f"Data file not found: {data_file}")
        return
    
    analyzer = IDITIAnalysisEngine(data_file)
    
    try:
        # Load and prepare data
        analyzer.load_and_prepare_data()
        
        # Perform analyses
        reliability_results = analyzer.calculate_reliability_metrics()
        correlation_results = analyzer.perform_correlation_analysis()
        comparative_results = analyzer.perform_comparative_analysis()
        
        # Generate visualizations
        viz_files = analyzer.generate_visualizations()
        
        # Generate comprehensive report
        final_report = analyzer.generate_comprehensive_report()
        
        # Save results
        output_dir = Path('experiment_reports/analysis')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = output_dir / f'iditi_analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump(final_report, f, indent=2, default=str)
        
        # Print summary
        logger.info("✅ Analysis Complete!")
        logger.info(f"📊 Report saved to: {report_file}")
        
        if viz_files:
            logger.info("📈 Visualizations generated:")
            for name, path in viz_files.items():
                logger.info(f"   • {name}: {path}")
        
        # Print key findings
        exec_summary = final_report['executive_summary']
        logger.info(f"\n🎯 Executive Summary:")
        logger.info(f"   Data Quality: {exec_summary['data_quality']}")
        logger.info(f"   Reliability: {exec_summary['reliability_assessment']}")
        
        if exec_summary['key_findings']:
            logger.info("   Key Findings:")
            for finding in exec_summary['key_findings']:
                logger.info(f"     • {finding}")
        
        logger.info("🚀 Ready for integration into orchestrator!")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    main() 