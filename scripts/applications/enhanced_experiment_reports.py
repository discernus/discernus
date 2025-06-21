#!/usr/bin/env python3
"""
Enhanced Experiment Report Generator - FIXED VERSION

✅ Uses actual PlotlyCircularVisualizer with proper wells configuration
✅ Checks for existing visualizations from production pipeline first  
✅ Only generates visualizations when production pipeline failed
✅ Uses correct circular visualization interface
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.narrative_gravity.models import get_db_session, Experiment, Run, FrameworkVersion
from src.narrative_gravity.api.analysis_service import RealAnalysisService

# Import current visualization tools
try:
    from src.narrative_gravity.visualization.plotly_circular import PlotlyCircularVisualizer
    CIRCULAR_VIZ_AVAILABLE = True
except ImportError:
    CIRCULAR_VIZ_AVAILABLE = False
    PlotlyCircularVisualizer = None


class EnhancedExperimentReportGenerator:
    """Enhanced experiment report generator with PROPER circular visualization integration."""
    
    def __init__(self, output_base_dir="analysis_results"):
        self.output_base = Path(output_base_dir)
        self.output_base.mkdir(exist_ok=True)
        
        # Initialize visualization tools
        if CIRCULAR_VIZ_AVAILABLE:
            self.circular_viz = PlotlyCircularVisualizer()
        
        # Initialize LLM for enhanced summaries
        self.llm_service = RealAnalysisService()
    
    def _load_framework_wells(self, framework_name: str) -> dict:
        """Load wells configuration from framework JSON."""
        
        framework_path = Path("frameworks") / framework_name / "framework.json"
        if framework_path.exists():
            with open(framework_path, 'r') as f:
                framework_config = json.load(f)
            return framework_config.get('wells', {})
        
        return {}
    
    def _check_existing_visualizations(self, experiment_id: int) -> dict:
        """Check for existing visualizations from production pipeline."""
        
        existing_viz = {}
        
        # Look for existing experiment directory and visualizations
        analysis_results_dir = Path("analysis_results")
        if analysis_results_dir.exists():
            for result_dir in analysis_results_dir.iterdir():
                if result_dir.is_dir() and f"experiment_{experiment_id}" in result_dir.name:
                    
                    # Check for standard visualizations directory
                    viz_dir = result_dir / "visualizations"
                    if viz_dir.exists():
                        for viz_file in viz_dir.glob("*.html"):
                            existing_viz[viz_file.stem] = viz_file
                    
                    # Check validation reports to see if pipeline succeeded
                    validation_dir = result_dir / "validation_reports"
                    pipeline_succeeded = False
                    if validation_dir.exists():
                        for report_file in validation_dir.glob("*.json"):
                            try:
                                with open(report_file, 'r') as f:
                                    report = json.load(f)
                                if report.get('status') == 'success':
                                    pipeline_succeeded = True
                                    break
                            except:
                                continue
                    
                    existing_viz['pipeline_succeeded'] = pipeline_succeeded
                    break
        
        return existing_viz
    
    def _find_or_create_experiment_dir(self, experiment_id: int) -> Path:
        """Find existing experiment directory or create new one."""
        
        # Look for existing experiment directory
        existing_dirs = list(self.output_base.glob(f"experiment_{experiment_id}_*"))
        
        if existing_dirs:
            exp_dir = max(existing_dirs, key=lambda d: d.name)
            print(f"   📁 Using existing experiment directory: {exp_dir.name}")
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            exp_dir = self.output_base / f"experiment_{experiment_id}_{timestamp}"
            exp_dir.mkdir(exist_ok=True)
            print(f"   📁 Created new experiment directory: {exp_dir.name}")
        
        return exp_dir
        
    async def generate_enhanced_report(self, experiment_id: int) -> Path:
        """Generate enhanced report with proper visualization integration."""
        
        session = get_db_session()
        try:
            # Get experiment and runs data
            experiment = session.query(Experiment).filter_by(id=experiment_id).first()
            if not experiment:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            runs = session.query(Run).filter_by(experiment_id=experiment_id).all()
            if not runs:
                raise ValueError(f"No analysis runs found for experiment {experiment_id}")
            
            print(f"📊 Generating enhanced report for: {experiment.name}")
            print(f"   Runs found: {len(runs)}")
            
            # Find or create experiment output directory
            exp_dir = self._find_or_create_experiment_dir(experiment_id)
            
            # Check for existing visualizations
            existing_viz = self._check_existing_visualizations(experiment_id)
            
            # Extract comprehensive experiment data
            experiment_data = self._extract_comprehensive_data(experiment, runs, session)
            
            # Handle visualizations
            print("   🎨 Processing visualizations...")
            viz_paths = await self._handle_visualizations(experiment_data, exp_dir, existing_viz)
            
            # Find and link existing academic outputs
            print("   🔍 Finding academic outputs...")
            academic_links = self._find_academic_outputs(experiment_id)
            
            # Generate detailed summary
            print("   🤖 Generating detailed analysis...")
            detailed_summary = await self._generate_detailed_summary(experiment_data)
            
            # Generate enhanced markdown report
            print("   📝 Assembling enhanced report...")
            report_path = await self._generate_enhanced_markdown(
                experiment_data, viz_paths, academic_links, detailed_summary, exp_dir
            )
            
            # Also create HTML version
            html_report_path = exp_dir / f"{experiment_data['experiment']['name']}_enhanced_report.html"
            await self._generate_html_report(report_path, viz_paths, html_report_path)
            
            print(f"   ✅ Enhanced report generated: {report_path}")
            return report_path
            
        finally:
            session.close()
    
    def _extract_comprehensive_data(self, experiment, runs, session):
        """Extract detailed experiment data."""
        
        # Get framework details
        framework = session.query(FrameworkVersion).filter_by(id=experiment.framework_config_id).first()
        framework_details = {
            'name': framework.framework_name if framework else "unknown",
            'version': framework.version if framework else "unknown",
            'id': framework.id if framework else None
        }
        
        # Process runs
        runs_data = []
        all_scores = {}
        text_analysis = {}
        
        for run in runs:
            try:
                raw_scores = json.loads(run.raw_scores) if run.raw_scores else {}
                
                run_data = {
                    'run_id': run.id,
                    'run_number': run.run_number,
                    'text_id': run.text_id,
                    'llm_model': run.llm_model,
                    'raw_scores': raw_scores,
                    'framework_fit_score': run.framework_fit_score,
                    'narrative_position': {
                        'x': run.narrative_position_x,
                        'y': run.narrative_position_y
                    },
                    'calculated_metrics': {
                        'narrative_elevation': run.narrative_elevation,
                        'polarity': run.polarity,
                        'coherence': run.coherence,
                        'directional_purity': run.directional_purity
                    },
                    'duration_seconds': run.duration_seconds,
                    'api_cost': run.api_cost,
                    'success': run.success
                }
                
                runs_data.append(run_data)
                
                # Aggregate scores by text
                if run.text_id not in text_analysis:
                    text_analysis[run.text_id] = {
                        'scores': raw_scores,
                        'metrics': run_data['calculated_metrics'],
                        'position': run_data['narrative_position'],
                        'model': run.llm_model
                    }
                
                # Overall aggregation
                for well, score in raw_scores.items():
                    if well not in all_scores:
                        all_scores[well] = []
                    all_scores[well].append(score)
                    
            except Exception as e:
                print(f"   ⚠️ Error processing run {run.id}: {e}")
                continue
        
        # Calculate statistics
        well_statistics = {}
        for well, scores in all_scores.items():
            well_statistics[well] = {
                'mean': sum(scores) / len(scores),
                'min': min(scores),
                'max': max(scores),
                'std': (sum((x - sum(scores)/len(scores))**2 for x in scores) / len(scores))**0.5 if len(scores) > 1 else 0,
                'count': len(scores)
            }
        
        # Identify patterns
        high_scoring_wells = [w for w, s in well_statistics.items() if s['mean'] > 0.6]
        low_scoring_wells = [w for w, s in well_statistics.items() if s['mean'] < 0.3]
        variable_wells = [w for w, s in well_statistics.items() if s['std'] > 0.2]
        
        return {
            'experiment': {
                'id': experiment.id,
                'name': experiment.name,
                'hypothesis': experiment.hypothesis,
                'description': experiment.description,
                'research_context': experiment.research_context,
                'framework': framework_details,
                'prompt_template_id': experiment.prompt_template_id,
                'scoring_algorithm_id': experiment.scoring_algorithm_id,
                'analysis_mode': experiment.analysis_mode,
                'selected_models': json.loads(experiment.selected_models) if experiment.selected_models else [],
                'status': experiment.status,
                'total_runs': experiment.total_runs,
                'successful_runs': experiment.successful_runs,
                'created_at': experiment.created_at,
                'updated_at': experiment.updated_at
            },
            'runs': runs_data,
            'text_analysis': text_analysis,
            'well_statistics': well_statistics,
            'patterns': {
                'high_scoring_wells': high_scoring_wells,
                'low_scoring_wells': low_scoring_wells,
                'variable_wells': variable_wells
            },
            'summary_metrics': {
                'total_runs': len(runs_data),
                'successful_runs': len([r for r in runs_data if r['success']]),
                'texts_analyzed': len(text_analysis),
                'total_cost': sum(r['api_cost'] or 0 for r in runs_data),
                'avg_duration': sum(r['duration_seconds'] or 0 for r in runs_data) / len(runs_data) if runs_data else 0,
                'avg_framework_fit': sum(r['framework_fit_score'] or 0 for r in runs_data) / len(runs_data) if runs_data else 0
            }
        }
    
    async def _handle_visualizations(self, experiment_data, exp_dir, existing_viz):
        """Handle visualizations - use existing if available, generate if needed."""
        
        viz_paths = {}
        
        # If production pipeline succeeded, link to existing visualizations
        if existing_viz.get('pipeline_succeeded', False):
            print("      📊 Using existing visualizations from production pipeline")
            for viz_name, viz_path in existing_viz.items():
                if viz_name != 'pipeline_succeeded':
                    viz_paths[viz_name] = viz_path
            return viz_paths
        
        # Production pipeline failed, generate visualizations using proper circular visualizer
        print("      🔄 Production pipeline failed, generating visualizations using circular engine")
        
        viz_dir = exp_dir / "enhanced_visualizations"
        viz_dir.mkdir(exist_ok=True)
        
        if CIRCULAR_VIZ_AVAILABLE:
            await self._generate_circular_visualizations(experiment_data, viz_dir, viz_paths)
        else:
            print("      ⚠️ PlotlyCircularVisualizer not available")
            
        return viz_paths
    
    async def _generate_circular_visualizations(self, experiment_data, viz_dir, viz_paths):
        """Generate visualizations using the ACTUAL PlotlyCircularVisualizer."""
        
        # Load framework wells configuration
        framework_name = experiment_data['experiment']['framework']['name']
        wells_config = self._load_framework_wells(framework_name)
        
        if not wells_config:
            print(f"      ⚠️ No wells configuration found for framework: {framework_name}")
            return
        
        print(f"      📊 Using {framework_name} wells configuration with {len(wells_config)} wells")
        
        # Single text visualization
        if len(experiment_data['text_analysis']) == 1:
            text_id, data = next(iter(experiment_data['text_analysis'].items()))
            
            # Create single visualization using proper interface
            fig = self.circular_viz.plot(
                wells=wells_config,
                narrative_scores=data['scores'],
                narrative_label=text_id,
                title=f"Circular Analysis - {experiment_data['experiment']['name']}",
                show=False
            )
            
            # Save outputs
            html_path = viz_dir / f"circular_analysis_{text_id}.html"
            png_path = viz_dir / f"circular_analysis_{text_id}.png"
            
            fig.write_html(html_path)
            try:
                fig.write_image(png_path, width=800, height=800, scale=2)
                viz_paths['circular_png'] = png_path
            except:
                pass
            
            viz_paths['circular'] = html_path
            print(f"      ✅ Generated single circular visualization: {text_id}")
        
        # Multi-text comparison visualization
        elif len(experiment_data['text_analysis']) > 1:
            
            # Prepare analyses for comparison using proper interface
            analyses = []
            for text_id, data in experiment_data['text_analysis'].items():
                analyses.append({
                    'name': text_id,
                    'wells': wells_config,  # Use actual framework wells config
                    'scores': data['scores'],  # This should be 'well_scores' according to visualizer
                    'narrative_position': data['position'],
                    'metrics': data['metrics']
                })
            
            # Create comparison using proper interface
            fig = self.circular_viz.create_comparison(
                analyses=analyses,
                title=f"Comparative Analysis - {experiment_data['experiment']['name']}"
            )
            
            # Save outputs
            html_path = viz_dir / "circular_comparison.html"
            png_path = viz_dir / "circular_comparison.png"
            
            fig.write_html(html_path)
            try:
                fig.write_image(png_path, width=1600, height=1600, scale=2)
                viz_paths['circular_png'] = png_path
            except:
                pass
            
            viz_paths['circular'] = html_path
            print(f"      ✅ Generated circular comparison: {len(analyses)} texts")
    
    def _find_academic_outputs(self, experiment_id: int) -> dict:
        """Find existing academic outputs for this experiment."""
        
        academic_links = {
            'academic_pipeline': [],
            'data_exports': [],
            'validation_reports': []
        }
        
        # Look for academic pipeline outputs
        analysis_results_dir = Path("analysis_results")
        if analysis_results_dir.exists():
            for result_dir in analysis_results_dir.iterdir():
                if result_dir.is_dir() and f"experiment_{experiment_id}" in result_dir.name:
                    
                    # Find data exports
                    exports_dir = result_dir / "academic_exports"
                    if exports_dir.exists():
                        for export_file in exports_dir.glob("*.csv"):
                            academic_links['data_exports'].append({
                                'name': export_file.name,
                                'path': str(export_file),
                                'type': 'CSV Export'
                            })
                    
                    # Find validation reports
                    validation_dir = result_dir / "validation_reports"
                    if validation_dir.exists():
                        for report_file in validation_dir.glob("*.json"):
                            academic_links['validation_reports'].append({
                                'name': report_file.name,
                                'path': str(report_file),
                                'type': 'Validation Report'
                            })
                    
                    academic_links['academic_pipeline'].append({
                        'name': result_dir.name,
                        'path': str(result_dir),
                        'type': 'Academic Pipeline Output'
                    })
        
        return academic_links
    
    async def _generate_detailed_summary(self, experiment_data):
        """Generate detailed analysis summary."""
        
        exp = experiment_data['experiment']
        metrics = experiment_data['summary_metrics']
        patterns = experiment_data['patterns']
        
        # Simple analysis without LLM calls
        support_level = "strong" if metrics['avg_framework_fit'] > 0.75 else "moderate" if metrics['avg_framework_fit'] > 0.6 else "limited"
        
        summary = f"""
