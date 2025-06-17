#!/usr/bin/env python3
"""
HTML Experiment Report Generator
Creates comprehensive HTML reports from experiment execution results
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

def generate_html_report(
    experiment_file: str,
    execution_results: Optional[Dict[str, Any]] = None,
    output_file: Optional[str] = None
) -> str:
    """Generate HTML report from experiment definition and execution results"""
    
    # Load experiment definition
    with open(experiment_file, 'r') as f:
        if experiment_file.endswith('.yaml'):
            import yaml
            experiment = yaml.safe_load(f)
        else:
            experiment = json.load(f)
    
    # Generate output file name if not provided
    if not output_file:
        experiment_name = experiment.get('experiment_meta', {}).get('name', 'experiment')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"experiment_reports/{experiment_name}_results_{timestamp}.html"
    
    # Create output directory if needed
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Generate HTML content
    html_content = generate_html_content(experiment, execution_results)
    
    # Write HTML file
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    return output_file

def generate_html_content(experiment: Dict[str, Any], execution_results: Optional[Dict[str, Any]] = None) -> str:
    """Generate the HTML content for the report"""
    
    meta = experiment.get('experiment_meta', {})
    components = experiment.get('components', {})
    execution = experiment.get('execution', {})
    
    # Status based on execution results
    if execution_results:
        status = "✅ Completed" if execution_results.get('successful_analyses', 0) > 0 else "❌ Failed"
        status_class = "status-success" if execution_results.get('successful_analyses', 0) > 0 else "status-error"
    else:
        status = "⏱️ Setup Complete"
        status_class = "status-pending"
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta.get('name', 'Experiment')} - Results Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .section {{
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .status-success {{ color: #28a745; font-weight: bold; }}
        .status-pending {{ color: #ffc107; font-weight: bold; }}
        .status-error {{ color: #dc3545; font-weight: bold; }}
        .code-block {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 15px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 14px;
            overflow-x: auto;
        }}
        .hypothesis {{
            border-left: 4px solid #007bff;
            padding-left: 20px;
            margin: 15px 0;
        }}
        .metric {{
            display: inline-block;
            background: #e9ecef;
            padding: 8px 12px;
            border-radius: 20px;
            margin: 5px;
            font-size: 14px;
        }}
        .execution-summary {{
            background: #e7f3ff;
            border: 1px solid #b3d9ff;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
        }}
        .cost-metric {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 4px;
            padding: 10px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 {meta.get('name', 'Experiment Report')}</h1>
        <h2>{meta.get('description', 'Experiment Description')}</h2>
        <p><strong>Version:</strong> {meta.get('version', 'Unknown')} | <strong>Generated:</strong> {timestamp}</p>
        <p><strong>Status:</strong> <span class="{status_class}">{status}</span></p>
    </div>"""

    # Executive Summary
    html += f"""
    <div class="section">
        <h2>📋 Executive Summary</h2>
        <p>{meta.get('description', 'No description provided')}</p>
        
        <div class="metric">Version: {meta.get('version', 'Unknown')}</div>
        <div class="metric">Hypotheses: {len(meta.get('hypotheses', []))}</div>
        <div class="metric">Success Criteria: {len(meta.get('success_criteria', []))}</div>"""
    
    if execution_results:
        html += f"""
        <div class="metric">Analyses: {execution_results.get('total_analyses', 0)}</div>
        <div class="metric">Success Rate: {execution_results.get('successful_analyses', 0)}/{execution_results.get('total_analyses', 0)}</div>
        <div class="metric">Total Cost: ${execution_results.get('total_cost', 0):.3f}</div>"""
    
    html += """
    </div>"""

    # Research Hypotheses
    if meta.get('hypotheses'):
        html += """
    <div class="section">
        <h2>🔬 Research Hypotheses</h2>"""
        
        for i, hypothesis in enumerate(meta.get('hypotheses', []), 1):
            html += f"""
        <div class="hypothesis">
            <h3>Hypothesis {i}</h3>
            <p>{hypothesis}</p>
        </div>"""
        
        html += """
    </div>"""

    # Execution Results (if available)
    if execution_results:
        html += f"""
    <div class="section">
        <h2>🚀 Execution Results</h2>
        <div class="execution-summary">
            <h3>Analysis Summary</h3>
            <table>
                <tr>
                    <td><strong>Total Analyses:</strong></td>
                    <td>{execution_results.get('total_analyses', 0)}</td>
                </tr>
                <tr>
                    <td><strong>Successful:</strong></td>
                    <td class="status-success">{execution_results.get('successful_analyses', 0)}</td>
                </tr>
                <tr>
                    <td><strong>Failed:</strong></td>
                    <td class="status-error">{execution_results.get('failed_analyses', 0)}</td>
                </tr>
                <tr>
                    <td><strong>Total Cost:</strong></td>
                    <td>${execution_results.get('total_cost', 0):.4f}</td>
                </tr>
                <tr>
                    <td><strong>Cost per Analysis:</strong></td>
                    <td>${execution_results.get('cost_efficiency', 0):.4f}</td>
                </tr>
            </table>
        </div>"""

        # Individual Analysis Results
        if execution_results.get('results'):
            html += """
        <h3>Individual Analysis Results</h3>
        <table>
            <thead>
                <tr>
                    <th>Analysis ID</th>
                    <th>Framework</th>
                    <th>Model</th>
                    <th>Duration</th>
                    <th>Cost</th>
                    <th>Quality Score</th>
                </tr>
            </thead>
            <tbody>"""
            
            for result in execution_results.get('results', []):
                html += f"""
                <tr>
                    <td>{result.get('analysis_id', 'Unknown')[:20]}...</td>
                    <td>{result.get('framework', 'Unknown')}</td>
                    <td>{result.get('model', 'Unknown')}</td>
                    <td>{result.get('duration_seconds', 0):.2f}s</td>
                    <td>${result.get('api_cost', 0):.4f}</td>
                    <td>{result.get('framework_fit_score', 0):.2f}</td>
                </tr>"""
            
            html += """
            </tbody>
        </table>"""
        
        html += """
    </div>"""

    # Components Used
    html += """
    <div class="section">
        <h2>🔧 Components Configuration</h2>
        <table>
            <thead>
                <tr>
                    <th>Component Type</th>
                    <th>ID</th>
                    <th>Version</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>"""
    
    # Add components to table
    for component_type, component_list in components.items():
        if isinstance(component_list, list):
            for component in component_list:
                html += f"""
                <tr>
                    <td>{component_type.title()}</td>
                    <td>{component.get('id', component.get('name', 'Unknown'))}</td>
                    <td>{component.get('version', 'N/A')}</td>
                    <td class="status-success">✅ Ready</td>
                </tr>"""
    
    html += """
            </tbody>
        </table>
    </div>"""

    # Success Criteria
    if meta.get('success_criteria'):
        html += """
    <div class="section">
        <h2>✅ Success Criteria</h2>
        <ul>"""
        
        for criterion in meta.get('success_criteria', []):
            # Status based on execution results
            status = "⏱️ Pending Evaluation" if not execution_results else "📊 Under Analysis"
            html += f"<li>{criterion} - <em>{status}</em></li>"
        
        html += """
        </ul>
    </div>"""

    # Academic Metadata
    if meta.get('principal_investigator'):
        html += f"""
    <div class="section">
        <h2>🎓 Academic Information</h2>
        <table>
            <tr>
                <td><strong>Principal Investigator:</strong></td>
                <td>{meta.get('principal_investigator', 'N/A')}</td>
            </tr>
            <tr>
                <td><strong>Institution:</strong></td>
                <td>{meta.get('institution', 'N/A')}</td>
            </tr>
            <tr>
                <td><strong>Ethical Clearance:</strong></td>
                <td>{meta.get('ethical_clearance', 'N/A')}</td>
            </tr>
            <tr>
                <td><strong>Funding Source:</strong></td>
                <td>{meta.get('funding_source', 'N/A')}</td>
            </tr>
        </table>
    </div>"""

    # Footer
    html += f"""
    <footer style="text-align: center; margin-top: 40px; padding: 20px; color: #666;">
        <p>Generated by Narrative Gravity Analysis Platform | {timestamp}</p>
        <p>Comprehensive Experiment Orchestrator v1.0.0</p>
    </footer>
</body>
</html>"""

    return html

def main():
    """CLI interface for generating HTML reports"""
    if len(sys.argv) < 2:
        print("Usage: python generate_experiment_html_report.py <experiment_file> [execution_results_file] [output_file]")
        sys.exit(1)
    
    experiment_file = sys.argv[1]
    execution_results_file = sys.argv[2] if len(sys.argv) > 2 else None
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Load execution results if provided
    execution_results = None
    if execution_results_file and Path(execution_results_file).exists():
        with open(execution_results_file, 'r') as f:
            execution_results = json.load(f)
    
    # Generate report
    output_path = generate_html_report(experiment_file, execution_results, output_file)
    print(f"✅ HTML report generated: {output_path}")

if __name__ == "__main__":
    main() 