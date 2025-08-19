"""
Human-Friendly Artifact Browser Interface

Provides an interactive interface for researchers to explore experiment artifacts
without needing to understand hash-based file names or complex directory structures.

Features:
- Human-readable artifact names and descriptions
- Interactive navigation of artifact relationships
- Search and filter capabilities
- Artifact content preview
- Export functionality for academic use
"""

import json
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import hashlib


class ArtifactBrowser:
    """
    Human-friendly interface for browsing experiment artifacts.
    
    Provides researchers with an intuitive way to explore artifacts without
    needing to understand hash-based naming or complex directory structures.
    """
    
    def __init__(self, run_directory: Path):
        """
        Initialize browser for a specific experiment run.
        
        Args:
            run_directory: Path to the experiment run directory
        """
        self.run_directory = run_directory
        self.provenance_file = run_directory / "artifacts" / "provenance.json"
        self.manifest_file = run_directory / "manifest.json"
        
        # Load data
        self.provenance_data = self._load_provenance_data()
        self.manifest_data = self._load_manifest_data()
        
        # Build artifact index
        self.artifact_index = self._build_artifact_index()
        
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
    
    def _build_artifact_index(self) -> Dict[str, Dict[str, Any]]:
        """
        Build a human-friendly index of all artifacts.
        
        Returns:
            Dictionary mapping human-readable names to artifact information
        """
        index = {}
        
        # First, try to load artifact registry for rich metadata
        shared_cache_dir = self.run_directory.parent.parent / "shared_cache" / "artifacts"
        registry_path = shared_cache_dir / "artifact_registry.json"
        
        artifact_registry = {}
        if registry_path.exists():
            try:
                with open(registry_path) as f:
                    artifact_registry = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load artifact registry: {e}")
        
        # Also load provenance data for run-specific artifact descriptions
        provenance_descriptions = self.provenance_data.get('artifact_descriptions', {})
        
        # Check for organized artifacts in the run directory first (symlinks)
        artifacts_dir = self.run_directory / "artifacts"
        if artifacts_dir.exists():
            for category_dir in artifacts_dir.iterdir():
                if category_dir.is_dir():
                    for artifact_file in category_dir.iterdir():
                        if artifact_file.is_file():
                            # Extract hash from filename (format: name_hash.ext)
                            filename = artifact_file.name
                            artifact_id = self._extract_hash_from_filename(filename)
                            
                            if artifact_id:
                                # Get metadata from registry
                                registry_data = artifact_registry.get(artifact_id, {})
                                metadata = registry_data.get('metadata', {})
                                
                                # Get artifact type from metadata or provenance
                                artifact_type = (
                                    metadata.get('artifact_type') or 
                                    provenance_descriptions.get(filename, '').replace('Artifact of type ', '') or
                                    self._infer_type_from_category(category_dir.name) or
                                    'unknown'
                                )
                                
                                # Create human-readable name
                                human_name = self._create_human_name_from_metadata(
                                    artifact_type, filename, metadata, artifact_id
                                )
                                
                                # Build comprehensive artifact info
                                artifact_data = {
                                    'id': artifact_id,
                                    'type': artifact_type,
                                    'created_time': registry_data.get('created_at', 'unknown'),
                                    'size_bytes': artifact_file.stat().st_size,
                                    'dependencies': metadata.get('dependencies', []),
                                    'metadata': metadata,
                                    'human_name': human_name,
                                    'short_id': artifact_id[:8],
                                    'filename': filename,
                                    'category': category_dir.name,
                                    'original_filename': metadata.get('original_filename', filename)
                                }
                                
                                index[human_name] = artifact_data
        
        # If no organized artifacts found, fall back to shared cache scanning
        if not index and shared_cache_dir.exists():
            for artifact_file in shared_cache_dir.glob('*'):
                if artifact_file.is_file() and len(artifact_file.name) == 64:  # SHA-256 hash
                    artifact_id = artifact_file.name
                    registry_data = artifact_registry.get(artifact_id, {})
                    metadata = registry_data.get('metadata', {})
                    
                    artifact_type = metadata.get('artifact_type', 'unknown')
                    created_time = registry_data.get('created_at', 
                                    datetime.fromtimestamp(artifact_file.stat().st_mtime).isoformat())
                    
                    human_name = self._create_human_name_from_metadata(
                        artifact_type, artifact_id, metadata, artifact_id
                    )
                    
                    artifact_data = {
                        'id': artifact_id,
                        'type': artifact_type,
                        'created_time': created_time,
                        'size_bytes': artifact_file.stat().st_size,
                        'dependencies': metadata.get('dependencies', []),
                        'metadata': metadata,
                        'human_name': human_name,
                        'short_id': artifact_id[:8],
                        'filename': artifact_id,
                        'category': 'uncategorized'
                    }
                    
                    index[human_name] = artifact_data
        
        return index
    
    def _extract_hash_from_filename(self, filename: str) -> Optional[str]:
        """
        Extract hash from filename (format: name_hash.ext or just hash).
        
        Args:
            filename: Filename to extract hash from
            
        Returns:
            Extracted hash or None
        """
        # Handle direct hash files (64 char SHA-256)
        if len(filename) == 64 and all(c in '0123456789abcdef' for c in filename):
            return filename
            
        # Handle hash-suffixed files (name_hash.ext)
        import re
        hash_pattern = r'([a-f0-9]{8,64})'
        matches = re.findall(hash_pattern, filename)
        if matches:
            # Return the longest hash found (most likely to be SHA-256)
            return max(matches, key=len)
            
        return None
    
    def _infer_type_from_category(self, category_name: str) -> str:
        """
        Infer artifact type from directory category.
        
        Args:
            category_name: Directory name (e.g., 'analysis_results')
            
        Returns:
            Inferred artifact type
        """
        category_mapping = {
            'analysis_results': 'analysis_json_v6',
            'statistical_results': 'statistical_analysis',
            'evidence': 'combined_evidence_v6',
            'analysis_plans': 'analysis_plan',
            'reports': 'final_report',
            'inputs': 'input_artifact'
        }
        return category_mapping.get(category_name, 'unknown')
    
    def _create_human_name_from_metadata(self, artifact_type: str, filename: str, 
                                       metadata: Dict[str, Any], artifact_id: str) -> str:
        """
        Create human-readable name using metadata.
        
        Args:
            artifact_type: Type of artifact
            filename: Original filename
            metadata: Artifact metadata
            artifact_id: Full artifact hash
            
        Returns:
            Human-readable artifact name
        """
        short_id = artifact_id[:8]
        
        # Use original filename if available
        if 'original_filename' in metadata:
            base_name = metadata['original_filename'].replace('.txt', '').replace('.md', '')
            return f"{base_name} ({artifact_type}) [{short_id}]"
        
        # Create descriptive names based on artifact type
        type_names = {
            'analysis_json_v6': 'Analysis Results',
            'combined_evidence_v6': 'Evidence Collection', 
            'statistical_analysis': 'Statistical Analysis',
            'final_report': 'Final Report',
            'corpus_document': 'Source Document',
            'framework': 'Analysis Framework',
            'analysis_plan': 'Analysis Plan',
            'raw_analysis_response_v6': 'Raw Analysis Response'
        }
        
        display_name = type_names.get(artifact_type, artifact_type.replace('_', ' ').title())
        
        # Add document count for evidence collections
        if artifact_type == 'combined_evidence_v6' and 'total_documents' in metadata:
            doc_count = metadata['total_documents']
            evidence_count = metadata.get('total_evidence_pieces', 0)
            return f"{display_name} ({doc_count} docs, {evidence_count} pieces) [{short_id}]"
        
        return f"{display_name} [{short_id}]"
    
    def _infer_artifact_type(self, artifact_id: str) -> str:
        """
        Deprecated: Use metadata-based type inference instead.
        """
        return 'unknown'
    
    def _create_human_name(self, artifact_type: str, artifact_id: str, created_time: str) -> str:
        """
        Create a human-readable name for an artifact.
        
        Args:
            artifact_type: Type of artifact
            artifact_id: Full artifact hash
            created_time: When artifact was created
            
        Returns:
            Human-readable name
        """
        short_id = artifact_id[:8]
        
        # Create descriptive name based on type
        if artifact_type == 'analysis_results':
            return f"Analysis Results ({short_id})"
        elif artifact_type == 'statistical_results':
            return f"Statistical Results ({short_id})"
        elif artifact_type == 'evidence':
            return f"Evidence Data ({short_id})"
        elif artifact_type == 'reports':
            return f"Final Report ({short_id})"
        elif artifact_type == 'analysis_plans':
            return f"Analysis Plan ({short_id})"
        elif artifact_type == 'raw_analysis_response':
            return f"Raw Analysis ({short_id})"
        elif artifact_type == 'combined_evidence':
            return f"Combined Evidence ({short_id})"
        else:
            return f"{artifact_type.title()} ({short_id})"
    
    def list_artifacts_by_type(self, artifact_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List artifacts, optionally filtered by type.
        
        Args:
            artifact_type: Optional type filter
            
        Returns:
            List of artifact information dictionaries
        """
        artifacts = []
        
        for human_name, artifact_data in self.artifact_index.items():
            if artifact_type is None or artifact_data['type'] == artifact_type:
                artifacts.append({
                    'human_name': human_name,
                    'type': artifact_data['type'],
                    'created_time': artifact_data['created_time'],
                    'size_bytes': artifact_data['size_bytes'],
                    'short_id': artifact_data['short_id'],
                    'dependencies_count': len(artifact_data['dependencies'])
                })
        
        # Sort by creation time
        artifacts.sort(key=lambda x: x['created_time'])
        
        return artifacts
    
    def get_artifact_details(self, human_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific artifact.
        
        Args:
            human_name: Human-readable name of the artifact
            
        Returns:
            Detailed artifact information or None if not found
        """
        if human_name not in self.artifact_index:
            return None
        
        artifact_data = self.artifact_index[human_name]
        
        # Try to load artifact content for preview
        content_preview = self._get_artifact_preview(artifact_data['id'])
        
        return {
            **artifact_data,
            'content_preview': content_preview,
            'file_path': self._find_artifact_file(artifact_data['id'])
        }
    
    def _get_artifact_preview(self, artifact_id: str) -> Optional[str]:
        """
        Get a preview of artifact content.
        
        Args:
            artifact_id: Full artifact hash
            
        Returns:
            Content preview or None if not available
        """
        # Look for artifact in shared cache
        shared_cache_path = self.run_directory.parent.parent / "shared_cache" / "artifacts" / artifact_id
        
        if shared_cache_path.exists():
            try:
                with open(shared_cache_path, 'r') as f:
                    content = f.read()
                    
                    # Handle delimited JSON format
                    if '<<<DISCERNUS_ANALYSIS_JSON_v6>>>' in content:
                        # Extract JSON after delimiter
                        json_start = content.find('{')
                        if json_start != -1:
                            json_content = content[json_start:]
                            # Find the end of the JSON object
                            brace_count = 0
                            json_end = 0
                            for i, char in enumerate(json_content):
                                if char == '{':
                                    brace_count += 1
                                elif char == '}':
                                    brace_count -= 1
                                    if brace_count == 0:
                                        json_end = i + 1
                                        break
                            
                            if json_end > 0:
                                json_content = json_content[:json_end]
                                artifact_data = json.loads(json_content)
                            else:
                                return f"❌ Invalid JSON structure: {content[:100]}..."
                        else:
                            return f"❌ Invalid delimited format: {content[:100]}..."
                    else:
                        # Regular JSON
                        artifact_data = json.loads(content)
                
                # Format the content based on artifact structure
                preview_lines = []
                preview_lines.append(f"📄 Artifact ID: {artifact_id[:16]}...")
                preview_lines.append(f"📊 Type: {type(artifact_data).__name__}")
                preview_lines.append(f"🔑 Keys: {list(artifact_data.keys())}")
                preview_lines.append("")
                
                # Show sample content from each key
                for key, value in list(artifact_data.items())[:3]:  # Show first 3 keys
                    if isinstance(value, dict):
                        preview_lines.append(f"📋 {key}:")
                        for sub_key, sub_value in list(value.items())[:2]:  # Show first 2 sub-keys
                            preview_lines.append(f"  • {sub_key}: {str(sub_value)[:50]}...")
                    elif isinstance(value, list):
                        preview_lines.append(f"📋 {key}: [{len(value)} items]")
                        if value:
                            preview_lines.append(f"  • First item: {str(value[0])[:50]}...")
                    else:
                        preview_lines.append(f"📋 {key}: {str(value)[:100]}...")
                
                preview = "\n".join(preview_lines)
                return preview
                
            except Exception as e:
                return f"❌ Error loading artifact: {str(e)}"
        
        return None
    
    def _find_artifact_file(self, artifact_id: str) -> Optional[str]:
        """
        Find the file path for an artifact.
        
        Args:
            artifact_id: Full artifact hash
            
        Returns:
            File path or None if not found
        """
        # Check shared cache first
        shared_cache_path = self.run_directory.parent.parent / "shared_cache" / "artifacts" / artifact_id
        if shared_cache_path.exists():
            return str(shared_cache_path)
        
        # Check run artifacts directory
        run_artifacts_path = self.run_directory / "artifacts" / artifact_id
        if run_artifacts_path.exists():
            return str(run_artifacts_path)
        
        return None
    
    def search_artifacts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search artifacts by human name or type.
        
        Args:
            query: Search query
            
        Returns:
            List of matching artifacts
        """
        query_lower = query.lower()
        matches = []
        
        for human_name, artifact_data in self.artifact_index.items():
            if (query_lower in human_name.lower() or 
                query_lower in artifact_data['type'].lower()):
                matches.append({
                    'human_name': human_name,
                    'type': artifact_data['type'],
                    'created_time': artifact_data['created_time'],
                    'short_id': artifact_data['short_id']
                })
        
        return matches
    
    def get_artifact_relationships(self, human_name: str) -> Dict[str, Any]:
        """
        Get artifact dependency relationships.
        
        Args:
            human_name: Human-readable name of the artifact
            
        Returns:
            Dictionary with dependency information
        """
        if human_name not in self.artifact_index:
            return {}
        
        artifact_data = self.artifact_index[human_name]
        dependencies = []
        dependents = []
        
        # Find dependencies (artifacts this one depends on)
        for dep_id in artifact_data['dependencies']:
            for other_name, other_data in self.artifact_index.items():
                if other_data['id'] == dep_id:
                    dependencies.append({
                        'human_name': other_name,
                        'type': other_data['type'],
                        'short_id': other_data['short_id']
                    })
                    break
        
        # Find dependents (artifacts that depend on this one)
        for other_name, other_data in self.artifact_index.items():
            if artifact_data['id'] in other_data['dependencies']:
                dependents.append({
                    'human_name': other_name,
                    'type': other_data['type'],
                    'short_id': other_data['short_id']
                })
        
        return {
            'artifact': {
                'human_name': human_name,
                'type': artifact_data['type'],
                'short_id': artifact_data['short_id']
            },
            'dependencies': dependencies,
            'dependents': dependents
        }
    
    def _format_relationships_html(self, relationships: Dict[str, Any]) -> str:
        """
        Format relationships data as HTML.
        
        Args:
            relationships: Dictionary with dependency information
            
        Returns:
            Formatted HTML string
        """
        if not relationships:
            return "📋 <strong>No dependency relationships found</strong>"
        
        html_lines = []
        html_lines.append("📋 <strong>Dependency Relationships:</strong>")
        
        # Dependencies (what this artifact depends on)
        dependencies = relationships.get('dependencies', [])
        if dependencies:
            html_lines.append("<br>🔽 <strong>Dependencies:</strong>")
            for dep in dependencies:
                html_lines.append(f"  • {dep['human_name']} ({dep['type']})")
        else:
            html_lines.append("<br>🔽 <strong>Dependencies:</strong> None")
        
        # Dependents (what depends on this artifact)
        dependents = relationships.get('dependents', [])
        if dependents:
            html_lines.append("<br>🔼 <strong>Dependents:</strong>")
            for dep in dependents:
                html_lines.append(f"  • {dep['human_name']} ({dep['type']})")
        else:
            html_lines.append("<br>🔼 <strong>Dependents:</strong> None")
        
        return "<br>".join(html_lines)
    
    def generate_browser_report(self) -> str:
        """
        Generate an HTML report for browsing artifacts.
        
        Returns:
            Complete HTML report with interactive artifact browser
        """
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Artifact Browser - {self.run_directory.name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .artifact-list {{ margin: 20px 0; }}
        .artifact-item {{ 
            border: 1px solid #ddd; 
            margin: 10px 0; 
            padding: 15px; 
            border-radius: 5px;
            background: white;
        }}
        .artifact-header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            margin-bottom: 10px;
        }}
        .artifact-name {{ font-weight: bold; color: #333; }}
        .artifact-type {{ 
            background: #e9ecef; 
            padding: 4px 8px; 
            border-radius: 3px; 
            font-size: 12px;
        }}
        .artifact-meta {{ 
            font-size: 12px; 
            color: #666; 
            margin: 5px 0;
        }}
        .search-box {{ 
            width: 100%; 
            padding: 10px; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
            margin: 10px 0;
        }}
        .filter-buttons {{ margin: 10px 0; }}
        .filter-btn {{ 
            background: #007bff; 
            color: white; 
            border: none; 
            padding: 8px 16px; 
            margin: 2px; 
            border-radius: 3px; 
            cursor: pointer;
        }}
        .filter-btn:hover {{ background: #0056b3; }}
        .filter-btn.active {{ background: #28a745; }}
        .preview {{ 
            background: #f8f9fa; 
            padding: 10px; 
            border-radius: 3px; 
            font-family: monospace; 
            font-size: 12px;
            max-height: 200px;
            overflow-y: auto;
        }}
        .relationships {{ margin-top: 10px; }}
        .relationship-list {{ 
            background: #f8f9fa; 
            padding: 10px; 
            border-radius: 3px;
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Artifact Browser</h1>
        <p><strong>Experiment:</strong> {self.run_directory.name}</p>
        <p><strong>Total Artifacts:</strong> {len(self.artifact_index)}</p>
        <p><strong>Generated:</strong> {datetime.now().isoformat()}</p>
    </div>
    
    <div>
        <input type="text" class="search-box" id="searchBox" placeholder="Search artifacts by name or type...">
        
        <div class="filter-buttons">
            <button class="filter-btn active" onclick="filterByType('all')">All</button>
            <button class="filter-btn" onclick="filterByType('analysis_json_v6')">Analysis</button>
            <button class="filter-btn" onclick="filterByType('statistical_analysis')">Statistics</button>
            <button class="filter-btn" onclick="filterByType('combined_evidence_v6')">Evidence</button>
            <button class="filter-btn" onclick="filterByType('final_report')">Reports</button>
            <button class="filter-btn" onclick="filterByType('corpus_document')">Documents</button>
        </div>
    </div>
    
    <div class="artifact-list" id="artifactList">
"""
        
        # Add artifact items with embedded data
        for human_name, artifact_data in self.artifact_index.items():
            # Get real preview content
            preview_content = self._get_artifact_preview(artifact_data['id'])
            if preview_content is None:
                preview_content = "❌ Unable to load artifact content"
            
            # Get relationships
            relationships = self.get_artifact_relationships(human_name)
            relationships_html = self._format_relationships_html(relationships)
            
            html += f"""
        <div class="artifact-item" data-type="{artifact_data['type']}">
            <div class="artifact-header">
                <span class="artifact-name">{human_name}</span>
                <span class="artifact-type">{artifact_data['type']}</span>
            </div>
            <div class="artifact-meta">
                <strong>ID:</strong> {artifact_data['short_id']} | 
                <strong>Created:</strong> {artifact_data['created_time']} | 
                <strong>Size:</strong> {artifact_data['size_bytes']} bytes | 
                <strong>Dependencies:</strong> {len(artifact_data['dependencies'])}
            </div>
            <button onclick="showDetails('{human_name}')" style="margin-top: 10px; padding: 5px 10px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer;">View Details</button>
            <div id="details-{human_name}" style="display: none; margin-top: 10px;">
                <div class="preview" id="preview-{human_name}">{preview_content}</div>
                <div class="relationships" id="relationships-{human_name}">{relationships_html}</div>
            </div>
        </div>
"""
        
        html += """
    </div>
    
    <script>
        // Search functionality
        document.getElementById('searchBox').addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const items = document.querySelectorAll('.artifact-item');
            
            items.forEach(item => {
                const name = item.querySelector('.artifact-name').textContent.toLowerCase();
                const type = item.querySelector('.artifact-type').textContent.toLowerCase();
                
                if (name.includes(query) || type.includes(query)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
        
        // Filter functionality
        function filterByType(type) {
            const items = document.querySelectorAll('.artifact-item');
            const buttons = document.querySelectorAll('.filter-btn');
            
            // Update button states
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            items.forEach(item => {
                if (type === 'all' || item.dataset.type === type) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        }
        
        // Show details functionality
        function showDetails(humanName) {
            const detailsDiv = document.getElementById('details-' + humanName);
            
            if (detailsDiv.style.display === 'none') {
                detailsDiv.style.display = 'block';
                // Content is already embedded in the HTML
            } else {
                detailsDiv.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""
        
        return html
    
    def save_browser_report(self, output_path: Optional[Path] = None) -> Path:
        """
        Generate and save the artifact browser report.
        
        Args:
            output_path: Optional path for the report file
            
        Returns:
            Path to the saved report file
        """
        if output_path is None:
            output_path = self.run_directory / "artifact_browser.html"
        
        html_content = self.generate_browser_report()
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return output_path


def create_artifact_browser(run_directory: str) -> str:
    """
    Convenience function to create artifact browser for a run.
    
    Args:
        run_directory: Path to experiment run directory
        
    Returns:
        Path to the generated browser report
    """
    run_path = Path(run_directory)
    browser = ArtifactBrowser(run_path)
    report_path = browser.save_browser_report()
    
    return str(report_path)


if __name__ == "__main__":
    # Example usage
    import sys
    if len(sys.argv) > 1:
        run_dir = sys.argv[1]
        report_path = create_artifact_browser(run_dir)
        print(f"Artifact browser saved to: {report_path}")
    else:
        print("Usage: python artifact_browser.py <run_directory>") 