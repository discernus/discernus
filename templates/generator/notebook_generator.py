# Notebook Generator for Stage 6 Templates
# Generates framework-specific Stage 6 notebooks from templates

import json
import yaml
import shutil
import numpy as np
from pathlib import Path
from datetime import datetime
from template_selector import select_template_pattern, get_template_info, validate_template_compatibility

def generate_stage6_notebook(experiment_results, framework_path, job_id, output_dir=None):
    """Generate Stage 6 notebook after successful experiment completion
    
    Main entry point for Stage 6 notebook auto-generation. Takes experiment
    results and framework configuration, selects appropriate template pattern,
    and generates configured notebook.
    
    Args:
        experiment_results: Dictionary with experiment results and metadata
        framework_path: Path to framework YAML file
        job_id: Unique experiment job identifier
        output_dir: Output directory (defaults to results/{job_id}/)
        
    Returns:
        str: Path to generated notebook
    """
    
    # Set up output directory
    if output_dir is None:
        output_dir = Path('results') / job_id
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🎯 Generating Stage 6 notebook for job: {job_id}")
    print(f"📁 Output directory: {output_dir}")
    
    # 1. Load framework and detect pattern
    print("🔍 Analyzing framework characteristics...")
    pattern = select_template_pattern(framework_path)
    template_info = get_template_info(pattern)
    validation = validate_template_compatibility(framework_path, pattern)
    
    print(f"   Selected pattern: {pattern}")
    print(f"   Template: {template_info['description']}")
    print(f"   Complexity: {template_info['complexity']}")
    
    if validation['warnings']:
        print("⚠️  Template compatibility warnings:")
        for warning in validation['warnings']:
            print(f"   • {warning}")
    
    # 2. Load template notebook
    print("📓 Loading template notebook...")
    template_path = get_template_notebook_path(pattern)
    
    if not template_path.exists():
        # Create basic template from Tamaki-Fuks as fallback
        print(f"   Template not found: {template_path}")
        print("   Creating basic template from Tamaki-Fuks notebook...")
        template_path = create_basic_template_from_tamaki_fuks(pattern)
    
    # 3. Configure template with framework-specific parameters
    print("⚙️  Configuring template for framework...")
    framework_config = generate_framework_config(framework_path, pattern)
    
    # 4. Generate notebook with injected data
    print("📝 Generating configured notebook...")
    output_path = output_dir / 'stage6_interactive_analysis.ipynb'
    
    generate_configured_notebook(
        template_path=template_path,
        framework_config=framework_config,
        experiment_results=experiment_results,
        job_id=job_id,
        output_path=output_path
    )
    
    # 5. Copy framework YAML for provenance
    framework_copy_path = output_dir / 'framework_definition.yaml'
    shutil.copy2(framework_path, framework_copy_path)
    
    print(f"✅ Stage 6 notebook generated: {output_path}")
    print(f"📋 Framework copied for provenance: {framework_copy_path}")
    print(f"🚀 Ready to run: jupyter notebook {output_path}")
    
    return str(output_path)

def get_template_notebook_path(pattern_name):
    """Get path to template notebook for given pattern"""
    template_dir = Path(__file__).parent.parent / 'patterns' / pattern_name
    return template_dir / 'template.ipynb'

def generate_framework_config(framework_path, pattern_name):
    """Generate framework-specific configuration for template
    
    Extracts framework characteristics and creates configuration dictionary
    that the template can use to adapt its analysis and visualizations.
    """
    
    with open(framework_path, 'r') as f:
        framework_yaml = yaml.safe_load(f)
    
    # Extract anchors with calculated positions (spec compliant)
    anchors = {}
    
    # Handle v3.1 (anchors) and v3.2 (components) format according to spec
    if 'components' in framework_yaml:
        # v3.2 format - use components section
        anchor_configs = framework_yaml['components']
    else:
        # v3.1 format - use anchors section
        anchor_configs = framework_yaml.get('anchors', {})
    
    for name, config in anchor_configs.items():
        angle = config.get('angle', 0)
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        
        anchors[name] = {
            'position': [x, y],  # List for JSON serialization
            'angle': angle,
            'color': config.get('color', auto_assign_color(name)),
            'description': config.get('description', ''),
            'type': config.get('type', 'anchor')
        }
    
    # Framework metadata
    metadata = {
        'name': framework_yaml.get('name', 'Unknown Framework'),
        'version': framework_yaml.get('version', '1.0'),
        'description': framework_yaml.get('description', ''),
        'anchor_count': len(anchors),
        'pattern': pattern_name
    }
    
    # Extract relationships if present
    relationships = framework_yaml.get('competitive_relationships', [])
    
    # Expected column names (for data loading)
    expected_columns = [f"{name}_score" for name in anchors.keys()]
    
    config = {
        'framework_metadata': metadata,
        'anchors': anchors,
        'relationships': relationships,
        'expected_columns': expected_columns,
        'pattern_name': pattern_name,
        'generation_timestamp': datetime.now().isoformat()
    }
    
    return config

