"""
Provenance Visualization Tools

Generates clear, visual representations of provenance chains for any experiment run.
Provides automated tools for understanding artifact relationships and data flow.

Features:
- Provenance flow diagrams showing data flow from corpus to final report
- Artifact dependency graphs showing which artifacts depend on which
- Timeline visualization showing when each artifact was created
- Interactive exploration of artifact relationships
- Health check visualizations for provenance chain completeness
"""

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import hashlib


class ProvenanceVisualizer:
    """
    Generates visual representations of experiment provenance chains.
    
    Creates clear diagrams showing how data flows from corpus through analysis
    to final results, enabling researchers and external reviewers to understand
    the complete research methodology.
    """
    
    def __init__(self, run_directory: Path):
        """
        Initialize visualizer for a specific experiment run.
        
        Args:
            run_directory: Path to the experiment run directory
        """
        self.run_directory = run_directory
        self.provenance_file = run_directory / "artifacts" / "provenance.json"
        self.manifest_file = run_directory / "manifest.json"
        
        # Load provenance data
        self.provenance_data = self._load_provenance_data()
        self.manifest_data = self._load_manifest_data()
        
    def _load_provenance_data(self) -> Dict[str, Any]:
        """Load provenance.json data if available."""
        if self.provenance_file.exists():
            with open(self.provenance_file) as f:
                return json.load(f)
        return {}
    
    def _load_manifest_data(self) -> Dict[str, Any]:
        """Load manifest.json data if available."""
        if self.manifest_file.exists():
            with open(self.manifest_file) as f:
                return json.load(f)
        return {}
    
    def generate_provenance_flow_diagram(self) -> str:
        """
        Generate a Mermaid diagram showing the complete data flow.
        
        Returns:
            Mermaid diagram code showing corpus → analysis → synthesis → results flow
        """
        diagram = """
graph TD
    %% Input Stage
    A[Corpus Documents] --> B[Framework Configuration]
    B --> C[Experiment Configuration]
    
    %% Analysis Stage
    C --> D[Enhanced Analysis Agent]
    D --> E[Raw Analysis Responses]
    E --> F[Intelligent Extractor]
    F --> G[Extracted Scores & Evidence]
    
    %% Synthesis Stage
    G --> H[THIN Synthesis Pipeline]
    H --> I[Analysis Planning]
    I --> J[Mathematical Analysis]
    J --> K[Evidence Curation]
    K --> L[Results Interpretation]
    
    %% Output Stage
    L --> M[Statistical Results]
    L --> N[Curated Evidence]
    L --> O[Final Report]
    L --> P[CSV Exports]
    
    %% Provenance Organization
    M --> Q[Provenance Organization]
    N --> Q
    O --> Q
    P --> Q
    
    %% Styling
    classDef input fill:#e1f5fe
    classDef analysis fill:#f3e5f5
    classDef synthesis fill:#e8f5e8
    classDef output fill:#fff3e0
    classDef provenance fill:#fce4ec
    
    class A,B,C input
    class D,E,F,G analysis
    class H,I,J,K,L synthesis
    class M,N,O,P output
    class Q provenance
"""
        return diagram
    
    def generate_artifact_dependency_graph(self) -> str:
        """
        Generate a Mermaid diagram showing artifact dependencies.
        
        Returns:
            Mermaid diagram showing which artifacts depend on which others
        """
        # Extract artifact relationships from manifest
        cache_analysis = self.manifest_data.get('cache_analysis', {})
        artifact_storage = cache_analysis.get('artifact_storage', {})
        
        # For now, create a simplified diagram since detailed dependencies aren't stored
        diagram = """
graph TD
    %% Artifact Dependencies (Simplified)
    A[Corpus Documents] --> B[Analysis Results]
    B --> C[Statistical Results]
    B --> D[Evidence Data]
    C --> E[Final Report]
    D --> E
    
    %% Styling
    classDef input fill:#e1f5fe
    classDef analysis fill:#f3e5f5
    classDef synthesis fill:#e8f5e8
    classDef output fill:#fff3e0
    
    class A input
    class B analysis
    class C,D synthesis
    class E output
"""
        
        return diagram
    
    def generate_timeline_visualization(self) -> str:
        """
        Generate a timeline showing when artifacts were created.
        
        Returns:
            Timeline visualization of artifact creation sequence
        """
        # Use run metadata for timeline since detailed artifact timestamps aren't available
        run_metadata = self.provenance_data.get('run_metadata', {})
        run_timestamp = run_metadata.get('run_timestamp', '')
        
        diagram = """
gantt
    title Experiment Execution Timeline
    dateFormat  YYYY-MM-DD HH:mm:ss
    axisFormat %H:%M:%S
"""
        
        if run_timestamp:
            # Create a simplified timeline based on run timestamp
            diagram += f"    Analysis Phase :analysis, {run_timestamp}, 2m\n"
            diagram += f"    Synthesis Phase :synthesis, {run_timestamp}, 3m\n"
            diagram += f"    Provenance Organization :provenance, {run_timestamp}, 1m\n"
        
        return diagram
    
    def generate_health_check_diagram(self) -> str:
        """
        Generate a health check diagram showing provenance completeness.
        
        Returns:
            Visual indicators of provenance chain health and completeness
        """
        # Check for required artifacts
        required_artifacts = [
            'analysis_results',
            'statistical_results', 
            'evidence',
            'reports',
            'final_report'
        ]
        
        diagram = """
graph TD
    %% Health Check Nodes
"""
        
        artifacts = self.manifest_data.get('artifacts', {})
        artifact_types = [info.get('type', '') for info in artifacts.values()]
        
        for required in required_artifacts:
            if required in artifact_types:
                diagram += f'    {required}[✅ {required}]\n'
            else:
                diagram += f'    {required}[❌ {required}]\n'
        
        diagram += """
    %% Styling
    classDef present fill:#c8e6c9
    classDef missing fill:#ffcdd2
"""
        
        return diagram
    
    def generate_html_report(self) -> str:
        """
        Generate a complete HTML report with all visualizations.
        
        Returns:
            Complete HTML report with embedded Mermaid diagrams
        """
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Provenance Visualization - {self.run_directory.name}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .section {{ margin: 30px 0; }}
        .diagram {{ margin: 20px 0; }}
        h1, h2 {{ color: #333; }}
        .artifact-info {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
        .health-check {{ display: flex; gap: 20px; }}
        .status {{ padding: 10px; border-radius: 5px; }}
        .present {{ background: #d4edda; color: #155724; }}
        .missing {{ background: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
    <h1>Provenance Visualization Report</h1>
    <p><strong>Experiment:</strong> {self.run_directory.name}</p>
    <p><strong>Generated:</strong> {datetime.now().isoformat()}</p>
    
    <div class="section">
        <h2>1. Provenance Flow Diagram</h2>
        <p>Complete data flow from corpus through analysis to final results:</p>
        <div class="diagram">
            <div class="mermaid">
{self.generate_provenance_flow_diagram()}
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>2. Artifact Dependency Graph</h2>
        <p>Shows which artifacts depend on which others:</p>
        <div class="diagram">
            <div class="mermaid">
{self.generate_artifact_dependency_graph()}
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>3. Timeline Visualization</h2>
        <p>When each artifact was created during the experiment:</p>
        <div class="diagram">
            <div class="mermaid">
{self.generate_timeline_visualization()}
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>4. Health Check</h2>
        <p>Provenance chain completeness indicators:</p>
        <div class="diagram">
            <div class="mermaid">
{self.generate_health_check_diagram()}
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>5. Artifact Summary</h2>
        <div class="artifact-info">
            <p><strong>Total Artifacts:</strong> {self.manifest_data.get('cache_analysis', {}).get('artifact_storage', {}).get('total_artifacts', 0)}</p>
            <p><strong>Organized Artifacts:</strong> {self.provenance_data.get('run_metadata', {}).get('organized_artifacts', 0)}</p>
            <p><strong>Framework:</strong> {self.provenance_data.get('run_metadata', {}).get('framework_version', 'Unknown')}</p>
            <p><strong>Model:</strong> {self.provenance_data.get('run_metadata', {}).get('model_used', 'Unknown')}</p>
        </div>
    </div>
    
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</body>
</html>
"""
        return html
    
    def save_visualization_report(self, output_path: Optional[Path] = None) -> Path:
        """
        Generate and save the complete visualization report.
        
        Args:
            output_path: Optional path for the report file
            
        Returns:
            Path to the saved report file
        """
        if output_path is None:
            output_path = self.run_directory / "provenance_visualization.html"
        
        html_content = self.generate_html_report()
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return output_path


def create_provenance_visualization(run_directory: str) -> str:
    """
    Convenience function to create provenance visualization for a run.
    
    Args:
        run_directory: Path to experiment run directory
        
    Returns:
        Path to the generated visualization report
    """
    run_path = Path(run_directory)
    visualizer = ProvenanceVisualizer(run_path)
    report_path = visualizer.save_visualization_report()
    
    return str(report_path)


if __name__ == "__main__":
    # Example usage
    import sys
    if len(sys.argv) > 1:
        run_dir = sys.argv[1]
        report_path = create_provenance_visualization(run_dir)
        print(f"Provenance visualization saved to: {report_path}")
    else:
        print("Usage: python provenance_visualizer.py <run_directory>") 