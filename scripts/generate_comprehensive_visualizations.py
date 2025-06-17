#!/usr/bin/env python3
"""
Framework-Aware Visualization Generator for Narrative Gravity Analysis
Uses production NarrativeGravityVisualizationEngine for consistent, theme-aware visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import logging
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import json
import sys
import warnings
warnings.filterwarnings('ignore')

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from narrative_gravity.visualization.engine import NarrativeGravityVisualizationEngine
from narrative_gravity.framework_manager import FrameworkManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VisualizationGenerator:
    """Framework-aware visualization generator using production visualization engine."""
    
    def __init__(self, output_dir: str = "experiment_reports/analysis/visualizations"):
        """Initialize the visualization generator with production engine."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generated_files = {}
        
        # Initialize production systems
        self.viz_engine = NarrativeGravityVisualizationEngine(theme='academic')
        self.framework_manager = FrameworkManager()
        
        logger.info(f"✅ Initialized visualization generator with production engine")
        logger.info(f"📊 Theme: {self.viz_engine.theme_name}")
        
    def generate_visualizations(self, structured_results: Dict, statistical_results: Dict, 
                              reliability_results: Dict) -> Dict[str, Any]:
        """
        Generate comprehensive visualizations using production visualization engine.
        
        Args:
            structured_results: Structured experiment data
            statistical_results: Statistical hypothesis testing results
            reliability_results: Interrater reliability analysis results
            
        Returns:
            Dictionary containing paths to generated visualization files
        """
        logger.info("🎨 Starting comprehensive visualization generation...")
        
        df = structured_results.get('structured_data')
        if df is None or df.empty:
            logger.error("No structured data available for visualization")
            return {'error': 'No data available'}
        
        # Get framework information
        frameworks_used = df['framework'].unique() if 'framework' in df.columns else ['unknown']
        primary_framework = frameworks_used[0] if len(frameworks_used) > 0 else 'unknown'
        
        # Load framework definition for well structure
        framework_wells = self._get_framework_wells(primary_framework)
        well_columns = [col for col in df.columns if col.startswith('well_')]
        
        logger.info(f"📊 Generating visualizations for {primary_framework} framework")
        logger.info(f"🎯 Framework wells: {framework_wells}")
        logger.info(f"📈 Data wells: {[col.replace('well_', '') for col in well_columns]}")
        
        # Generate different types of visualizations using production engine
        viz_results = {
            'descriptive_plots': self.create_descriptive_plots(df, well_columns, primary_framework),
            'hypothesis_plots': self.create_hypothesis_plots(statistical_results),
            'reliability_plots': self.create_reliability_plots(reliability_results),
            'correlation_plots': self.create_framework_correlation_plots(df, well_columns, primary_framework),
            'distribution_plots': self.create_distribution_plots(df, well_columns),
            'narrative_gravity_plots': self.create_production_narrative_plots(df, well_columns, primary_framework),
            'interactive_dashboard': self.create_production_dashboard(df, well_columns, statistical_results, primary_framework),
            'generated_files': self.generated_files
        }
        
        logger.info(f"✅ Generated {len(self.generated_files)} visualization files using production engine")
        return viz_results

    def _get_framework_wells(self, framework_name: str) -> List[str]:
        """Get the list of wells defined for a specific framework."""
        try:
            framework = self.framework_manager.load_framework(framework_name)
            if hasattr(framework, 'wells') and framework.wells:
                return list(framework.wells.keys())
            elif hasattr(framework, 'dipoles'):
                # Extract well names from dipoles
                wells = []
                for dipole in framework.dipoles:
                    if hasattr(dipole, 'positive') and hasattr(dipole.positive, 'name'):
                        wells.append(dipole.positive.name)
                    if hasattr(dipole, 'negative') and hasattr(dipole.negative, 'name'):
                        wells.append(dipole.negative.name)
                return wells
            else:
                logger.warning(f"Framework {framework_name} has no defined wells")
                return []
        except Exception as e:
            logger.warning(f"Could not load framework {framework_name}: {e}")
            return []

    def _prepare_framework_data(self, df: pd.DataFrame, well_columns: List[str], framework_name: str) -> Dict:
        """Prepare data in format expected by production visualization engine."""
        framework_wells = self._get_framework_wells(framework_name)
        
        # Build wells configuration for visualization engine
        wells = {}
        try:
            framework = self.framework_manager.load_framework(framework_name)
            
            if hasattr(framework, 'wells') and framework.wells:
                for well_name, well_config in framework.wells.items():
                    wells[well_name] = {
                        'angle': getattr(well_config, 'angle', 0),
                        'type': getattr(well_config, 'type', 'integrative'),
                        'weight': getattr(well_config, 'weight', 1.0)
                    }
            elif hasattr(framework, 'dipoles'):
                # Build wells from dipoles
                for dipole in framework.dipoles:
                    if hasattr(dipole, 'positive'):
                        wells[dipole.positive.name] = {
                            'angle': getattr(dipole.positive, 'angle', 90),
                            'type': 'integrative',
                            'weight': getattr(dipole.positive, 'weight', 1.0)
                        }
                    if hasattr(dipole, 'negative'):
                        wells[dipole.negative.name] = {
                            'angle': getattr(dipole.negative, 'angle', 270),
                            'type': 'disintegrative', 
                            'weight': getattr(dipole.negative, 'weight', -1.0)
                        }
        except Exception as e:
            logger.warning(f"Could not load framework configuration for {framework_name}: {e}")
        
        return wells

    def create_production_narrative_plots(self, df: pd.DataFrame, well_columns: List[str], 
                                        framework_name: str) -> Dict[str, str]:
        """Create narrative gravity plots using production visualization engine."""
        logger.info("🌌 Creating narrative gravity plots with production engine...")
        
        plots = {}
        
        # Prepare framework configuration
        wells = self._prepare_framework_data(df, well_columns, framework_name)
        
        if not wells:
            logger.warning("No framework wells configuration available")
            return plots
        
        # Create multiple analyses for comparison
        analyses = []
        for i, row in df.iterrows():
            # Extract narrative scores from row
            narrative_scores = {}
            for well_name in wells.keys():
                well_col = f"well_{well_name.lower().replace(' ', '_').replace('-', '_')}"
                if well_col in df.columns:
                    narrative_scores[well_name] = row[well_col]
            
            if narrative_scores:
                analyses.append({
                    'title': row.get('text_id', f'Analysis {i}'),
                    'wells': wells,
                    'scores': narrative_scores,
                    'metadata': {
                        'framework': framework_name,
                        'model': row.get('model', 'unknown'),
                        'cost': row.get('api_cost', 0.0)
                    }
                })
        
        if analyses:
            # Create single analysis visualization (first analysis)
            single_fig = self.viz_engine.create_single_analysis(
                wells=wells,
                narrative_scores=analyses[0]['scores'],
                title=f'{framework_name.upper()} Framework - {analyses[0]["title"]}',
                show=False
            )
            
            # Save single analysis
            single_plot_file = self.output_dir / 'narrative_gravity_map.png'
            single_fig.write_image(str(single_plot_file), width=1200, height=800)
            plots['narrative_gravity_map'] = str(single_plot_file)
            self.generated_files['narrative_gravity_map'] = str(single_plot_file)
            
            # Create comparative analysis if multiple analyses
            if len(analyses) > 1:
                # Take first few for comparison to avoid clutter
                comparison_analyses = analyses[:min(6, len(analyses))]
                
                comp_fig = self.viz_engine.create_comparative_analysis(
                    analyses=comparison_analyses,
                    title=f'{framework_name.upper()} Framework - Comparative Analysis',
                    show=False
                )
                
                comp_plot_file = self.output_dir / 'comparative_narrative_analysis.png'
                comp_fig.write_image(str(comp_plot_file), width=1600, height=1000)
                plots['comparative_analysis'] = str(comp_plot_file)
                self.generated_files['comparative_analysis'] = str(comp_plot_file)
        
        return plots

    def create_framework_correlation_plots(self, df: pd.DataFrame, well_columns: List[str], 
                                         framework_name: str) -> Dict[str, str]:
        """Create correlation matrix showing only framework-defined wells."""
        logger.info("🔗 Creating framework-aware correlation plots...")
        
        plots = {}
        
        if len(well_columns) < 2:
            return plots
        
        # Get framework wells to filter correlation matrix
        framework_wells = self._get_framework_wells(framework_name)
        
        # Filter well columns to only framework-defined wells
        filtered_well_columns = []
        for well_name in framework_wells:
            well_col = f"well_{well_name.lower().replace(' ', '_').replace('-', '_')}"
            if well_col in well_columns:
                filtered_well_columns.append(well_col)
        
        if len(filtered_well_columns) >= 2:
            well_data = df[filtered_well_columns].dropna()
            if not well_data.empty:
                correlation_matrix = well_data.corr()
                
                # Create correlation heatmap with framework styling
                plt.figure(figsize=(10, 8))
                mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
                sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='RdBu_r', center=0,
                           square=True, linewidths=0.5, cbar_kws={"shrink": .8})
                plt.title(f'{framework_name.upper()} Framework - Well Scores Correlation Matrix', 
                         fontsize=14, fontweight='bold')
                
                # Clean up labels to show framework well names
                labels = []
                for col in filtered_well_columns:
                    well_name = col.replace('well_', '')
                    # Try to find the original well name in framework
                    for fw_well in framework_wells:
                        if fw_well.lower().replace(' ', '_').replace('-', '_') == well_name:
                            labels.append(fw_well)
                            break
                    else:
                        labels.append(well_name)
                
                plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
                plt.yticks(range(len(labels)), labels, rotation=0)
                
                plt.tight_layout()
                
                plot_file = self.output_dir / 'correlation_matrix.png'
                plt.savefig(plot_file, dpi=300, bbox_inches='tight')
                plt.close()
                
                plots['correlation_matrix'] = str(plot_file)
                self.generated_files['correlation_matrix'] = str(plot_file)
        
        return plots

    def create_production_dashboard(self, df: pd.DataFrame, well_columns: List[str], 
                                  statistical_results: Dict, framework_name: str) -> Dict[str, str]:
        """Create interactive dashboard using production visualization components."""
        logger.info("🎮 Creating interactive dashboard with production components...")
        
        plots = {}
        
        # Prepare framework data
        wells = self._prepare_framework_data(df, well_columns, framework_name)
        
        if not wells:
            logger.warning("No framework configuration for dashboard")
            return plots
        
        # Create dashboard with production engine
        try:
            # Prepare analyses for dashboard
            analyses = []
            for i, row in df.iterrows():
                narrative_scores = {}
                for well_name in wells.keys():
                    well_col = f"well_{well_name.lower().replace(' ', '_').replace('-', '_')}"
                    if well_col in df.columns:
                        narrative_scores[well_name] = row[well_col]
                
                if narrative_scores:
                    analyses.append({
                        'title': row.get('text_id', f'Analysis {i}'),
                        'wells': wells,
                        'scores': narrative_scores
                    })
            
            if analyses:
                # Create dashboard HTML
                dashboard_fig = self.viz_engine.create_comparative_analysis(
                    analyses=analyses[:10],  # Limit for performance
                    title=f'{framework_name.upper()} Framework - Interactive Dashboard',
                    show=False
                )
                
                dashboard_file = self.output_dir / 'interactive_dashboard.html'
                dashboard_fig.write_html(str(dashboard_file))
                
                plots['interactive_dashboard'] = str(dashboard_file)
                self.generated_files['interactive_dashboard'] = str(dashboard_file)
        
        except Exception as e:
            logger.warning(f"Could not create production dashboard: {e}")
        
        return plots

    # Keep minimal custom plots for statistical results that don't have production equivalents
    def create_descriptive_plots(self, df: pd.DataFrame, well_columns: List[str], framework_name: str) -> Dict[str, str]:
        """Create minimal descriptive plots for statistical overview."""
        logger.info("📊 Creating descriptive plots...")
        
        plots = {}
        framework_wells = self._get_framework_wells(framework_name)
        
        # Filter to framework wells only
        filtered_well_columns = []
        for well_name in framework_wells:
            well_col = f"well_{well_name.lower().replace(' ', '_').replace('-', '_')}"
            if well_col in well_columns:
                filtered_well_columns.append(well_col)
        
        if filtered_well_columns:
            fig, axes = plt.subplots(1, 2, figsize=(15, 6))
            fig.suptitle(f'{framework_name.upper()} Framework - Descriptive Analysis', fontsize=14, fontweight='bold')
            
            # Well means with proper framework labels
            well_data = df[filtered_well_columns].dropna()
            if not well_data.empty:
                means = [well_data[col].mean() for col in filtered_well_columns]
                stds = [well_data[col].std() for col in filtered_well_columns]
                
                # Get proper well names
                well_names = []
                for col in filtered_well_columns:
                    well_name = col.replace('well_', '')
                    for fw_well in framework_wells:
                        if fw_well.lower().replace(' ', '_').replace('-', '_') == well_name:
                            well_names.append(fw_well)
                            break
                    else:
                        well_names.append(well_name)
                
                axes[0].bar(well_names, means, yerr=stds, capsize=5, alpha=0.7)
                axes[0].set_title(f'Mean Well Scores ({framework_name})')
                axes[0].set_ylabel('Mean Score')
                axes[0].tick_params(axis='x', rotation=45)
            
            # Cost and quality analysis
            if 'api_cost' in df.columns and 'quality_score' in df.columns:
                axes[1].scatter(df['api_cost'], df['quality_score'], alpha=0.6)
                axes[1].set_xlabel('API Cost ($)')
                axes[1].set_ylabel('Quality Score')
                axes[1].set_title('Cost vs Quality Analysis')
            
            plt.tight_layout()
            
            plot_file = self.output_dir / 'descriptive_analysis.png'
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            plots['descriptive_analysis'] = str(plot_file)
            self.generated_files['descriptive_analysis'] = str(plot_file)
        
        return plots

    def create_hypothesis_plots(self, statistical_results: Dict) -> Dict[str, str]:
        """Create plots for hypothesis testing results."""
        logger.info("🎯 Creating hypothesis testing plots...")
        
        plots = {}
        
        if 'hypothesis_testing' not in statistical_results:
            return plots
        
        hypothesis_data = statistical_results['hypothesis_testing']
        
        # Create minimal hypothesis summary
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        fig.suptitle('Hypothesis Testing Results Summary', fontsize=14, fontweight='bold')
        
        # Collect hypothesis results
        hypothesis_names = []
        statuses = []
        
        for h_name, h_results in hypothesis_data.items():
            if isinstance(h_results, dict):
                hypothesis_names.append(h_name.replace('_', ' ').title())
                status = h_results.get('status', 'unknown')
                statuses.append(status)
        
        if hypothesis_names:
            # Color code by status
            colors = []
            for status in statuses:
                if status == 'supported':
                    colors.append('green')
                elif status == 'insufficient_data':
                    colors.append('orange')
                else:
                    colors.append('red')
            
            ax.bar(hypothesis_names, [1] * len(hypothesis_names), color=colors, alpha=0.7)
            ax.set_title('Hypothesis Testing Status')
            ax.set_ylabel('Status')
            ax.set_ylim(0, 1.2)
            ax.tick_params(axis='x', rotation=45)
            
            # Add status labels
            for i, (name, status) in enumerate(zip(hypothesis_names, statuses)):
                ax.text(i, 0.5, status.replace('_', ' ').title(), 
                       ha='center', va='center', fontweight='bold', color='white')
        
        plt.tight_layout()
        
        plot_file = self.output_dir / 'hypothesis_testing_results.png'
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        plots['hypothesis_testing'] = str(plot_file)
        self.generated_files['hypothesis_testing'] = str(plot_file)
        
        return plots

    def create_reliability_plots(self, reliability_results: Dict) -> Dict[str, str]:
        """Create minimal reliability plots."""
        logger.info("🔍 Creating reliability plots...")
        
        plots = {}
        
        # Simple reliability summary
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, 'Reliability Analysis\n(See reliability_results.json for details)', 
                ha='center', va='center', fontsize=14, transform=plt.gca().transAxes)
        plt.title('Reliability Analysis Summary', fontsize=14, fontweight='bold')
        plt.axis('off')
        
        plot_file = self.output_dir / 'reliability_analysis.png'
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        plots['reliability_analysis'] = str(plot_file)
        self.generated_files['reliability_analysis'] = str(plot_file)
        
        return plots

    def create_distribution_plots(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, str]:
        """Create distribution plots (minimal version)."""
        logger.info("📈 Creating distribution plots...")
        
        plots = {}
        
        if well_columns:
            # Simple summary plot
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, f'Distribution Analysis\n{len(well_columns)} wells analyzed\n(See interactive dashboard for details)', 
                    ha='center', va='center', fontsize=14, transform=plt.gca().transAxes)
            plt.title('Score Distributions Summary', fontsize=14, fontweight='bold')
            plt.axis('off')
            
            plot_file = self.output_dir / 'score_distributions.png'
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            plots['score_distributions'] = str(plot_file)
            self.generated_files['score_distributions'] = str(plot_file)
        
        return plots

    def save_visualization_index(self) -> str:
        """Save index of generated visualizations."""
        index_data = {
            'generation_timestamp': pd.Timestamp.now().isoformat(),
            'visualization_engine': 'NarrativeGravityVisualizationEngine (Production)',
            'theme': self.viz_engine.theme_name,
            'files_generated': self.generated_files,
            'total_files': len(self.generated_files)
        }
        
        index_file = self.output_dir / 'visualization_index.json'
        with open(index_file, 'w') as f:
            json.dump(index_data, f, indent=2)
        
        return str(index_file)

