# Template Pattern Selection Logic
# Auto-selects appropriate template pattern based on framework characteristics

import yaml
from pathlib import Path

def select_template_pattern(framework_path):
    """Auto-select appropriate template pattern based on framework characteristics
    
    Analyzes framework YAML to determine which template pattern provides
    the best analysis capabilities for the given framework type.
    
    Args:
        framework_path: Path to framework YAML file
        
    Returns:
        str: Template pattern name (two_axis_orthogonal, competitive_dynamics, complementary_moral, etc.)
    """
    
    with open(framework_path, 'r') as f:
        framework = yaml.safe_load(f)
    
    framework_name = framework.get('name', '').lower()
    
    # NEW: Check for revolutionary two-axis orthogonal architecture first
    if 'axes' in framework:
        return 'two_axis_orthogonal'
    
    # Handle v3.1 (anchors) and v3.2 (components) format according to spec
    # v3.2 frameworks use components, v3.1 frameworks use anchors
    if 'components' in framework:
        # v3.2 format - use components section
        anchor_count = len(framework['components'])
    else:
        # v3.1 format - use anchors section  
        anchor_count = len(framework.get('anchors', {}))
    
    has_competitive = 'competitive_relationships' in framework
    
    # Pattern matching logic based on framework characteristics
    
    # 1. COMPETITIVE DYNAMICS PATTERN (Legacy - to be deprecated)
    if has_competitive and anchor_count <= 4:
        return 'competitive_dynamics'
    
    # 2. MORAL FOUNDATIONS THEORY PATTERN  
    if 'moral' in framework_name or 'foundations' in framework_name:
        return 'complementary_moral'
    
    # 3. HIERARCHICAL INSTITUTIONAL PATTERN (Complex frameworks)
    if anchor_count >= 8 or 'civic' in framework_name or 'virtue' in framework_name:
        return 'hierarchical_institutional'
    
    # 4. TRIANGULAR COMPARATIVE PATTERN
    if 'triad' in framework_name or anchor_count == 3:
        return 'triangular_comparative'
    
    # 5. REGULATORY COMPLIANCE PATTERN
    if 'business' in framework_name or 'ethics' in framework_name or 'compliance' in framework_name:
        return 'regulatory_compliance'
    
    # 6. FALLBACK LOGIC (based on anchor count)
    if anchor_count <= 3:
        return 'competitive_dynamics'  # Simplest robust template
    elif anchor_count <= 6:
        return 'complementary_moral'
    else:
        return 'hierarchical_institutional'

def get_template_info(pattern_name):
    """Get detailed information about a template pattern
    
    Returns metadata about the selected template pattern including
    capabilities, visualizations, and requirements.
    
    Args:
        pattern_name: Template pattern name
        
    Returns:
        dict: Template pattern information
    """
    
    template_patterns = {
        'two_axis_orthogonal': {
            'description': 'Revolutionary two-axis orthogonal framework (Populism/Pluralism × Patriotism/Nationalism)',
            'anchor_range': [0, 0],  # Uses axes instead of anchors
            'features': [
                'orthogonal_dimensional_analysis',
                'quadrant_based_classification', 
                'sequential_single_pass_scoring',
                'dimensional_independence_validation',
                'bolsonaro_problem_resolution'
            ],
            'visualizations': [
                'quadrant_scatter_plot',
                'dimensional_distribution',
                'temporal_quadrant_evolution',
                'comparative_quadrant_analysis',
                'axis_independence_validation'
            ],
            'frameworks': ['political_discourse_two_axis', 'orthogonal_discourse_analysis'],
            'complexity': 'medium',
            'innovation': 'eliminates_crowding_out_effects'
        },
        
        'competitive_dynamics': {
            'description': 'Competitive ideological dynamics with temporal evolution (Legacy - being deprecated)',
            'anchor_range': [3, 4],
            'features': [
                'competitive_dilution_modeling',
                'strategic_temporal_evolution', 
                'campaign_trajectory_analysis',
                'dual_panel_visualization'
            ],
            'visualizations': [
                'coordinate_space_with_competition_lines',
                'competitive_effects_boxplot',
                'temporal_evolution_complex_grid',
                'strategic_trajectory_mapping'
            ],
            'frameworks': ['tamaki_fuks_competitive_populism', 'ideological_competition'],
            'complexity': 'medium',
            'status': 'legacy_deprecated'
        },
        
        'complementary_moral': {
            'description': 'Complementary moral psychology with cross-cultural analysis',
            'anchor_range': [5, 12],
            'features': [
                'value_balance_analysis',
                'cross_cultural_comparison',
                'moral_reasoning_patterns',
                'stability_over_time'
            ],
            'visualizations': [
                'moral_foundation_balance_chart',
                'cultural_comparison_radar',
                'temporal_moral_evolution',
                'value_system_heatmap'
            ],
            'frameworks': ['moral_foundations_theory', 'value_systems'],
            'complexity': 'medium'
        },
        
        'hierarchical_institutional': {
            'description': 'Complex hierarchical frameworks with clustered anchors',
            'anchor_range': [8, 12],
            'features': [
                'virtue_vice_clustering',
                'institutional_health_metrics',
                'democratic_discourse_quality',
                'complex_relationship_modeling'
            ],
            'visualizations': [
                'clustered_arc_positioning',
                'virtue_vice_opposition_analysis',
                'institutional_health_dashboard',
                'democratic_quality_metrics'
            ],
            'frameworks': ['civic_virtue_framework', 'governance_quality'],
            'complexity': 'high'
        },
        
        'triangular_comparative': {
            'description': 'Triangular positioning with comparative entity analysis',
            'anchor_range': [3, 3],
            'features': [
                'entity_comparison_analysis',
                'positioning_relative_analysis',
                'competitive_landscape_mapping',
                'movement_tracking'
            ],
            'visualizations': [
                'triangular_positioning_space',
                'comparative_entity_analysis',
                'positioning_shift_tracking',
                'competitive_landscape_overview'
            ],
            'frameworks': ['political_worldview_triad', 'candidate_comparison'],
            'complexity': 'low'
        },
        
        'regulatory_compliance': {
            'description': 'Business ethics and regulatory compliance analysis',
            'anchor_range': [4, 5],
            'features': [
                'compliance_tracking',
                'stakeholder_analysis',
                'risk_assessment_modeling',
                'regulatory_trend_analysis'
            ],
            'visualizations': [
                'compliance_dashboard',
                'stakeholder_impact_analysis',
                'regulatory_risk_heatmap',
                'trend_compliance_tracking'
            ],
            'frameworks': ['business_ethics_framework', 'esg_analysis'],
            'complexity': 'medium'
        }
    }
    
    return template_patterns.get(pattern_name, {
        'description': 'Generic coordinate analysis template',
        'complexity': 'unknown'
    })