def create_basic_template_from_tamaki_fuks(pattern_name):
    """Create basic template from existing Tamaki-Fuks notebook
    
    Fallback function to create a working template when pattern-specific
    template doesn't exist yet. Uses the proven Tamaki-Fuks notebook
    as foundation.
    """
    
    # Path to existing Tamaki-Fuks notebook (from templates/generator directory)
    tamaki_fuks_path = Path('../../examples/notebooks/stage5_to_stage6_sarah_experience.ipynb')
    
    # Create pattern directory
    pattern_dir = Path(__file__).parent.parent / 'patterns' / pattern_name
    pattern_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy Tamaki-Fuks notebook as template
    template_path = pattern_dir / 'template.ipynb'
    shutil.copy2(tamaki_fuks_path, template_path)
    
    print(f"   Created basic template: {template_path}")
    print(f"   Source: {tamaki_fuks_path}")
    
    return template_path

def generate_configured_notebook(template_path, framework_config, experiment_results, 
                                job_id, output_path):
    """Generate configured notebook from template
    
    Takes template notebook and injects framework configuration and experiment
    results to create a fully configured Stage 6 analysis notebook.
    """
    
    # Load template notebook
    with open(template_path, 'r') as f:
        notebook = json.load(f)
    
    # Create configuration injection cell
    config_cell = create_config_injection_cell(framework_config, experiment_results, job_id)
    
    # Insert configuration as second cell (after markdown header)
    notebook['cells'].insert(1, config_cell)
    
    # Update notebook metadata
    notebook['metadata']['stage6_generation'] = {
        'job_id': job_id,
        'framework_name': framework_config['framework_metadata']['name'],
        'pattern': framework_config['pattern_name'],
        'generation_time': datetime.now().isoformat(),
        'template_source': str(template_path)
    }
    
    # Save configured notebook
    with open(output_path, 'w') as f:
        json.dump(notebook, f, indent=2)

def create_config_injection_cell(framework_config, experiment_results, job_id):
    """Create cell that injects framework configuration into notebook"""
    
    config_code = f'''# Auto-Generated Framework Configuration
# Generated by Stage 6 template system for job: {job_id}

import json
import numpy as np

# Framework Configuration (Auto-Injected)
FRAMEWORK_CONFIG = {json.dumps(framework_config, indent=4)}

# Experiment Results (Auto-Injected)  
EXPERIMENT_RESULTS = {json.dumps(experiment_results, indent=4, default=str)}

# Auto-load framework from config
framework = {{
    'name': FRAMEWORK_CONFIG['framework_metadata']['name'],
    'version': FRAMEWORK_CONFIG['framework_metadata']['version'],
    'description': FRAMEWORK_CONFIG['framework_metadata']['description'],
    'anchors': FRAMEWORK_CONFIG['anchors'],
    'relationships': FRAMEWORK_CONFIG['relationships']
}}

print(f"🎯 Framework Loaded: {{framework['name']}}")
print(f"📊 Anchors: {{len(framework['anchors'])}}")
print(f"⚔️ Relationships: {{len(framework['relationships'])}}")
print(f"🔧 Pattern: {{FRAMEWORK_CONFIG['pattern_name']}}")
'''
    
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": config_code.split('\n')
    }

def auto_assign_color(anchor_name):
    """Auto-assign colors (simplified version)"""
    colors = ['#d62728', '#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd', 
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    return colors[hash(anchor_name) % len(colors)]

# Quick test function
def test_with_tamaki_fuks():
    """Test notebook generation with Tamaki-Fuks framework"""
    
    # Mock experiment results
    experiment_results = {
        'job_id': 'test_tamaki_fuks_generation',
        'framework_name': 'Tamaki-Fuks Competitive Populism',
        'total_speeches': 127,
        'validation_correlation': 0.89
    }
    
    # Test framework path (you'll need to adjust this)
    framework_path = '../../examples/notebooks/tamaki_fuks_framework.yaml'
    
    # Generate notebook
    try:
        output_path = generate_stage6_notebook(
            experiment_results=experiment_results,
            framework_path=framework_path,
            job_id='test_generation_001'
        )
        print(f"\n✅ Test successful! Generated: {output_path}")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    test_with_tamaki_fuks() 