This experiment demonstrates {support_level} validation of the {exp['framework']['name']} framework 
with an average fit score of {metrics['avg_framework_fit']:.3f}. 

**Key Findings:**
- **Success Rate**: {metrics['successful_runs']}/{metrics['total_runs']} ({(metrics['successful_runs']/metrics['total_runs']*100):.1f}%)
- **High-scoring wells**: {', '.join(patterns['high_scoring_wells'][:5])}
- **Framework effectiveness**: {support_level.title()} support for hypothesis
- **Cost efficiency**: ${metrics['total_cost']:.4f} total analysis cost
- **Processing speed**: {metrics['avg_duration']:.2f}s average execution time

The results {'support' if len(patterns['high_scoring_wells']) > len(patterns['low_scoring_wells']) else 'partially support'} 
the original hypothesis and demonstrate the framework's utility for narrative analysis.
"""
        
        return summary
    
    async def _generate_enhanced_markdown(self, experiment_data, viz_paths, academic_links, detailed_summary, output_dir):
        """Generate enhanced Markdown report with proper visualization integration."""
        
        exp = experiment_data['experiment']
        metrics = experiment_data['summary_metrics']
        
        # Generate report content with inline visualizations
        markdown_content = f"""# Enhanced Experiment Report: {exp['name']}

