#!/usr/bin/env python3
"""
Comprehensive Visualization Generator for Narrative Gravity Analysis
Creates publication-ready visualizations for statistical analysis and reliability metrics
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
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set style for matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class VisualizationGenerator:
    """Comprehensive visualization generator for narrative gravity analysis."""
    
    def __init__(self, output_dir: str = "experiment_reports/analysis/visualizations"):
        """Initialize the visualization generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generated_files = {}
        
    def generate_visualizations(self, structured_results: Dict, statistical_results: Dict, 
                              reliability_results: Dict) -> Dict[str, Any]:
        """
        Generate comprehensive visualizations for all analysis results.
        
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
        
        well_columns = [col for col in df.columns if col.startswith('well_')]
        
        # Generate different types of visualizations
        viz_results = {
            'descriptive_plots': self.create_descriptive_plots(df, well_columns),
            'hypothesis_plots': self.create_hypothesis_plots(statistical_results),
            'reliability_plots': self.create_reliability_plots(reliability_results),
            'correlation_plots': self.create_correlation_plots(df, well_columns),
            'distribution_plots': self.create_distribution_plots(df, well_columns),
            'narrative_gravity_plots': self.create_narrative_gravity_plots(df, well_columns),
            'interactive_dashboard': self.create_interactive_dashboard(df, well_columns, statistical_results),
            'generated_files': self.generated_files
        }
        
        logger.info(f"✅ Generated {len(self.generated_files)} visualization files")
        return viz_results
    
    def create_descriptive_plots(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, str]:
        """Create descriptive statistical plots."""
        logger.info("📊 Creating descriptive plots...")
        
        plots = {}
        
        # 1. Well scores distribution
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Well Scores Distribution Analysis', fontsize=16, fontweight='bold')
        
        # Box plot
        if len(well_columns) > 0:
            well_data = df[well_columns].dropna()
            axes[0, 0].boxplot([well_data[col].dropna() for col in well_columns], 
                              labels=[col.replace('well_', '') for col in well_columns])
            axes[0, 0].set_title('Well Scores Distribution')
            axes[0, 0].set_ylabel('Score')
            axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Violin plot
        if len(well_columns) > 0:
            well_data_melted = pd.melt(df[well_columns], var_name='Well', value_name='Score')
            well_data_melted['Well'] = well_data_melted['Well'].str.replace('well_', '')
            sns.violinplot(data=well_data_melted, x='Well', y='Score', ax=axes[0, 1])
            axes[0, 1].set_title('Well Scores Density Distribution')
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Mean scores by well
        if len(well_columns) > 0:
            means = [df[col].mean() for col in well_columns]
            stds = [df[col].std() for col in well_columns]
            well_names = [col.replace('well_', '') for col in well_columns]
            
            axes[1, 0].bar(well_names, means, yerr=stds, capsize=5, alpha=0.7)
            axes[1, 0].set_title('Mean Well Scores with Standard Deviation')
            axes[1, 0].set_ylabel('Mean Score')
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Cost and quality analysis
        if 'cost' in df.columns and 'quality_score' in df.columns:
            scatter = axes[1, 1].scatter(df['cost'], df['quality_score'], alpha=0.6)
            axes[1, 1].set_xlabel('API Cost ($)')
            axes[1, 1].set_ylabel('Quality Score')
            axes[1, 1].set_title('Cost vs Quality Analysis')
        
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
        
        # Create hypothesis summary plot
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('Hypothesis Testing Results Summary', fontsize=16, fontweight='bold')
        
        # H1: Discriminative Validity
        h1_results = hypothesis_data.get('H1_discriminative_validity', {})
        if h1_results.get('tests_performed'):
            test_names = []
            p_values = []
            significance = []
            
            for test in h1_results['tests_performed']:
                test_names.append(test.get('comparison', 'Test'))
                p_values.append(test.get('p_value', 1.0))
                significance.append('Significant' if test.get('significant', False) else 'Not Significant')
            
            colors = ['green' if sig == 'Significant' else 'red' for sig in significance]
            axes[0].bar(range(len(test_names)), p_values, color=colors, alpha=0.7)
            axes[0].axhline(y=0.05, color='red', linestyle='--', alpha=0.5, label='α = 0.05')
            axes[0].set_title('H1: Discriminative Validity\np-values')
            axes[0].set_ylabel('p-value')
            axes[0].set_yscale('log')
            axes[0].legend()
        
        # H2: Ideological Agnosticism
        h2_results = hypothesis_data.get('H2_ideological_agnosticism', {})
        if h2_results.get('tests_performed'):
            well_names = []
            p_values = []
            effect_sizes = []
            
            for test in h2_results['tests_performed']:
                well_names.append(test.get('well', 'Well').replace('well_', ''))
                p_values.append(test.get('p_value', 1.0))
                effect_sizes.append(test.get('effect_size', 0.0))
            
            # Scatter plot of p-values vs effect sizes
            scatter = axes[1].scatter(effect_sizes, p_values, alpha=0.7, s=60)
            axes[1].axhline(y=0.05, color='red', linestyle='--', alpha=0.5, label='α = 0.05')
            axes[1].set_xlabel('Effect Size')
            axes[1].set_ylabel('p-value')
            axes[1].set_title('H2: Ideological Agnosticism\nEffect Size vs p-value')
            axes[1].set_yscale('log')
            axes[1].legend()
        
        # H3: Ground Truth Alignment
        h3_results = hypothesis_data.get('H3_ground_truth_alignment', {})
        if h3_results.get('tests_performed'):
            text_ids = []
            scores = []
            meets_threshold = []
            
            for test in h3_results['tests_performed']:
                text_ids.append(test.get('text_id', 'Text')[:20])  # Truncate for display
                scores.append(test.get('score', 0.0))
                meets_threshold.append(test.get('meets_threshold', False))
            
            colors = ['green' if meets else 'red' for meets in meets_threshold]
            bars = axes[2].bar(range(len(text_ids)), scores, color=colors, alpha=0.7)
            axes[2].axhline(y=0.8, color='red', linestyle='--', alpha=0.5, label='Threshold = 0.8')
            axes[2].set_title('H3: Ground Truth Alignment\nControl Text Performance')
            axes[2].set_ylabel('Score')
            axes[2].set_xticks(range(len(text_ids)))
            axes[2].set_xticklabels(text_ids, rotation=45, ha='right')
            axes[2].legend()
        
        plt.tight_layout()
        
        plot_file = self.output_dir / 'hypothesis_testing_results.png'
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        plots['hypothesis_testing'] = str(plot_file)
        self.generated_files['hypothesis_testing'] = str(plot_file)
        
        return plots
    
    def create_reliability_plots(self, reliability_results: Dict) -> Dict[str, str]:
        """Create plots for reliability analysis results."""
        logger.info("🔍 Creating reliability plots...")
        
        plots = {}
        
        if not reliability_results or 'error' in reliability_results:
            return plots
        
        # ICC Analysis Plot
        icc_data = reliability_results.get('icc_analysis', {})
        if icc_data:
            fig, axes = plt.subplots(1, 2, figsize=(15, 6))
            fig.suptitle('Interrater Reliability Analysis', fontsize=16, fontweight='bold')
            
            # ICC values by well
            wells = []
            icc_values = []
            interpretations = []
            
            for well, icc_result in icc_data.items():
                if icc_result.get('icc_value') is not None:
                    wells.append(well.replace('well_', ''))
                    icc_values.append(icc_result['icc_value'])
                    interpretations.append(icc_result.get('interpretation', 'unknown'))
            
            if wells:
                # Color code by interpretation
                color_map = {'poor': 'red', 'moderate': 'orange', 'good': 'lightgreen', 'excellent': 'green'}
                colors = [color_map.get(interp, 'gray') for interp in interpretations]
                
                bars = axes[0].bar(wells, icc_values, color=colors, alpha=0.7)
                axes[0].axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Poor threshold')
                axes[0].axhline(y=0.75, color='orange', linestyle='--', alpha=0.5, label='Good threshold')
                axes[0].axhline(y=0.9, color='green', linestyle='--', alpha=0.5, label='Excellent threshold')
                axes[0].set_title('Intraclass Correlation Coefficients (ICC)')
                axes[0].set_ylabel('ICC Value')
                axes[0].set_ylim(0, 1.0)
                axes[0].tick_params(axis='x', rotation=45)
                axes[0].legend()
                
                # Add interpretation labels on bars
                for bar, interp in zip(bars, interpretations):
                    height = bar.get_height()
                    axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                               interp.replace('_', ' ').title(),
                               ha='center', va='bottom', fontsize=8, rotation=90)
        
        # Coefficient of Variation
        cv_data = reliability_results.get('coefficient_of_variation', {})
        if cv_data:
            wells = []
            cv_values = []
            
            for well, cv_result in cv_data.items():
                wells.append(well.replace('well_', ''))
                cv_values.append(cv_result['coefficient_of_variation'])
            
            if wells:
                axes[1].bar(wells, cv_values, alpha=0.7, color='skyblue')
                axes[1].set_title('Coefficient of Variation by Well')
                axes[1].set_ylabel('CV (%)')
                axes[1].tick_params(axis='x', rotation=45)
                axes[1].axhline(y=20, color='orange', linestyle='--', alpha=0.5, label='Moderate variability')
                axes[1].legend()
        
        plt.tight_layout()
        
        plot_file = self.output_dir / 'reliability_analysis.png'
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        plots['reliability_analysis'] = str(plot_file)
        self.generated_files['reliability_analysis'] = str(plot_file)
        
        return plots
    
    def create_correlation_plots(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, str]:
        """Create correlation matrix and related plots."""
        logger.info("🔗 Creating correlation plots...")
        
        plots = {}
        
        if len(well_columns) < 2:
            return plots
        
        # Correlation matrix
        well_data = df[well_columns].dropna()
        if not well_data.empty:
            correlation_matrix = well_data.corr()
            
            # Create correlation heatmap
            plt.figure(figsize=(12, 10))
            mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
            sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                       square=True, linewidths=0.5, cbar_kws={"shrink": .8})
            plt.title('Well Scores Correlation Matrix', fontsize=16, fontweight='bold')
            
            # Clean up labels
            labels = [col.replace('well_', '') for col in well_columns]
            plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
            plt.yticks(range(len(labels)), labels, rotation=0)
            
            plt.tight_layout()
            
            plot_file = self.output_dir / 'correlation_matrix.png'
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            plots['correlation_matrix'] = str(plot_file)
            self.generated_files['correlation_matrix'] = str(plot_file)
        
        return plots
    
    def create_distribution_plots(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, str]:
        """Create distribution analysis plots."""
        logger.info("📈 Creating distribution plots...")
        
        plots = {}
        
        if not well_columns:
            return plots
        
        # Create distribution plots for each well
        n_wells = len(well_columns)
        n_cols = 4
        n_rows = (n_wells + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
        fig.suptitle('Well Score Distributions', fontsize=16, fontweight='bold')
        
        if n_rows == 1:
            axes = axes.reshape(1, -1)
        
        for i, well_col in enumerate(well_columns):
            row = i // n_cols
            col = i % n_cols
            
            well_data = df[well_col].dropna()
            if len(well_data) > 0:
                axes[row, col].hist(well_data, bins=20, alpha=0.7, edgecolor='black')
                axes[row, col].axvline(well_data.mean(), color='red', linestyle='--', 
                                     label=f'Mean: {well_data.mean():.3f}')
                axes[row, col].axvline(well_data.median(), color='green', linestyle='--', 
                                     label=f'Median: {well_data.median():.3f}')
                axes[row, col].set_title(well_col.replace('well_', ''))
                axes[row, col].set_xlabel('Score')
                axes[row, col].set_ylabel('Frequency')
                axes[row, col].legend()
        
        # Hide empty subplots
        for i in range(n_wells, n_rows * n_cols):
            row = i // n_cols
            col = i % n_cols
            axes[row, col].set_visible(False)
        
        plt.tight_layout()
        
        plot_file = self.output_dir / 'score_distributions.png'
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        plots['score_distributions'] = str(plot_file)
        self.generated_files['score_distributions'] = str(plot_file)
        
        return plots
    
    def create_narrative_gravity_plots(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[str, str]:
        """Create narrative gravity specific visualizations."""
        logger.info("🌌 Creating narrative gravity plots...")
        
        plots = {}
        
        # Check if we have narrative position data
        if 'narrative_position_x' in df.columns and 'narrative_position_y' in df.columns:
            # Narrative gravity scatter plot
            plt.figure(figsize=(12, 10))
            
            # Create scatter plot
            scatter = plt.scatter(df['narrative_position_x'], df['narrative_position_y'], 
                                alpha=0.7, s=80, c=df.index, cmap='viridis')
            
            # Add text labels if text_id is available
            if 'text_id' in df.columns:
                for i, txt in enumerate(df['text_id']):
                    if pd.notna(txt):
                        plt.annotate(str(txt)[:10], 
                                   (df['narrative_position_x'].iloc[i], df['narrative_position_y'].iloc[i]),
                                   xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.7)
            
            plt.xlabel('Narrative Position X')
            plt.ylabel('Narrative Position Y')
            plt.title('Narrative Gravity Positioning Map', fontsize=16, fontweight='bold')
            plt.grid(True, alpha=0.3)
            plt.colorbar(scatter, label='Analysis Index')
            
            # Add quadrant lines
            plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
            
            plt.tight_layout()
            
            plot_file = self.output_dir / 'narrative_gravity_map.png'
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            plots['narrative_gravity_map'] = str(plot_file)
            self.generated_files['narrative_gravity_map'] = str(plot_file)
        
        # Well comparison radar chart
        if len(well_columns) >= 3:
            # Create radar chart for mean well scores
            well_means = [df[col].mean() for col in well_columns]
            well_names = [col.replace('well_', '') for col in well_columns]
            
            # Create radar chart
            angles = np.linspace(0, 2 * np.pi, len(well_names), endpoint=False).tolist()
            well_means += well_means[:1]  # Complete the circle
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
            ax.plot(angles, well_means, 'o-', linewidth=2, label='Mean Scores')
            ax.fill(angles, well_means, alpha=0.25)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(well_names)
            ax.set_ylim(0, 1)
            ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
            ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'])
            ax.grid(True)
            plt.title('Mean Well Scores Radar Chart', fontsize=16, fontweight='bold', pad=20)
            plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
            
            plt.tight_layout()
            
            plot_file = self.output_dir / 'well_scores_radar.png'
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            plots['well_scores_radar'] = str(plot_file)
            self.generated_files['well_scores_radar'] = str(plot_file)
        
        return plots
    
    def create_interactive_dashboard(self, df: pd.DataFrame, well_columns: List[str], 
                                   statistical_results: Dict) -> Dict[str, str]:
        """Create interactive Plotly dashboard."""
        logger.info("🎮 Creating interactive dashboard...")
        
        plots = {}
        
        if not well_columns:
            return plots
        
        # Create subplot dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Well Scores Distribution', 'Narrative Gravity Map', 
                          'Correlation Heatmap', 'Hypothesis Testing Results'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 1. Well scores box plot
        for col in well_columns:
            well_data = df[col].dropna()
            if len(well_data) > 0:
                fig.add_trace(
                    go.Box(y=well_data, name=col.replace('well_', ''), showlegend=False),
                    row=1, col=1
                )
        
        # 2. Narrative gravity scatter plot
        if 'narrative_position_x' in df.columns and 'narrative_position_y' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df['narrative_position_x'],
                    y=df['narrative_position_y'],
                    mode='markers',
                    text=df['text_id'] if 'text_id' in df.columns else df.index,
                    hovertemplate='<b>%{text}</b><br>X: %{x}<br>Y: %{y}<extra></extra>',
                    showlegend=False
                ),
                row=1, col=2
            )
        
        # 3. Correlation heatmap
        if len(well_columns) > 1:
            well_data = df[well_columns].dropna()
            if not well_data.empty:
                correlation_matrix = well_data.corr()
                fig.add_trace(
                    go.Heatmap(
                        z=correlation_matrix.values,
                        x=[col.replace('well_', '') for col in correlation_matrix.columns],
                        y=[col.replace('well_', '') for col in correlation_matrix.index],
                        colorscale='RdBu',
                        zmid=0,
                        showscale=False
                    ),
                    row=2, col=1
                )
        
        # 4. Hypothesis testing results
        if 'hypothesis_testing' in statistical_results:
            h1_results = statistical_results['hypothesis_testing'].get('H1_discriminative_validity', {})
            if h1_results.get('tests_performed'):
                comparisons = [test.get('comparison', f'Test {i}') for i, test in enumerate(h1_results['tests_performed'])]
                p_values = [test.get('p_value', 1.0) for test in h1_results['tests_performed']]
                
                fig.add_trace(
                    go.Bar(
                        x=comparisons,
                        y=p_values,
                        name='p-values',
                        showlegend=False
                    ),
                    row=2, col=2
                )
                
                # Add significance line
                fig.add_hline(y=0.05, line_dash="dash", line_color="red", 
                            annotation_text="α = 0.05", row=2, col=2)
        
        # Update layout
        fig.update_layout(
            title_text="Narrative Gravity Analysis Dashboard",
            title_x=0.5,
            height=800,
            showlegend=False
        )
        
        # Save interactive plot
        plot_file = self.output_dir / 'interactive_dashboard.html'
        fig.write_html(plot_file)
        
        plots['interactive_dashboard'] = str(plot_file)
        self.generated_files['interactive_dashboard'] = str(plot_file)
        
        return plots
    
    def save_visualization_index(self) -> str:
        """Create an index file listing all generated visualizations."""
        
        index_content = {
            'generation_timestamp': pd.Timestamp.now().isoformat(),
            'total_files': len(self.generated_files),
            'visualizations': self.generated_files,
            'descriptions': {
                'descriptive_analysis': 'Box plots, violin plots, and mean comparisons of well scores',
                'hypothesis_testing': 'Visual summaries of statistical hypothesis testing results',
                'reliability_analysis': 'ICC values and coefficient of variation analysis',
                'correlation_matrix': 'Correlation heatmap between all well scores',
                'score_distributions': 'Histograms showing distribution of each well score',
                'narrative_gravity_map': 'Scatter plot of narrative positioning coordinates',
                'well_scores_radar': 'Radar chart comparing mean well scores',
                'interactive_dashboard': 'Interactive Plotly dashboard with multiple views'
            }
        }
        
        index_file = self.output_dir / 'visualization_index.json'
        with open(index_file, 'w') as f:
            json.dump(index_content, f, indent=2)
        
        logger.info(f"📋 Visualization index saved to: {index_file}")
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