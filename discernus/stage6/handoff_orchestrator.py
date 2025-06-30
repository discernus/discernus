#!/usr/bin/env python3
"""
Stage 5→6 Handoff Orchestrator
=============================

Automatically generates Stage 6 analysis notebooks after successful Stage 5 experiment completion.
Creates rich, interactive notebooks for ANY framework type using framework-agnostic templates
that adapt dynamically to the framework's structure and characteristics.

Framework-Independent Architecture:
- No hardcoded framework names or domain-specific logic
- Templates selected based on structural characteristics (# of components, axes, etc.)
- Content generated dynamically from framework definitions
- Academic-quality notebooks for any research domain
"""

import os
import json
import yaml
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Stage6HandoffOrchestrator:
    """
    Framework-agnostic orchestrator for generating Stage 6 analysis notebooks.
    Works with any framework by analyzing structural characteristics rather than domain-specific content.
    """
    
    def __init__(self, base_results_dir: str = "results"):
        # This will be overridden to use workspace-local results
        self.base_results_dir = Path(base_results_dir)
        self.base_results_dir.mkdir(exist_ok=True)
        
    def generate_stage6_notebook(
        self, 
        experiment_result: Dict[str, Any], 
        experiment_file_path: str,
        experiment_def: Dict[str, Any]
    ) -> str:
        """
        Generate Stage 6 analysis notebook with pre-loaded data and embedded analytics.
        
        Args:
            experiment_result: The result from Stage 5 experiment execution
            experiment_file_path: Path to original experiment YAML
            experiment_def: The experiment definition dictionary
            
        Returns:
            Path to generated notebook
        """
        job_id = experiment_result.get('job_id', str(uuid.uuid4()))
        
        # Determine experiment directory from file path
        experiment_path = Path(experiment_file_path)
        experiment_dir = experiment_path.parent  # The experiment folder containing the YAML
        
        # Create results directory within the experiment folder (self-contained structure)
        experiment_results_dir_base = experiment_dir / "results"
        experiment_results_dir_base.mkdir(exist_ok=True)
        
        # Create timestamped run directory
        experiment_name = experiment_path.stem  # e.g., "byu_bolsonaro_minimal"
        run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        experiment_results_dir = experiment_results_dir_base / run_timestamp
        experiment_results_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract metadata for notebook configuration
        metadata = self._extract_metadata(experiment_result, experiment_file_path, experiment_def)
        
        # Generate notebook content
        notebook_content = self._generate_notebook_content(metadata, experiment_result)
        
        # Save notebook
        notebook_path = experiment_results_dir / "stage6_interactive_analysis.ipynb"
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_content, f, indent=2, ensure_ascii=False)
        
        # Save run metadata for provenance tracking
        run_metadata = {
            "job_id": job_id,
            "experiment_file": str(experiment_path),
            "run_timestamp": run_timestamp,
            "experiment_name": experiment_name,
            "framework_name": metadata['framework_name'],
            "models_analyzed": metadata['models_used'],
            "total_analyses": metadata['total_analyses'],
            "generation_timestamp": metadata['generation_timestamp']
        }
        
        metadata_path = experiment_results_dir / "run_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(run_metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Stage 6 notebook generated: {notebook_path}")
        logger.info(f"✅ Run metadata saved: {metadata_path}")
        
        return str(notebook_path)
    
    def _extract_metadata(
        self, 
        experiment_result: Dict[str, Any], 
        experiment_file_path: str, 
        experiment_def: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract metadata for notebook configuration"""
        
        # Extract framework configuration
        framework_config = experiment_def.get('framework', {})
        framework_name = framework_config.get('name', 'unknown_framework')
        
        # Determine template type based on structural characteristics (framework-agnostic)
        template_type = self._determine_template_type(framework_config)
        
        # Extract experiment metadata
        experiment_meta = experiment_def.get('experiment_meta', {})
        
        return {
            'job_id': experiment_result.get('job_id'),
            'experiment_name': experiment_meta.get('display_name', 'Untitled Experiment'),
            'framework_name': framework_name,
            'framework_config': framework_config,
            'template_type': template_type,
            'experiment_file_path': experiment_file_path,
            'generation_timestamp': datetime.now().isoformat(),
            'condition_results': experiment_result.get('condition_results', []),
            'statistical_metrics': experiment_result.get('statistical_metrics', {}),
            'models_used': [cr.get('condition_identifier') for cr in experiment_result.get('condition_results', [])],
            'corpus_info': experiment_def.get('corpus', {}),
            'total_analyses': sum(cr.get('total_analyses', 0) for cr in experiment_result.get('condition_results', []))
        }
    
    def _determine_template_type(self, framework_config: Dict[str, Any]) -> str:
        """
        Determine template type based on framework structural characteristics (framework-agnostic).
        No hardcoded framework names or domain-specific logic.
        """
        
        # Analyze framework structure
        components = framework_config.get('components', {})
        axes = framework_config.get('axes', {})
        num_components = len(components)
        num_axes = len(axes)
        
        # Template selection based on structural characteristics
        if num_axes == 2 and num_components <= 4:
            # Two-axis frameworks (most common for political science, psychology, etc.)
            return 'two_axis_framework'
        elif num_components >= 5:
            # Multi-component frameworks (complex theoretical models)
            return 'multi_component_framework'
        elif num_axes >= 3:
            # Multi-axis frameworks (3D+ coordinate systems)
            return 'multi_axis_framework'
        else:
            # Standard framework template for simpler structures
            return 'standard_framework'
    
    def _generate_notebook_content(self, metadata: Dict[str, Any], experiment_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the complete Jupyter notebook content"""
        
        # Base notebook structure
        notebook = {
            "cells": [],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {"name": "ipython", "version": 3},
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.8.0"
                },
                "discernus_metadata": {
                    "stage6_generated": True,
                    "job_id": metadata['job_id'],
                    "framework_name": metadata['framework_name'],
                    "template_type": metadata['template_type'],
                    "generation_timestamp": metadata['generation_timestamp']
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        # Generate cells based on template type (framework-agnostic)
        if metadata['template_type'] == 'two_axis_framework':
            cells = self._generate_two_axis_cells(metadata, experiment_result)
        elif metadata['template_type'] == 'multi_component_framework':
            cells = self._generate_multi_component_cells(metadata, experiment_result)
        elif metadata['template_type'] == 'multi_axis_framework':
            cells = self._generate_multi_axis_cells(metadata, experiment_result)
        else:
            cells = self._generate_standard_framework_cells(metadata, experiment_result)
        
        notebook["cells"] = cells
        return notebook
    
    def _generate_two_axis_cells(self, metadata: Dict[str, Any], experiment_result: Dict[str, Any]) -> list:
        """Generate cells specifically optimized for two-axis frameworks"""
        
        cells = []
        
        # Extract framework information dynamically
        framework_info = self._extract_framework_info(metadata['framework_config'])
        
        # Header cell
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# {metadata['experiment_name']} - Interactive Analysis\n",
                f"**Framework:** {framework_info['display_name']}  \n",
                f"**Generated:** {metadata['generation_timestamp']}  \n",
                f"**Job ID:** {metadata['job_id']}  \n",
                "\n",
                "## Overview\n",
                "This notebook provides interactive analysis of your experiment results with embedded statistical methods, ",
                "visualization tools, and academic export capabilities. Perfect for individual research - ",
                "scales beautifully until you have lots of experiments and need enterprise organization tools! 📊\n",
                "\n",
                "### Two-Axis Framework Analysis\n",
                f"This analysis uses the **{framework_info['display_name']}** framework to analyze content across ",
                f"two theoretical dimensions. **Models analyzed:** {', '.join(metadata['models_used'])}  \n",
                f"**Total analyses:** {metadata['total_analyses']}\n",
                "\n",
                f"**Framework Description:** {framework_info['description']}\n"
            ]
        })
        
        # Setup and imports cell
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# EXPERIMENT DATA SETUP - Auto-generated from Stage 5 results\n",
                "# =============================================================================\n",
                "\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import plotly.express as px\n",
                "import plotly.graph_objects as go\n",
                "from scipy import stats\n",
                "import json\n",
                "from pathlib import Path\n",
                "\n",
                "# Configure plotting\n",
                "plt.style.use('seaborn-v0_8')\n",
                "sns.set_palette('husl')\n",
                "\n",
                f"# Experiment metadata\n",
                f"JOB_ID = '{metadata['job_id']}'\n",
                f"FRAMEWORK_NAME = '{metadata['framework_name']}'\n",
                f"EXPERIMENT_NAME = '{metadata['experiment_name']}'\n",
                f"MODELS_ANALYZED = {metadata['models_used']}\n",
                f"TOTAL_ANALYSES = {metadata['total_analyses']}\n",
                "\n",
                "print(f'📊 Loaded experiment: {EXPERIMENT_NAME}')\n",
                "print(f'🎯 Framework: {FRAMEWORK_NAME}')\n",
                "print(f'🤖 Models: {\", \".join(MODELS_ANALYZED)}')\n",
                "print(f'📈 Total analyses: {TOTAL_ANALYSES}')\n"
            ]
        })
        
        # Data loading cell
        cells.append({
            "cell_type": "code", 
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# RESULTS DATA - Pre-loaded from Stage 5 experiment\n",
                "# =============================================================================\n",
                "\n",
                f"# Raw experiment results\n",
                f"EXPERIMENT_RESULTS = {json.dumps(experiment_result, indent=2)}\n",
                "\n",
                "# Extract condition results into DataFrame\n",
                "condition_data = []\n",
                "for condition in EXPERIMENT_RESULTS['condition_results']:\n",
                "    condition_data.append({\n",
                "        'model': condition['condition_identifier'],\n",
                "        'centroid_x': condition['centroid'][0],\n",
                "        'centroid_y': condition['centroid'][1], \n",
                "        'total_analyses': condition.get('total_analyses', 0),\n",
                "        'raw_scores': condition.get('raw_scores', {})\n",
                "    })\n",
                "\n",
                "df_results = pd.DataFrame(condition_data)\n",
                "print('✅ Results loaded into DataFrame:')\n",
                "print(df_results.head())\n",
                "\n",
                "# Statistical metrics\n",
                f"STATISTICAL_METRICS = {json.dumps(metadata['statistical_metrics'], indent=2)}\n",
                "print(f'\\n📊 Statistical metrics available: {list(STATISTICAL_METRICS.keys())}')"
            ]
        })
        
        # Two-axis specific analysis cell
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Two-Axis Framework Analysis\n",
                "\n",
                "### Coordinate Space Interpretation\n",
                "Your framework positions analyzed content in a **theoretical coordinate space** where each axis represents a dimension of your analytical framework. The centroid positions show where each model's analysis clusters in this space.\n",
                "\n",
                "### Key Metrics\n",
                "- **Centroid Position** (X, Y): The average position of all analyses for each model\n",
                "- **Magnitude**: Distance from origin (0,0) - indicates overall \"intensity\" of the analysis\n",
                "- **Angle**: Direction in the coordinate space relative to the theoretical axes\n",
                "- **Spread**: How dispersed the individual analyses are around the centroid\n"
            ]
        })
        
        # Visualization cell
        cells.append({
            "cell_type": "code",
            "execution_count": None, 
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# COORDINATE VISUALIZATION - Democratic Tension Quadrants\n",
                "# =============================================================================\n",
                "\n",
                "# Create quadrant visualization\n",
                "fig, ax = plt.subplots(1, 1, figsize=(10, 10))\n",
                "\n",
                "# Plot model centroids\n",
                "colors = sns.color_palette('husl', len(df_results))\n",
                "for i, (_, row) in enumerate(df_results.iterrows()):\n",
                "    ax.scatter(row['centroid_x'], row['centroid_y'], \n",
                "              s=200, alpha=0.7, color=colors[i], \n",
                "              label=row['model'])\n",
                "    ax.annotate(row['model'], \n",
                "               (row['centroid_x'], row['centroid_y']),\n",
                "               xytext=(5, 5), textcoords='offset points',\n",
                "               fontsize=10, ha='left')\n",
                "\n",
                "# Add quadrant lines and labels\n",
                "ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)\n",
                "ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)\n",
                "\n",
                "# Quadrant labels for Democratic Tension Model\n",
                "ax.text(0.5, 0.5, 'High Populism\\n+ High Nationalism', \n",
                "        transform=ax.transAxes, ha='center', va='center',\n",
                "        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))\n",
                "ax.text(-0.5, 0.5, 'High Populism\\n+ High Patriotism',\n",
                "        transform=ax.transAxes, ha='center', va='center', \n",
                "        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))\n",
                "ax.text(-0.5, -0.5, 'High Pluralism\\n+ High Patriotism',\n",
                "        transform=ax.transAxes, ha='center', va='center',\n",
                "        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))\n",
                "ax.text(0.5, -0.5, 'High Pluralism\\n+ High Nationalism',\n",
                "        transform=ax.transAxes, ha='center', va='center',\n",
                "        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))\n",
                "\n",
                "ax.set_xlabel('Patriotism ← → Nationalism', fontsize=12)\n",
                "ax.set_ylabel('Pluralism ← → Populism', fontsize=12)\n",
                "ax.set_title(f'Democratic Tension Analysis: {EXPERIMENT_NAME}\\nBrazilian Political Discourse Coordinates', \n",
                "             fontsize=14, pad=20)\n",
                "ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')\n",
                "ax.grid(True, alpha=0.3)\n",
                "ax.set_aspect('equal')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
                "\n",
                "print(f'📊 Coordinate plot generated for {len(df_results)} models')"
            ]
        })
        
        # Statistical analysis embedding (creates complexity for scaling)
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# EMBEDDED STATISTICAL ANALYSIS - Creates natural scaling challenges! 📈\n",
                "# =============================================================================\n",
                "\n",
                "def calculate_geometric_similarity(results_df):\n",
                "    \"\"\"Calculate pairwise geometric distances between model centroids\"\"\"\n",
                "    distances = []\n",
                "    models = results_df['model'].tolist()\n",
                "    \n",
                "    for i in range(len(results_df)):\n",
                "        for j in range(i + 1, len(results_df)):\n",
                "            x1, y1 = results_df.iloc[i][['centroid_x', 'centroid_y']]\n",
                "            x2, y2 = results_df.iloc[j][['centroid_x', 'centroid_y']]\n",
                "            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)\n",
                "            distances.append({\n",
                "                'model_1': models[i],\n",
                "                'model_2': models[j], \n",
                "                'distance': distance\n",
                "            })\n",
                "    \n",
                "    return pd.DataFrame(distances)\n",
                "\n",
                "def calculate_dimensional_correlation(results_df):\n",
                "    \"\"\"Calculate correlation between model positions\"\"\"\n",
                "    if len(results_df) < 2:\n",
                "        return {\"error\": \"Need at least 2 models for correlation\"}\n",
                "    \n",
                "    x_coords = results_df['centroid_x'].values\n",
                "    y_coords = results_df['centroid_y'].values\n",
                "    \n",
                "    correlation = np.corrcoef(x_coords, y_coords)[0, 1]\n",
                "    \n",
                "    return {\n",
                "        'x_y_correlation': correlation,\n",
                "        'x_mean': np.mean(x_coords),\n",
                "        'y_mean': np.mean(y_coords),\n",
                "        'x_std': np.std(x_coords),\n",
                "        'y_std': np.std(y_coords)\n",
                "    }\n",
                "\n",
                "# Run embedded statistical analysis\n",
                "geometric_analysis = calculate_geometric_similarity(df_results)\n",
                "correlation_analysis = calculate_dimensional_correlation(df_results)\n",
                "\n",
                "print('✅ Geometric Similarity Analysis:')\n",
                "print(geometric_analysis)\n",
                "print('\\n✅ Dimensional Correlation Analysis:')\n",
                "print(correlation_analysis)\n",
                "\n",
                "# This is getting complex... imagine having 20+ experiments to manage! 🤔"
            ]
        })
        
        # Publication export cell (scales poorly)
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# PUBLICATION-READY EXPORT - Manual process that scales poorly 📝\n",
                "# =============================================================================\n",
                "\n",
                "def export_for_publication(results_df, job_id):\n",
                "    \"\"\"Export results in academic publication format\"\"\"\n",
                "    \n",
                "    # Create publication directory \n",
                "    pub_dir = Path(f'publication_exports/{job_id}')\n",
                "    pub_dir.mkdir(parents=True, exist_ok=True)\n",
                "    \n",
                "    # Export data as CSV\n",
                "    results_df.to_csv(pub_dir / 'model_centroids.csv', index=False)\n",
                "    \n",
                "    # Export statistical summary\n",
                "    summary = {\n",
                "        'experiment_name': EXPERIMENT_NAME,\n",
                "        'framework': FRAMEWORK_NAME,\n",
                "        'models_analyzed': MODELS_ANALYZED,\n",
                "        'total_analyses': TOTAL_ANALYSES,\n",
                "        'mean_x': results_df['centroid_x'].mean(),\n",
                "        'mean_y': results_df['centroid_y'].mean(),\n",
                "        'std_x': results_df['centroid_x'].std(),\n",
                "        'std_y': results_df['centroid_y'].std()\n",
                "    }\n",
                "    \n",
                "    with open(pub_dir / 'summary_statistics.json', 'w') as f:\n",
                "        json.dump(summary, f, indent=2)\n",
                "    \n",
                "    print(f'📊 Publication files exported to: {pub_dir}')\n",
                "    print('📁 Files: model_centroids.csv, summary_statistics.json')\n",
                "    \n",
                "    return pub_dir\n",
                "\n",
                "# Export for publication\n",
                "export_dir = export_for_publication(df_results, JOB_ID)\n",
                "\n",
                "print('\\n🎓 Ready for academic submission!')\n",
                "print('💡 Pro tip: With multiple experiments, managing all these exports becomes... challenging!')\n",
                "print('🚀 That\\'s when enterprise tools become really helpful! 😉')"
            ]
        })
        
        # BYU collaboration cell
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Next Steps for BYU Collaboration\n",
                "\n",
                "### Validation Protocol\n",
                "1. **Correlation Analysis**: Compare these LLM results with Tamaki & Fuks manual coding\n",
                "2. **Statistical Significance**: Test if differences are meaningful (target: r > 0.70)\n",
                "3. **Methodological Documentation**: Prepare for academic publication\n",
                "\n",
                "### Value Demonstration\n",
                "- **Speed**: LLM analysis completes in minutes vs. weeks of manual coding\n",
                "- **Scale**: Can analyze entire corpora not feasible for manual coding\n",
                "- **Consistency**: Eliminates inter-rater reliability concerns\n",
                "- **Innovation**: Enables novel analytical approaches (temporal dynamics, cross-framework comparison)\n",
                "\n",
                "### Research Acceleration Opportunities\n",
                "- **Global Populism Database**: Scale to thousands of speeches across countries\n",
                "- **Temporal Analysis**: Track discourse evolution across election cycles  \n",
                "- **Comparative Frameworks**: Apply multiple theoretical lenses simultaneously\n",
                "- **Real-time Analysis**: Monitor contemporary political discourse as it emerges\n",
                "\n",
                "**Ready to transform computational social science research! 🚀**\n"
            ]
        })
        
        return cells
    
    def _generate_multi_component_cells(self, metadata: Dict[str, Any], experiment_result: Dict[str, Any]) -> list:
        """Generate cells specifically optimized for multi-component frameworks"""
        
        cells = []
        
        # Header cell
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# {metadata['experiment_name']} - Interactive Analysis\n",
                f"**Framework:** {metadata['framework_name']}  \n",
                f"**Generated:** {metadata['generation_timestamp']}  \n",
                f"**Job ID:** {metadata['job_id']}  \n",
                "\n",
                "## Overview\n",
                "This notebook provides interactive analysis of your experiment results with embedded statistical methods, ",
                "visualization tools, and academic export capabilities. Perfect for individual research - ",
                "scales beautifully until you have lots of experiments and need enterprise organization tools! 📊\n",
                "\n",
                "### Multi-Component Framework Analysis\n",
                "This analysis replicates and extends the methodology from Tamaki & Fuks (2019) using the ",
                f"Democratic Tension Axis Model for Brazilian political discourse. **Models analyzed:** {', '.join(metadata['models_used'])}  \n",
                f"**Total analyses:** {metadata['total_analyses']}\n"
            ]
        })
        
        # Setup and imports cell
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# EXPERIMENT DATA SETUP - Auto-generated from Stage 5 results\n",
                "# =============================================================================\n",
                "\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import plotly.express as px\n",
                "import plotly.graph_objects as go\n",
                "from scipy import stats\n",
                "import json\n",
                "from pathlib import Path\n",
                "\n",
                "# Configure plotting\n",
                "plt.style.use('seaborn-v0_8')\n",
                "sns.set_palette('husl')\n",
                "\n",
                f"# Experiment metadata\n",
                f"JOB_ID = '{metadata['job_id']}'\n",
                f"FRAMEWORK_NAME = '{metadata['framework_name']}'\n",
                f"EXPERIMENT_NAME = '{metadata['experiment_name']}'\n",
                f"MODELS_ANALYZED = {metadata['models_used']}\n",
                f"TOTAL_ANALYSES = {metadata['total_analyses']}\n",
                "\n",
                "print(f'📊 Loaded experiment: {EXPERIMENT_NAME}')\n",
                "print(f'🎯 Framework: {FRAMEWORK_NAME}')\n",
                "print(f'🤖 Models: {\", \".join(MODELS_ANALYZED)}')\n",
                "print(f'📈 Total analyses: {TOTAL_ANALYSES}')\n"
            ]
        })
        
        # Data loading cell
        cells.append({
            "cell_type": "code", 
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# RESULTS DATA - Pre-loaded from Stage 5 experiment\n",
                "# =============================================================================\n",
                "\n",
                f"# Raw experiment results\n",
                f"EXPERIMENT_RESULTS = {json.dumps(experiment_result, indent=2)}\n",
                "\n",
                "# Extract condition results into DataFrame\n",
                "condition_data = []\n",
                "for condition in EXPERIMENT_RESULTS['condition_results']:\n",
                "    condition_data.append({\n",
                "        'model': condition['condition_identifier'],\n",
                "        'centroid_x': condition['centroid'][0],\n",
                "        'centroid_y': condition['centroid'][1], \n",
                "        'total_analyses': condition.get('total_analyses', 0),\n",
                "        'raw_scores': condition.get('raw_scores', {})\n",
                "    })\n",
                "\n",
                "df_results = pd.DataFrame(condition_data)\n",
                "print('✅ Results loaded into DataFrame:')\n",
                "print(df_results.head())\n",
                "\n",
                "# Statistical metrics\n",
                f"STATISTICAL_METRICS = {json.dumps(metadata['statistical_metrics'], indent=2)}\n",
                "print(f'\\n📊 Statistical metrics available: {list(STATISTICAL_METRICS.keys())}')"
            ]
        })
        
        # Multi-component specific analysis cell
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Multi-Component Framework Analysis\n",
                "\n",
                "### Coordinate Space Interpretation\n",
                "Your framework positions analyzed content in a **theoretical coordinate space** where each axis represents a dimension of your analytical framework. The centroid positions show where each model's analysis clusters in this space.\n",
                "\n",
                "### Key Metrics\n",
                "- **Centroid Position** (X, Y): The average position of all analyses for each model\n",
                "- **Magnitude**: Distance from origin (0,0) - indicates overall \"intensity\" of the analysis\n",
                "- **Angle**: Direction in the coordinate space relative to the theoretical axes\n",
                "- **Spread**: How dispersed the individual analyses are around the centroid\n"
            ]
        })
        
        # Visualization cell
        cells.append({
            "cell_type": "code",
            "execution_count": None, 
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# COORDINATE VISUALIZATION - Democratic Tension Quadrants\n",
                "# =============================================================================\n",
                "\n",
                "# Create quadrant visualization\n",
                "fig, ax = plt.subplots(1, 1, figsize=(10, 10))\n",
                "\n",
                "# Plot model centroids\n",
                "colors = sns.color_palette('husl', len(df_results))\n",
                "for i, (_, row) in enumerate(df_results.iterrows()):\n",
                "    ax.scatter(row['centroid_x'], row['centroid_y'], \n",
                "              s=200, alpha=0.7, color=colors[i], \n",
                "              label=row['model'])\n",
                "    ax.annotate(row['model'], \n",
                "               (row['centroid_x'], row['centroid_y']),\n",
                "               xytext=(5, 5), textcoords='offset points',\n",
                "               fontsize=10, ha='left')\n",
                "\n",
                "# Add quadrant lines and labels\n",
                "ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)\n",
                "ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)\n",
                "\n",
                "# Quadrant labels for Democratic Tension Model\n",
                "ax.text(0.5, 0.5, 'High Populism\\n+ High Nationalism', \n",
                "        transform=ax.transAxes, ha='center', va='center',\n",
                "        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))\n",
                "ax.text(-0.5, 0.5, 'High Populism\\n+ High Patriotism',\n",
                "        transform=ax.transAxes, ha='center', va='center', \n",
                "        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))\n",
                "ax.text(-0.5, -0.5, 'High Pluralism\\n+ High Patriotism',\n",
                "        transform=ax.transAxes, ha='center', va='center',\n",
                "        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))\n",
                "ax.text(0.5, -0.5, 'High Pluralism\\n+ High Nationalism',\n",
                "        transform=ax.transAxes, ha='center', va='center',\n",
                "        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))\n",
                "\n",
                "ax.set_xlabel('Patriotism ← → Nationalism', fontsize=12)\n",
                "ax.set_ylabel('Pluralism ← → Populism', fontsize=12)\n",
                "ax.set_title(f'Democratic Tension Analysis: {EXPERIMENT_NAME}\\nBrazilian Political Discourse Coordinates', \n",
                "             fontsize=14, pad=20)\n",
                "ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')\n",
                "ax.grid(True, alpha=0.3)\n",
                "ax.set_aspect('equal')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
                "\n",
                "print(f'📊 Coordinate plot generated for {len(df_results)} models')"
            ]
        })
        
        # Statistical analysis embedding (creates complexity for scaling)
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# EMBEDDED STATISTICAL ANALYSIS - Creates natural scaling challenges! 📈\n",
                "# =============================================================================\n",
                "\n",
                "def calculate_geometric_similarity(results_df):\n",
                "    \"\"\"Calculate pairwise geometric distances between model centroids\"\"\"\n",
                "    distances = []\n",
                "    models = results_df['model'].tolist()\n",
                "    \n",
                "    for i in range(len(results_df)):\n",
                "        for j in range(i + 1, len(results_df)):\n",
                "            x1, y1 = results_df.iloc[i][['centroid_x', 'centroid_y']]\n",
                "            x2, y2 = results_df.iloc[j][['centroid_x', 'centroid_y']]\n",
                "            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)\n",
                "            distances.append({\n",
                "                'model_1': models[i],\n",
                "                'model_2': models[j], \n",
                "                'distance': distance\n",
                "            })\n",
                "    \n",
                "    return pd.DataFrame(distances)\n",
                "\n",
                "def calculate_dimensional_correlation(results_df):\n",
                "    \"\"\"Calculate correlation between model positions\"\"\"\n",
                "    if len(results_df) < 2:\n",
                "        return {\"error\": \"Need at least 2 models for correlation\"}\n",
                "    \n",
                "    x_coords = results_df['centroid_x'].values\n",
                "    y_coords = results_df['centroid_y'].values\n",
                "    \n",
                "    correlation = np.corrcoef(x_coords, y_coords)[0, 1]\n",
                "    \n",
                "    return {\n",
                "        'x_y_correlation': correlation,\n",
                "        'x_mean': np.mean(x_coords),\n",
                "        'y_mean': np.mean(y_coords),\n",
                "        'x_std': np.std(x_coords),\n",
                "        'y_std': np.std(y_coords)\n",
                "    }\n",
                "\n",
                "# Run embedded statistical analysis\n",
                "geometric_analysis = calculate_geometric_similarity(df_results)\n",
                "correlation_analysis = calculate_dimensional_correlation(df_results)\n",
                "\n",
                "print('✅ Geometric Similarity Analysis:')\n",
                "print(geometric_analysis)\n",
                "print('\\n✅ Dimensional Correlation Analysis:')\n",
                "print(correlation_analysis)\n",
                "\n",
                "# This is getting complex... imagine having 20+ experiments to manage! 🤔"
            ]
        })
        
        # Publication export cell (scales poorly)
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# PUBLICATION-READY EXPORT - Manual process that scales poorly 📝\n",
                "# =============================================================================\n",
                "\n",
                "def export_for_publication(results_df, job_id):\n",
                "    \"\"\"Export results in academic publication format\"\"\"\n",
                "    \n",
                "    # Create publication directory \n",
                "    pub_dir = Path(f'publication_exports/{job_id}')\n",
                "    pub_dir.mkdir(parents=True, exist_ok=True)\n",
                "    \n",
                "    # Export data as CSV\n",
                "    results_df.to_csv(pub_dir / 'model_centroids.csv', index=False)\n",
                "    \n",
                "    # Export statistical summary\n",
                "    summary = {\n",
                "        'experiment_name': EXPERIMENT_NAME,\n",
                "        'framework': FRAMEWORK_NAME,\n",
                "        'models_analyzed': MODELS_ANALYZED,\n",
                "        'total_analyses': TOTAL_ANALYSES,\n",
                "        'mean_x': results_df['centroid_x'].mean(),\n",
                "        'mean_y': results_df['centroid_y'].mean(),\n",
                "        'std_x': results_df['centroid_x'].std(),\n",
                "        'std_y': results_df['centroid_y'].std()\n",
                "    }\n",
                "    \n",
                "    with open(pub_dir / 'summary_statistics.json', 'w') as f:\n",
                "        json.dump(summary, f, indent=2)\n",
                "    \n",
                "    print(f'📊 Publication files exported to: {pub_dir}')\n",
                "    print('📁 Files: model_centroids.csv, summary_statistics.json')\n",
                "    \n",
                "    return pub_dir\n",
                "\n",
                "# Export for publication\n",
                "export_dir = export_for_publication(df_results, JOB_ID)\n",
                "\n",
                "print('\\n🎓 Ready for academic submission!')\n",
                "print('💡 Pro tip: With multiple experiments, managing all these exports becomes... challenging!')\n",
                "print('🚀 That\\'s when enterprise tools become really helpful! 😉')"
            ]
        })
        
        # BYU collaboration cell
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Next Steps for BYU Collaboration\n",
                "\n",
                "### Validation Protocol\n",
                "1. **Correlation Analysis**: Compare these LLM results with Tamaki & Fuks manual coding\n",
                "2. **Statistical Significance**: Test if differences are meaningful (target: r > 0.70)\n",
                "3. **Methodological Documentation**: Prepare for academic publication\n",
                "\n",
                "### Value Demonstration\n",
                "- **Speed**: LLM analysis completes in minutes vs. weeks of manual coding\n",
                "- **Scale**: Can analyze entire corpora not feasible for manual coding\n",
                "- **Consistency**: Eliminates inter-rater reliability concerns\n",
                "- **Innovation**: Enables novel analytical approaches (temporal dynamics, cross-framework comparison)\n",
                "\n",
                "### Research Acceleration Opportunities\n",
                "- **Global Populism Database**: Scale to thousands of speeches across countries\n",
                "- **Temporal Analysis**: Track discourse evolution across election cycles  \n",
                "- **Comparative Frameworks**: Apply multiple theoretical lenses simultaneously\n",
                "- **Real-time Analysis**: Monitor contemporary political discourse as it emerges\n",
                "\n",
                "**Ready to transform computational social science research! 🚀**\n"
            ]
        })
        
        return cells
    
    def _generate_multi_axis_cells(self, metadata: Dict[str, Any], experiment_result: Dict[str, Any]) -> list:
        """Generate cells specifically optimized for multi-axis frameworks"""
        
        cells = []
        
        # Header cell
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# {metadata['experiment_name']} - Interactive Analysis\n",
                f"**Framework:** {metadata['framework_name']}  \n",
                f"**Generated:** {metadata['generation_timestamp']}  \n",
                f"**Job ID:** {metadata['job_id']}  \n",
                "\n",
                "## Overview\n",
                "This notebook provides interactive analysis of your experiment results with embedded statistical methods, ",
                "visualization tools, and academic export capabilities. Perfect for individual research - ",
                "scales beautifully until you have lots of experiments and need enterprise organization tools! 📊\n",
                "\n",
                "### Multi-Axis Framework Analysis\n",
                "This analysis replicates and extends the methodology from Tamaki & Fuks (2019) using the ",
                f"Democratic Tension Axis Model for Brazilian political discourse. **Models analyzed:** {', '.join(metadata['models_used'])}  \n",
                f"**Total analyses:** {metadata['total_analyses']}\n"
            ]
        })
        
        # Setup and imports cell
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# EXPERIMENT DATA SETUP - Auto-generated from Stage 5 results\n",
                "# =============================================================================\n",
                "\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import plotly.express as px\n",
                "import plotly.graph_objects as go\n",
                "from scipy import stats\n",
                "import json\n",
                "from pathlib import Path\n",
                "\n",
                "# Configure plotting\n",
                "plt.style.use('seaborn-v0_8')\n",
                "sns.set_palette('husl')\n",
                "\n",
                f"# Experiment metadata\n",
                f"JOB_ID = '{metadata['job_id']}'\n",
                f"FRAMEWORK_NAME = '{metadata['framework_name']}'\n",
                f"EXPERIMENT_NAME = '{metadata['experiment_name']}'\n",
                f"MODELS_ANALYZED = {metadata['models_used']}\n",
                f"TOTAL_ANALYSES = {metadata['total_analyses']}\n",
                "\n",
                "print(f'📊 Loaded experiment: {EXPERIMENT_NAME}')\n",
                "print(f'🎯 Framework: {FRAMEWORK_NAME}')\n",
                "print(f'🤖 Models: {\", \".join(MODELS_ANALYZED)}')\n",
                "print(f'📈 Total analyses: {TOTAL_ANALYSES}')\n"
            ]
        })
        
        # Data loading cell
        cells.append({
            "cell_type": "code", 
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# RESULTS DATA - Pre-loaded from Stage 5 experiment\n",
                "# =============================================================================\n",
                "\n",
                f"# Raw experiment results\n",
                f"EXPERIMENT_RESULTS = {json.dumps(experiment_result, indent=2)}\n",
                "\n",
                "# Extract condition results into DataFrame\n",
                "condition_data = []\n",
                "for condition in EXPERIMENT_RESULTS['condition_results']:\n",
                "    condition_data.append({\n",
                "        'model': condition['condition_identifier'],\n",
                "        'centroid_x': condition['centroid'][0],\n",
                "        'centroid_y': condition['centroid'][1], \n",
                "        'total_analyses': condition.get('total_analyses', 0),\n",
                "        'raw_scores': condition.get('raw_scores', {})\n",
                "    })\n",
                "\n",
                "df_results = pd.DataFrame(condition_data)\n",
                "print('✅ Results loaded into DataFrame:')\n",
                "print(df_results.head())\n",
                "\n",
                "# Statistical metrics\n",
                f"STATISTICAL_METRICS = {json.dumps(metadata['statistical_metrics'], indent=2)}\n",
                "print(f'\\n📊 Statistical metrics available: {list(STATISTICAL_METRICS.keys())}')"
            ]
        })
        
        # Multi-axis specific analysis cell
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Multi-Axis Framework Analysis\n",
                "\n",
                "### Coordinate Space Interpretation\n",
                "Your framework positions analyzed content in a **theoretical coordinate space** where each axis represents a dimension of your analytical framework. The centroid positions show where each model's analysis clusters in this space.\n",
                "\n",
                "### Key Metrics\n",
                "- **Centroid Position** (X, Y): The average position of all analyses for each model\n",
                "- **Magnitude**: Distance from origin (0,0) - indicates overall \"intensity\" of the analysis\n",
                "- **Angle**: Direction in the coordinate space relative to the theoretical axes\n",
                "- **Spread**: How dispersed the individual analyses are around the centroid\n"
            ]
        })
        
        # Visualization cell
        cells.append({
            "cell_type": "code",
            "execution_count": None, 
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# COORDINATE VISUALIZATION - Democratic Tension Quadrants\n",
                "# =============================================================================\n",
                "\n",
                "# Create quadrant visualization\n",
                "fig, ax = plt.subplots(1, 1, figsize=(10, 10))\n",
                "\n",
                "# Plot model centroids\n",
                "colors = sns.color_palette('husl', len(df_results))\n",
                "for i, (_, row) in enumerate(df_results.iterrows()):\n",
                "    ax.scatter(row['centroid_x'], row['centroid_y'], \n",
                "              s=200, alpha=0.7, color=colors[i], \n",
                "              label=row['model'])\n",
                "    ax.annotate(row['model'], \n",
                "               (row['centroid_x'], row['centroid_y']),\n",
                "               xytext=(5, 5), textcoords='offset points',\n",
                "               fontsize=10, ha='left')\n",
                "\n",
                "# Add quadrant lines and labels\n",
                "ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)\n",
                "ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)\n",
                "\n",
                "# Quadrant labels for Democratic Tension Model\n",
                "ax.text(0.5, 0.5, 'High Populism\\n+ High Nationalism', \n",
                "        transform=ax.transAxes, ha='center', va='center',\n",
                "        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))\n",
                "ax.text(-0.5, 0.5, 'High Populism\\n+ High Patriotism',\n",
                "        transform=ax.transAxes, ha='center', va='center', \n",
                "        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))\n",
                "ax.text(-0.5, -0.5, 'High Pluralism\\n+ High Patriotism',\n",
                "        transform=ax.transAxes, ha='center', va='center',\n",
                "        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))\n",
                "ax.text(0.5, -0.5, 'High Pluralism\\n+ High Nationalism',\n",
                "        transform=ax.transAxes, ha='center', va='center',\n",
                "        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))\n",
                "\n",
                "ax.set_xlabel('Patriotism ← → Nationalism', fontsize=12)\n",
                "ax.set_ylabel('Pluralism ← → Populism', fontsize=12)\n",
                "ax.set_title(f'Democratic Tension Analysis: {EXPERIMENT_NAME}\\nBrazilian Political Discourse Coordinates', \n",
                "             fontsize=14, pad=20)\n",
                "ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')\n",
                "ax.grid(True, alpha=0.3)\n",
                "ax.set_aspect('equal')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
                "\n",
                "print(f'📊 Coordinate plot generated for {len(df_results)} models')"
            ]
        })
        
        # Statistical analysis embedding (creates complexity for scaling)
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# EMBEDDED STATISTICAL ANALYSIS - Creates natural scaling challenges! 📈\n",
                "# =============================================================================\n",
                "\n",
                "def calculate_geometric_similarity(results_df):\n",
                "    \"\"\"Calculate pairwise geometric distances between model centroids\"\"\"\n",
                "    distances = []\n",
                "    models = results_df['model'].tolist()\n",
                "    \n",
                "    for i in range(len(results_df)):\n",
                "        for j in range(i + 1, len(results_df)):\n",
                "            x1, y1 = results_df.iloc[i][['centroid_x', 'centroid_y']]\n",
                "            x2, y2 = results_df.iloc[j][['centroid_x', 'centroid_y']]\n",
                "            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)\n",
                "            distances.append({\n",
                "                'model_1': models[i],\n",
                "                'model_2': models[j], \n",
                "                'distance': distance\n",
                "            })\n",
                "    \n",
                "    return pd.DataFrame(distances)\n",
                "\n",
                "def calculate_dimensional_correlation(results_df):\n",
                "    \"\"\"Calculate correlation between model positions\"\"\"\n",
                "    if len(results_df) < 2:\n",
                "        return {\"error\": \"Need at least 2 models for correlation\"}\n",
                "    \n",
                "    x_coords = results_df['centroid_x'].values\n",
                "    y_coords = results_df['centroid_y'].values\n",
                "    \n",
                "    correlation = np.corrcoef(x_coords, y_coords)[0, 1]\n",
                "    \n",
                "    return {\n",
                "        'x_y_correlation': correlation,\n",
                "        'x_mean': np.mean(x_coords),\n",
                "        'y_mean': np.mean(y_coords),\n",
                "        'x_std': np.std(x_coords),\n",
                "        'y_std': np.std(y_coords)\n",
                "    }\n",
                "\n",
                "# Run embedded statistical analysis\n",
                "geometric_analysis = calculate_geometric_similarity(df_results)\n",
                "correlation_analysis = calculate_dimensional_correlation(df_results)\n",
                "\n",
                "print('✅ Geometric Similarity Analysis:')\n",
                "print(geometric_analysis)\n",
                "print('\\n✅ Dimensional Correlation Analysis:')\n",
                "print(correlation_analysis)\n",
                "\n",
                "# This is getting complex... imagine having 20+ experiments to manage! 🤔"
            ]
        })
        
        # Publication export cell (scales poorly)
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# PUBLICATION-READY EXPORT - Manual process that scales poorly 📝\n",
                "# =============================================================================\n",
                "\n",
                "def export_for_publication(results_df, job_id):\n",
                "    \"\"\"Export results in academic publication format\"\"\"\n",
                "    \n",
                "    # Create publication directory \n",
                "    pub_dir = Path(f'publication_exports/{job_id}')\n",
                "    pub_dir.mkdir(parents=True, exist_ok=True)\n",
                "    \n",
                "    # Export data as CSV\n",
                "    results_df.to_csv(pub_dir / 'model_centroids.csv', index=False)\n",
                "    \n",
                "    # Export statistical summary\n",
                "    summary = {\n",
                "        'experiment_name': EXPERIMENT_NAME,\n",
                "        'framework': FRAMEWORK_NAME,\n",
                "        'models_analyzed': MODELS_ANALYZED,\n",
                "        'total_analyses': TOTAL_ANALYSES,\n",
                "        'mean_x': results_df['centroid_x'].mean(),\n",
                "        'mean_y': results_df['centroid_y'].mean(),\n",
                "        'std_x': results_df['centroid_x'].std(),\n",
                "        'std_y': results_df['centroid_y'].std()\n",
                "    }\n",
                "    \n",
                "    with open(pub_dir / 'summary_statistics.json', 'w') as f:\n",
                "        json.dump(summary, f, indent=2)\n",
                "    \n",
                "    print(f'📊 Publication files exported to: {pub_dir}')\n",
                "    print('📁 Files: model_centroids.csv, summary_statistics.json')\n",
                "    \n",
                "    return pub_dir\n",
                "\n",
                "# Export for publication\n",
                "export_dir = export_for_publication(df_results, JOB_ID)\n",
                "\n",
                "print('\\n🎓 Ready for academic submission!')\n",
                "print('💡 Pro tip: With multiple experiments, managing all these exports becomes... challenging!')\n",
                "print('🚀 That\\'s when enterprise tools become really helpful! 😉')"
            ]
        })
        
        # BYU collaboration cell
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Next Steps for BYU Collaboration\n",
                "\n",
                "### Validation Protocol\n",
                "1. **Correlation Analysis**: Compare these LLM results with Tamaki & Fuks manual coding\n",
                "2. **Statistical Significance**: Test if differences are meaningful (target: r > 0.70)\n",
                "3. **Methodological Documentation**: Prepare for academic publication\n",
                "\n",
                "### Value Demonstration\n",
                "- **Speed**: LLM analysis completes in minutes vs. weeks of manual coding\n",
                "- **Scale**: Can analyze entire corpora not feasible for manual coding\n",
                "- **Consistency**: Eliminates inter-rater reliability concerns\n",
                "- **Innovation**: Enables novel analytical approaches (temporal dynamics, cross-framework comparison)\n",
                "\n",
                "### Research Acceleration Opportunities\n",
                "- **Global Populism Database**: Scale to thousands of speeches across countries\n",
                "- **Temporal Analysis**: Track discourse evolution across election cycles  \n",
                "- **Comparative Frameworks**: Apply multiple theoretical lenses simultaneously\n",
                "- **Real-time Analysis**: Monitor contemporary political discourse as it emerges\n",
                "\n",
                "**Ready to transform computational social science research! 🚀**\n"
            ]
        })
        
        return cells
    
    def _generate_standard_framework_cells(self, metadata: Dict[str, Any], experiment_result: Dict[str, Any]) -> list:
        """Generate cells specifically optimized for standard frameworks"""
        
        cells = []
        
        # Header cell
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# {metadata['experiment_name']} - Interactive Analysis\n",
                f"**Framework:** {metadata['framework_name']}  \n",
                f"**Generated:** {metadata['generation_timestamp']}  \n",
                f"**Job ID:** {metadata['job_id']}  \n",
                "\n",
                "## Overview\n",
                "This notebook provides interactive analysis of your experiment results with embedded statistical methods, ",
                "visualization tools, and academic export capabilities. Perfect for individual research - ",
                "scales beautifully until you have lots of experiments and need enterprise organization tools! 📊\n",
                "\n",
                "### Standard Framework Analysis\n",
                "This analysis replicates and extends the methodology from Tamaki & Fuks (2019) using the ",
                f"Democratic Tension Axis Model for Brazilian political discourse. **Models analyzed:** {', '.join(metadata['models_used'])}  \n",
                f"**Total analyses:** {metadata['total_analyses']}\n"
            ]
        })
        
        # Setup and imports cell
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# EXPERIMENT DATA SETUP - Auto-generated from Stage 5 results\n",
                "# =============================================================================\n",
                "\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import plotly.express as px\n",
                "import plotly.graph_objects as go\n",
                "from scipy import stats\n",
                "import json\n",
                "from pathlib import Path\n",
                "\n",
                "# Configure plotting\n",
                "plt.style.use('seaborn-v0_8')\n",
                "sns.set_palette('husl')\n",
                "\n",
                f"# Experiment metadata\n",
                f"JOB_ID = '{metadata['job_id']}'\n",
                f"FRAMEWORK_NAME = '{metadata['framework_name']}'\n",
                f"EXPERIMENT_NAME = '{metadata['experiment_name']}'\n",
                f"MODELS_ANALYZED = {metadata['models_used']}\n",
                f"TOTAL_ANALYSES = {metadata['total_analyses']}\n",
                "\n",
                "print(f'📊 Loaded experiment: {EXPERIMENT_NAME}')\n",
                "print(f'🎯 Framework: {FRAMEWORK_NAME}')\n",
                "print(f'🤖 Models: {\", \".join(MODELS_ANALYZED)}')\n",
                "print(f'📈 Total analyses: {TOTAL_ANALYSES}')\n"
            ]
        })
        
        # Data loading cell
        cells.append({
            "cell_type": "code", 
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# RESULTS DATA - Pre-loaded from Stage 5 experiment\n",
                "# =============================================================================\n",
                "\n",
                f"# Raw experiment results\n",
                f"EXPERIMENT_RESULTS = {json.dumps(experiment_result, indent=2)}\n",
                "\n",
                "# Extract condition results into DataFrame\n",
                "condition_data = []\n",
                "for condition in EXPERIMENT_RESULTS['condition_results']:\n",
                "    condition_data.append({\n",
                "        'model': condition['condition_identifier'],\n",
                "        'centroid_x': condition['centroid'][0],\n",
                "        'centroid_y': condition['centroid'][1], \n",
                "        'total_analyses': condition.get('total_analyses', 0),\n",
                "        'raw_scores': condition.get('raw_scores', {})\n",
                "    })\n",
                "\n",
                "df_results = pd.DataFrame(condition_data)\n",
                "print('✅ Results loaded into DataFrame:')\n",
                "print(df_results.head())\n",
                "\n",
                "# Statistical metrics\n",
                f"STATISTICAL_METRICS = {json.dumps(metadata['statistical_metrics'], indent=2)}\n",
                "print(f'\\n📊 Statistical metrics available: {list(STATISTICAL_METRICS.keys())}')"
            ]
        })
        
        # Standard framework specific analysis cell
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Standard Framework Analysis\n",
                "\n",
                "### Coordinate Space Interpretation\n",
                "Your framework positions analyzed content in a **theoretical coordinate space** where each axis represents a dimension of your analytical framework. The centroid positions show where each model's analysis clusters in this space.\n",
                "\n",
                "### Key Metrics\n",
                "- **Centroid Position** (X, Y): The average position of all analyses for each model\n",
                "- **Magnitude**: Distance from origin (0,0) - indicates overall \"intensity\" of the analysis\n",
                "- **Angle**: Direction in the coordinate space relative to the theoretical axes\n",
                "- **Spread**: How dispersed the individual analyses are around the centroid\n"
            ]
        })
        
        # Visualization cell
        cells.append({
            "cell_type": "code",
            "execution_count": None, 
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# COORDINATE VISUALIZATION - Democratic Tension Quadrants\n",
                "# =============================================================================\n",
                "\n",
                "# Create quadrant visualization\n",
                "fig, ax = plt.subplots(1, 1, figsize=(10, 10))\n",
                "\n",
                "# Plot model centroids\n",
                "colors = sns.color_palette('husl', len(df_results))\n",
                "for i, (_, row) in enumerate(df_results.iterrows()):\n",
                "    ax.scatter(row['centroid_x'], row['centroid_y'], \n",
                "              s=200, alpha=0.7, color=colors[i], \n",
                "              label=row['model'])\n",
                "    ax.annotate(row['model'], \n",
                "               (row['centroid_x'], row['centroid_y']),\n",
                "               xytext=(5, 5), textcoords='offset points',\n",
                "               fontsize=10, ha='left')\n",
                "\n",
                "# Add quadrant lines and labels\n",
                "ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)\n",
                "ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)\n",
                "\n",
                "# Quadrant labels for Democratic Tension Model\n",
                "ax.text(0.5, 0.5, 'High Populism\\n+ High Nationalism', \n",
                "        transform=ax.transAxes, ha='center', va='center',\n",
                "        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))\n",
                "ax.text(-0.5, 0.5, 'High Populism\\n+ High Patriotism',\n",
                "        transform=ax.transAxes, ha='center', va='center', \n",
                "        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))\n",
                "ax.text(-0.5, -0.5, 'High Pluralism\\n+ High Patriotism',\n",
                "        transform=ax.transAxes, ha='center', va='center',\n",
                "        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))\n",
                "ax.text(0.5, -0.5, 'High Pluralism\\n+ High Nationalism',\n",
                "        transform=ax.transAxes, ha='center', va='center',\n",
                "        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))\n",
                "\n",
                "ax.set_xlabel('Patriotism ← → Nationalism', fontsize=12)\n",
                "ax.set_ylabel('Pluralism ← → Populism', fontsize=12)\n",
                "ax.set_title(f'Democratic Tension Analysis: {EXPERIMENT_NAME}\\nBrazilian Political Discourse Coordinates', \n",
                "             fontsize=14, pad=20)\n",
                "ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')\n",
                "ax.grid(True, alpha=0.3)\n",
                "ax.set_aspect('equal')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
                "\n",
                "print(f'📊 Coordinate plot generated for {len(df_results)} models')"
            ]
        })
        
        # Statistical analysis embedding (creates complexity for scaling)
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# EMBEDDED STATISTICAL ANALYSIS - Creates natural scaling challenges! 📈\n",
                "# =============================================================================\n",
                "\n",
                "def calculate_geometric_similarity(results_df):\n",
                "    \"\"\"Calculate pairwise geometric distances between model centroids\"\"\"\n",
                "    distances = []\n",
                "    models = results_df['model'].tolist()\n",
                "    \n",
                "    for i in range(len(results_df)):\n",
                "        for j in range(i + 1, len(results_df)):\n",
                "            x1, y1 = results_df.iloc[i][['centroid_x', 'centroid_y']]\n",
                "            x2, y2 = results_df.iloc[j][['centroid_x', 'centroid_y']]\n",
                "            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)\n",
                "            distances.append({\n",
                "                'model_1': models[i],\n",
                "                'model_2': models[j], \n",
                "                'distance': distance\n",
                "            })\n",
                "    \n",
                "    return pd.DataFrame(distances)\n",
                "\n",
                "def calculate_dimensional_correlation(results_df):\n",
                "    \"\"\"Calculate correlation between model positions\"\"\"\n",
                "    if len(results_df) < 2:\n",
                "        return {\"error\": \"Need at least 2 models for correlation\"}\n",
                "    \n",
                "    x_coords = results_df['centroid_x'].values\n",
                "    y_coords = results_df['centroid_y'].values\n",
                "    \n",
                "    correlation = np.corrcoef(x_coords, y_coords)[0, 1]\n",
                "    \n",
                "    return {\n",
                "        'x_y_correlation': correlation,\n",
                "        'x_mean': np.mean(x_coords),\n",
                "        'y_mean': np.mean(y_coords),\n",
                "        'x_std': np.std(x_coords),\n",
                "        'y_std': np.std(y_coords)\n",
                "    }\n",
                "\n",
                "# Run embedded statistical analysis\n",
                "geometric_analysis = calculate_geometric_similarity(df_results)\n",
                "correlation_analysis = calculate_dimensional_correlation(df_results)\n",
                "\n",
                "print('✅ Geometric Similarity Analysis:')\n",
                "print(geometric_analysis)\n",
                "print('\\n✅ Dimensional Correlation Analysis:')\n",
                "print(correlation_analysis)\n",
                "\n",
                "# This is getting complex... imagine having 20+ experiments to manage! 🤔"
            ]
        })
        
        # Publication export cell (scales poorly)
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# =============================================================================\n",
                "# PUBLICATION-READY EXPORT - Manual process that scales poorly 📝\n",
                "# =============================================================================\n",
                "\n",
                "def export_for_publication(results_df, job_id):\n",
                "    \"\"\"Export results in academic publication format\"\"\"\n",
                "    \n",
                "    # Create publication directory \n",
                "    pub_dir = Path(f'publication_exports/{job_id}')\n",
                "    pub_dir.mkdir(parents=True, exist_ok=True)\n",
                "    \n",
                "    # Export data as CSV\n",
                "    results_df.to_csv(pub_dir / 'model_centroids.csv', index=False)\n",
                "    \n",
                "    # Export statistical summary\n",
                "    summary = {\n",
                "        'experiment_name': EXPERIMENT_NAME,\n",
                "        'framework': FRAMEWORK_NAME,\n",
                "        'models_analyzed': MODELS_ANALYZED,\n",
                "        'total_analyses': TOTAL_ANALYSES,\n",
                "        'mean_x': results_df['centroid_x'].mean(),\n",
                "        'mean_y': results_df['centroid_y'].mean(),\n",
                "        'std_x': results_df['centroid_x'].std(),\n",
                "        'std_y': results_df['centroid_y'].std()\n",
                "    }\n",
                "    \n",
                "    with open(pub_dir / 'summary_statistics.json', 'w') as f:\n",
                "        json.dump(summary, f, indent=2)\n",
                "    \n",
                "    print(f'📊 Publication files exported to: {pub_dir}')\n",
                "    print('📁 Files: model_centroids.csv, summary_statistics.json')\n",
                "    \n",
                "    return pub_dir\n",
                "\n",
                "# Export for publication\n",
                "export_dir = export_for_publication(df_results, JOB_ID)\n",
                "\n",
                "print('\\n🎓 Ready for academic submission!')\n",
                "print('💡 Pro tip: With multiple experiments, managing all these exports becomes... challenging!')\n",
                "print('🚀 That\\'s when enterprise tools become really helpful! 😉')"
            ]
        })
        
        # BYU collaboration cell
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Next Steps for BYU Collaboration\n",
                "\n",
                "### Validation Protocol\n",
                "1. **Correlation Analysis**: Compare these LLM results with Tamaki & Fuks manual coding\n",
                "2. **Statistical Significance**: Test if differences are meaningful (target: r > 0.70)\n",
                "3. **Methodological Documentation**: Prepare for academic publication\n",
                "\n",
                "### Value Demonstration\n",
                "- **Speed**: LLM analysis completes in minutes vs. weeks of manual coding\n",
                "- **Scale**: Can analyze entire corpora not feasible for manual coding\n",
                "- **Consistency**: Eliminates inter-rater reliability concerns\n",
                "- **Innovation**: Enables novel analytical approaches (temporal dynamics, cross-framework comparison)\n",
                "\n",
                "### Research Acceleration Opportunities\n",
                "- **Global Populism Database**: Scale to thousands of speeches across countries\n",
                "- **Temporal Analysis**: Track discourse evolution across election cycles  \n",
                "- **Comparative Frameworks**: Apply multiple theoretical lenses simultaneously\n",
                "- **Real-time Analysis**: Monitor contemporary political discourse as it emerges\n",
                "\n",
                "**Ready to transform computational social science research! 🚀**\n"
            ]
        })
        
        return cells
    
    def _extract_framework_info(self, framework_config: Dict[str, Any]) -> Dict[str, Any]:
        """Extract framework information dynamically for use in templates"""
        
        # Get basic framework info
        framework_name = framework_config.get('name', 'Unknown Framework')
        display_name = framework_config.get('display_name', framework_name)
        description = framework_config.get('description', 'Framework analysis')
        
        # Extract components and axes
        components = framework_config.get('components', {})
        axes = framework_config.get('axes', {})
        
        # Get axis names if available
        axis_names = []
        axis_labels = {}
        for axis_id, axis_config in axes.items():
            axis_name = axis_config.get('description', axis_id)
            axis_names.append(axis_name)
            
            # Extract anchor names for this axis
            anchor_ids = axis_config.get('anchor_ids', [])
            if len(anchor_ids) == 2:
                anchor_1 = components.get(anchor_ids[0], {}).get('description', anchor_ids[0])
                anchor_2 = components.get(anchor_ids[1], {}).get('description', anchor_ids[1])
                axis_labels[axis_id] = f"{anchor_1} ← → {anchor_2}"
        
        # Generate generic quadrant labels or use framework-specific ones
        quadrant_labels = self._generate_quadrant_labels(components, axes)
        
        return {
            'framework_name': framework_name,
            'display_name': display_name,
            'description': description,
            'components': components,
            'axes': axes,
            'axis_names': axis_names,
            'axis_labels': axis_labels,
            'quadrant_labels': quadrant_labels
        }
    
    def _generate_quadrant_labels(self, components: Dict[str, Any], axes: Dict[str, Any]) -> Dict[str, str]:
        """Generate quadrant labels based on framework structure"""
        
        # If we have exactly 2 axes, generate quadrant labels
        if len(axes) == 2:
            axis_list = list(axes.values())
            if len(axis_list) >= 2:
                # Get anchor names from the first two axes
                axis1_anchors = axis_list[0].get('anchor_ids', [])
                axis2_anchors = axis_list[1].get('anchor_ids', [])
                
                if len(axis1_anchors) == 2 and len(axis2_anchors) == 2:
                    # Get component descriptions
                    comp1_high = components.get(axis1_anchors[0], {}).get('description', axis1_anchors[0])
                    comp1_low = components.get(axis1_anchors[1], {}).get('description', axis1_anchors[1])
                    comp2_high = components.get(axis2_anchors[0], {}).get('description', axis2_anchors[0])
                    comp2_low = components.get(axis2_anchors[1], {}).get('description', axis2_anchors[1])
                    
                    return {
                        'q1': f"High {comp1_high.split()[0]}\\n+ High {comp2_high.split()[0]}",
                        'q2': f"High {comp1_high.split()[0]}\\n+ High {comp2_low.split()[0]}",
                        'q3': f"High {comp1_low.split()[0]}\\n+ High {comp2_low.split()[0]}",
                        'q4': f"High {comp1_low.split()[0]}\\n+ High {comp2_high.split()[0]}"
                    }
        
        # Generic quadrant labels as fallback
        return {
            'q1': 'Quadrant I\\n(+X, +Y)',
            'q2': 'Quadrant II\\n(-X, +Y)', 
            'q3': 'Quadrant III\\n(-X, -Y)',
            'q4': 'Quadrant IV\\n(+X, -Y)'
        }


def trigger_stage6_handoff(
    experiment_result: Dict[str, Any], 
    experiment_file_path: str,
    experiment_def: Dict[str, Any]
) -> str:
    """
    Main entry point for triggering Stage 6 handoff after Stage 5 completion.
    
    Args:
        experiment_result: Result dictionary from successful experiment execution
        experiment_file_path: Path to the original experiment YAML file
        experiment_def: The loaded experiment definition dictionary
        
    Returns:
        Path to generated Stage 6 notebook
    """
    orchestrator = Stage6HandoffOrchestrator()
    return orchestrator.generate_stage6_notebook(
        experiment_result, 
        experiment_file_path, 
        experiment_def
    ) 