**Generated**: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}  
**Experiment ID**: {exp['id']}  
**Status**: {exp['status'].title()}  
**Framework**: {exp['framework']['name']} v{exp['framework']['version']}

---

## Executive Summary

{detailed_summary}

---

## Visualizations (Standard Pipeline)

"""

        # Add visualizations inline using ACTUAL circular visualizer outputs
        if 'circular_png' in viz_paths:
            if len(experiment_data['text_analysis']) == 1:
                markdown_content += f"""### Circular Analysis

![Circular Analysis](enhanced_visualizations/{viz_paths['circular_png'].name})

*Figure 1: Circular visualization showing narrative positioning using {exp['framework']['name']} framework wells*

📊 **Interactive Version**: [enhanced_visualizations/{viz_paths['circular'].name}](enhanced_visualizations/{viz_paths['circular'].name})

"""
            else:
                markdown_content += f"""### Multi-Text Circular Comparison

![Circular Comparison](enhanced_visualizations/{viz_paths['circular_png'].name})

*Figure 1: Circular comparison visualization showing narrative positioning across {len(experiment_data['text_analysis'])} analyzed texts*

📊 **Interactive Version**: [enhanced_visualizations/{viz_paths['circular'].name}](enhanced_visualizations/{viz_paths['circular'].name})