def main():
    """Main execution function for standalone testing."""
    
    # For testing purposes, try to load recent data
    data_files = list(Path("exports/analysis_results/").glob("extracted_results_*.csv"))
    
    if not data_files:
        logger.error("No extracted results files found. Run extract_experiment_results.py first.")
        return
    
    # Use most recent file
    latest_file = max(data_files, key=lambda x: x.stat().st_mtime)
    logger.info(f"Testing with data from: {latest_file}")
    
    # Load data
    df = pd.read_csv(latest_file)
    
    # Create mock inputs
    well_columns = [col for col in df.columns if col.startswith('well_')]
    
    structured_results = {
        'structured_data': df,
        'metadata': {
            'well_columns': well_columns,
            'frameworks_used': df['framework'].unique().tolist() if 'framework' in df.columns else [],
            'models_used': df['model_name'].unique().tolist() if 'model_name' in df.columns else []
        }
    }
    
    # Mock statistical and reliability results
    statistical_results = {'hypothesis_testing': {}}
    reliability_results = {}
    
    # Generate visualizations
    generator = VisualizationGenerator()
    results = generator.generate_visualizations(structured_results, statistical_results, reliability_results)
    
    # Create index
    index_file = generator.save_visualization_index()
    
    logger.info(f"✅ Visualization generation complete!")
    logger.info(f"📁 Generated files: {len(generator.generated_files)}")
    logger.info(f"📋 Index file: {index_file}")
    
    # Print generated files
    for name, path in generator.generated_files.items():
        print(f"  📊 {name}: {path}")

if __name__ == "__main__":
    main() 