def validate_template_compatibility(framework_path, pattern_name):
    """Validate that selected template pattern is compatible with framework
    
    Checks framework characteristics against template requirements to ensure
    the selected pattern can properly analyze the given framework.
    
    Args:
        framework_path: Path to framework YAML file
        pattern_name: Selected template pattern name
        
    Returns:
        dict: Validation results with compatibility status and warnings
    """
    
    with open(framework_path, 'r') as f:
        framework = yaml.safe_load(f)
    
    framework_name = framework.get('name', '').lower()
    template_info = get_template_info(pattern_name)
    
    validation_result = {
        'compatible': True,
        'warnings': [],
        'recommendations': []
    }
    
    # NEW: Handle two-axis orthogonal frameworks
    if pattern_name == 'two_axis_orthogonal':
        if 'axes' not in framework:
            validation_result['warnings'].append(
                "Two-axis template selected but framework has no 'axes' section defined"
            )
            validation_result['recommendations'].append(
                "Consider using traditional anchor-based template instead"
            )
        else:
            # Validate two-axis structure - check for exactly 2 axes (any names)
            axes = framework.get('axes', {})
            if len(axes) != 2:
                validation_result['warnings'].append(
                    f"Two-axis framework should have exactly 2 axes, found {len(axes)}"
                )
            else:
                # Validate each axis has the required structure
                for axis_name, axis_config in axes.items():
                    if 'anchor_ids' not in axis_config:
                        validation_result['warnings'].append(
                            f"Axis '{axis_name}' missing required 'anchor_ids' field"
                        )
                    elif len(axis_config['anchor_ids']) != 2:
                        validation_result['warnings'].append(
                            f"Axis '{axis_name}' should have exactly 2 anchor_ids, found {len(axis_config['anchor_ids'])}"
                        )
        return validation_result
    
    # Handle traditional anchor-based frameworks
    if 'components' in framework:
        anchor_count = len(framework['components'])
    else:
        anchor_count = len(framework.get('anchors', {}))
    
    # Check anchor count compatibility for traditional frameworks
    anchor_range = template_info.get('anchor_range', [1, 20])
    if anchor_count < anchor_range[0] or anchor_count > anchor_range[1]:
        validation_result['warnings'].append(
            f"Framework has {anchor_count} anchors, template optimized for {anchor_range[0]}-{anchor_range[1]}"
        )
    
    # Check for required features
    if pattern_name == 'competitive_dynamics' and 'competitive_relationships' not in framework:
        validation_result['warnings'].append(
            "Competitive dynamics template selected but framework has no competitive relationships defined"
        )
        validation_result['recommendations'].append(
            "Consider using complementary_moral or triangular_comparative pattern instead"
        )
    
    if pattern_name == 'hierarchical_institutional' and anchor_count < 8:
        validation_result['warnings'].append(
            f"Hierarchical template designed for complex frameworks (8+ anchors), this framework has {anchor_count}"
        )
    
    # All warnings are non-fatal - framework will work, just may not be optimal
    return validation_result

def get_template_path(pattern_name):
    """Get file path for selected template pattern
    
    Returns the path to the Jupyter notebook template for the selected pattern.
    
    Args:
        pattern_name: Template pattern name
        
    Returns:
        Path: Path to template notebook file
    """
    
    template_dir = Path(__file__).parent / 'templates' / 'patterns' / pattern_name
    template_file = template_dir / 'template.ipynb'
    
    if not template_file.exists():
        # Fallback to competitive_dynamics template (most robust)
        fallback_dir = Path(__file__).parent / 'templates' / 'patterns' / 'competitive_dynamics'
        template_file = fallback_dir / 'template.ipynb'
    
    return template_file 