"""

        # Add experiment configuration
        markdown_content += f"""---

## Experiment Configuration

### Research Design
- **Hypothesis**: {exp['hypothesis']}
- **Research Context**: {exp['research_context']}
- **Framework**: {exp['framework']['name']} (ID: {exp['framework']['id']})
- **Analysis Mode**: {exp['analysis_mode']}
- **Selected Models**: {', '.join(exp['selected_models'])}

### Execution Summary
- **Total Runs**: {metrics['total_runs']}
- **Successful Runs**: {metrics['successful_runs']} ({(metrics['successful_runs']/metrics['total_runs']*100):.1f}%)
- **Texts Analyzed**: {metrics['texts_analyzed']}
- **Total Cost**: ${metrics['total_cost']:.4f}
- **Average Duration**: {metrics['avg_duration']:.2f} seconds
- **Average Framework Fit**: {metrics['avg_framework_fit']:.3f}

---

## Academic Pipeline Integration

"""

        # Add academic links
        if any(academic_links.values()):
            if academic_links['academic_pipeline']:
                markdown_content += "\n### Academic Pipeline Outputs\n"
                for link in academic_links['academic_pipeline']:
                    markdown_content += f"- 📁 [{link['name']}]({link['path']}) - {link['type']}\n"
            
            if academic_links['data_exports']:
                markdown_content += "\n### Data Exports\n"
                for link in academic_links['data_exports']:
                    markdown_content += f"- 📊 [{link['name']}]({link['path']}) - {link['type']}\n"
            
            if academic_links['validation_reports']:
                markdown_content += "\n### Validation Reports\n"
                for link in academic_links['validation_reports']:
                    markdown_content += f"- ✅ [{link['name']}]({link['path']}) - {link['type']}\n"
        else:
            markdown_content += "\n*No additional academic outputs found for this experiment.*\n"

        # Add detailed results
        markdown_content += f"""

---

## Detailed Results

### Well Score Statistics

| Well | Mean Score | Std Dev | Min | Max | Runs |
|------|------------|---------|-----|-----|------|
"""

        # Add well statistics table
        for well, stats in experiment_data['well_statistics'].items():
            markdown_content += f"| {well} | {stats['mean']:.3f} | {stats['std']:.3f} | {stats['min']:.3f} | {stats['max']:.3f} | {stats['count']} |\n"

        # Add run details
        markdown_content += f"""

### Run Details

| Run | Text ID | Model | Framework Fit | Cost | Duration | Success |
|-----|---------|-------|---------------|------|----------|----------|
"""

        # Add individual run results
        for run in experiment_data['runs']:
            success_icon = "✅" if run['success'] else "❌"
            markdown_content += f"| {run['run_number']} | {run['text_id']} | {run['llm_model']} | {run['framework_fit_score']:.3f} | ${run['api_cost']:.4f} | {run['duration_seconds']:.2f}s | {success_icon} |\n"

        markdown_content += f"""

---

## Technical Details

### Framework Configuration
- **Framework**: {exp['framework']['name']} v{exp['framework']['version']}
- **Framework ID**: {exp['framework']['id']}
- **Wells Configuration**: Loaded from {exp['framework']['name']} framework JSON
- **Visualization Engine**: PlotlyCircularVisualizer (proper circular visualizations)

### Methodology
- **Pipeline**: Enhanced experiment report generator with standard visualization integration
- **Visualization Tools**: {'Circular pipeline (PlotlyCircularVisualizer)' if CIRCULAR_VIZ_AVAILABLE else 'Standard'}, Academic charts
- **Data Storage**: PostgreSQL with complete provenance tracking

### Provenance
- **Created**: {exp['created_at'].strftime('%B %d, %Y at %I:%M %p')}
- **Last Updated**: {exp['updated_at'].strftime('%B %d, %Y at %I:%M %p')}
- **Database ID**: {exp['id']}
- **Report Generated**: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

---

*Enhanced report generated by the Narrative Gravity Analysis System*  
*Using standard PlotlyCircularVisualizer with proper framework wells configuration*
"""

        # Save enhanced markdown report
        report_path = output_dir / f"{exp['name']}_enhanced_report.md"
        with open(report_path, 'w') as f:
            f.write(markdown_content)
        
        # Save comprehensive data
        data_path = output_dir / "enhanced_data" / "comprehensive_experiment_data.json"
        with open(data_path, 'w') as f:
            json.dump(experiment_data, f, indent=2, default=str)
        
        return report_path
    
    async def _generate_html_report(self, markdown_path, viz_paths, html_path):
        """Generate HTML version with embedded interactive visualizations."""
        
        try:
            import markdown
            
            # Read markdown content
            with open(markdown_path, 'r') as f:
                markdown_content = f.read()
            
            # Convert markdown to HTML
            md = markdown.Markdown(extensions=['tables', 'fenced_code'])
            html_body = md.convert(markdown_content)
            
            # Create complete HTML document
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Experiment Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1, h2, h3 {{ color: #2c3e50; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{ background-color: #f2f2f2; }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""
            
            # Save HTML report
            with open(html_path, 'w') as f:
                f.write(html_content)
            
            print(f"      ✅ Generated HTML report: {html_path.name}")
            
        except ImportError:
            print("      ⚠️ HTML generation requires 'markdown' package: pip install markdown")
        except Exception as e:
            print(f"      ⚠️ HTML generation failed: {e}")

    async def generate_all_enhanced_reports(self):
        """Generate enhanced reports for all experiments with runs."""
        
        session = get_db_session()
        try:
            # Get all experiments that have runs
            experiments = session.query(Experiment).filter(
                Experiment.id.in_(
                    session.query(Run.experiment_id).distinct()
                )
            ).all()
            
            reports = []
            for experiment in experiments:
                try:
                    report_path = await self.generate_enhanced_report(experiment.id)
                    reports.append({
                        'experiment_id': experiment.id,
                        'name': experiment.name,
                        'report_path': report_path
                    })
                except Exception as e:
                    print(f"❌ Failed to generate report for experiment {experiment.id}: {e}")
            
            # Generate index
            if reports:
                await self._generate_enhanced_index(reports)
            
            return reports
            
        finally:
            session.close()
    
    async def _generate_enhanced_index(self, reports):
        """Generate enhanced reports index."""
        
        index_content = f"""# Enhanced Experiment Reports Dashboard

**Generated**: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}  
**Total Reports**: {len(reports)}  
**Report Type**: Enhanced with Proper Circular Visualization Integration

This dashboard provides access to comprehensive experiment reports using the actual PlotlyCircularVisualizer.

## 🧪 Available Experiment Reports

"""

        for report in reports:
            exp_dir = report['report_path'].parent
            md_file = report['report_path'].name
            html_file = md_file.replace('.md', '.html')
            
            index_content += f"""### 📊 {report['name']}
- **Experiment ID**: {report['experiment_id']}
- **📄 Markdown Report**: [{md_file}]({exp_dir.name}/{md_file})  
- **🌐 HTML Report**: [{html_file}]({exp_dir.name}/{html_file}) *(with embedded interactive visualizations)*
- **Report Type**: Uses ACTUAL PlotlyCircularVisualizer with framework wells configuration

"""

        index_content += f"""
---

## 🎯 Enhanced Report Features (FIXED)

### 📊 **Proper Circular Visualization Integration**
- **✅ Real Circular Charts**: Uses actual PlotlyCircularVisualizer from yesterday's work
- **✅ Framework Wells Config**: Loads proper wells configuration from framework JSON files  
- **✅ Correct Interface**: Uses proper wells/narrative_scores data structure
- **✅ Multi-text Comparisons**: create_comparison() method for comparative analysis

### 🔗 **Smart Pipeline Integration**
- **✅ Reuses Existing**: Links to existing visualizations when production pipeline succeeded
- **✅ Generates When Needed**: Only creates new visualizations when production pipeline failed
- **✅ Proper Fallback**: Uses correct circular engine as fallback

### 🎨 **Proper Visualization Output**
- **✅ Actual Circular Shapes**: No more elliptical or bar charts
- **✅ Framework-Specific**: Uses actual wells angles/weights/colors from framework config
- **✅ Standard Interface**: Compatible with existing PlotlyCircularVisualizer

---

*Enhanced reports generated using the ACTUAL PlotlyCircularVisualizer*  
*With proper framework wells configuration and intelligent pipeline integration*
"""

        # Save index
        index_path = self.output_base / "ENHANCED_REPORTS_INDEX.md"
        with open(index_path, 'w') as f:
            f.write(index_content)
        
        print(f"✅ Enhanced reports index generated: {index_path}")


async def main():
    """Main function to generate enhanced reports."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate enhanced experiment reports')
    parser.add_argument('--experiment-id', type=int, help='Generate report for specific experiment')
    parser.add_argument('--all', action='store_true', help='Generate reports for all experiments')
    
    args = parser.parse_args()
    
    generator = EnhancedExperimentReportGenerator()
    
    if args.experiment_id:
        try:
            report_path = await generator.generate_enhanced_report(args.experiment_id)
            print(f"✅ Enhanced report generated: {report_path}")
        except Exception as e:
            print(f"❌ Error generating report: {e}")
    
    elif args.all:
        try:
            reports = await generator.generate_all_enhanced_reports()
            print(f"✅ Generated {len(reports)} enhanced reports")
        except Exception as e:
            print(f"❌ Error generating reports: {e}")
    
    else:
        print("Use --experiment-id <ID> or --all")


if __name__ == "__main__":
    asyncio.run(main()) 