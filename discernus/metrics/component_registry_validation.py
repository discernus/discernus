"""
Component Registry Validation
=============================

Validation metrics for Framework Specification v3.2 hybrid architecture.
Focus: Component registry consistency, polar constraint, hybrid architecture validation.

Critical Path: Brazil 2018 Democratic Tension Axis Model v3.2 validation.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Set
import warnings

def validate_component_registry(framework_config: Dict) -> Dict[str, Any]:
    """
    Validate component registry consistency and completeness.
    
    From Mathematical Foundations v1.0:
    "For framework F with component registry C and axes A:
     registry_completeness = |{anchor_ids referenced in A}| / |C|
     orphaned_components = C - {anchor_ids referenced in A}
     missing_references = {anchor_ids referenced in A} - C"
    
    Args:
        framework_config: Framework configuration dictionary
        
    Returns:
        Dictionary with validation results
    """
    validation_results = {
        'valid': False,
        'registry_completeness': 0.0,
        'orphaned_components': [],
        'missing_references': [],
        'component_count': 0,
        'referenced_component_count': 0,
        'errors': [],
        'warnings': []
    }
    
    try:
        # Extract components and axes
        components = framework_config.get('components', {})
        axes = framework_config.get('axes', {})
        
        if not components:
            validation_results['errors'].append("No components section found in framework")
            return validation_results
        
        if not axes:
            validation_results['errors'].append("No axes section found in framework")
            return validation_results
        
        # Get all component IDs
        component_ids = set(components.keys())
        validation_results['component_count'] = len(component_ids)
        
        # Get all referenced anchor IDs from axes
        referenced_ids = set()
        for axis_name, axis_config in axes.items():
            if isinstance(axis_config, dict):
                anchor_ids = axis_config.get('anchor_ids', [])
                if isinstance(anchor_ids, list):
                    referenced_ids.update(anchor_ids)
                else:
                    validation_results['warnings'].append(
                        f"Axis '{axis_name}' has non-list anchor_ids: {anchor_ids}"
                    )
        
        validation_results['referenced_component_count'] = len(referenced_ids)
        
        # Calculate registry completeness
        if len(component_ids) > 0:
            validation_results['registry_completeness'] = len(referenced_ids) / len(component_ids)
        
        # Find orphaned components (defined but not used)
        orphaned_components = component_ids - referenced_ids
        validation_results['orphaned_components'] = list(orphaned_components)
        
        # Find missing references (used but not defined)
        missing_references = referenced_ids - component_ids
        validation_results['missing_references'] = list(missing_references)
        
        # Validation logic
        if missing_references:
            validation_results['errors'].extend([
                f"Missing component definition for referenced ID: {ref_id}"
                for ref_id in missing_references
            ])
        
        if len(orphaned_components) > 0:
            validation_results['warnings'].append(
                f"Orphaned components (defined but not referenced): {list(orphaned_components)}"
            )
        
        # Overall validation
        validation_results['valid'] = (
            len(missing_references) == 0 and
            len(component_ids) > 0 and
            len(referenced_ids) > 0
        )
        
        return validation_results
        
    except Exception as e:
        validation_results['errors'].append(f"Validation error: {str(e)}")
        return validation_results

def validate_polar_constraint(framework_config: Dict) -> Dict[str, Any]:
    """
    Validate polar constraint (exactly 2 anchors per axis).
    
    From Mathematical Foundations v1.0:
    "for each axis_j in A:
        axis_anchor_count_j = |axis_j.anchor_ids|
        polar_constraint_satisfied_j = (axis_anchor_count_j == 2)
     
     polar_constraint_global = ∀ axis_j: polar_constraint_satisfied_j"
    
    Args:
        framework_config: Framework configuration dictionary
        
    Returns:
        Dictionary with polar constraint validation results
    """
    validation_results = {
        'polar_constraint_satisfied': False,
        'axes_validations': {},
        'total_axes': 0,
        'valid_axes': 0,
        'violations': [],
        'errors': []
    }
    
    try:
        axes = framework_config.get('axes', {})
        
        if not axes:
            validation_results['errors'].append("No axes section found in framework")
            return validation_results
        
        validation_results['total_axes'] = len(axes)
        
        for axis_name, axis_config in axes.items():
            axis_validation = {
                'axis_name': axis_name,
                'anchor_count': 0,
                'anchor_ids': [],
                'polar_constraint_satisfied': False,
                'errors': []
            }
            
            if not isinstance(axis_config, dict):
                axis_validation['errors'].append(f"Axis '{axis_name}' is not a dictionary")
                validation_results['axes_validations'][axis_name] = axis_validation
                continue
            
            # Check for anchor_ids (v3.2 hybrid architecture)
            anchor_ids = axis_config.get('anchor_ids', [])
            
            if not isinstance(anchor_ids, list):
                axis_validation['errors'].append(f"anchor_ids must be a list, got: {type(anchor_ids)}")
            else:
                anchor_count = len(anchor_ids)
                axis_validation['anchor_count'] = anchor_count
                axis_validation['anchor_ids'] = anchor_ids
                
                # Polar constraint: exactly 2 anchors per axis
                if anchor_count == 2:
                    axis_validation['polar_constraint_satisfied'] = True
                    validation_results['valid_axes'] += 1
                else:
                    violation = {
                        'axis': axis_name,
                        'anchor_count': anchor_count,
                        'anchor_ids': anchor_ids,
                        'violation': f"Axis has {anchor_count} anchors, requires exactly 2"
                    }
                    validation_results['violations'].append(violation)
                    axis_validation['errors'].append(
                        f"POLAR CONSTRAINT VIOLATION: {anchor_count} anchors (requires exactly 2)"
                    )
            
            validation_results['axes_validations'][axis_name] = axis_validation
        
        # Global polar constraint satisfaction
        validation_results['polar_constraint_satisfied'] = (
            validation_results['valid_axes'] == validation_results['total_axes'] and
            validation_results['total_axes'] > 0
        )
        
        return validation_results
        
    except Exception as e:
        validation_results['errors'].append(f"Polar constraint validation error: {str(e)}")
        return validation_results

def validate_hybrid_architecture(framework_config: Dict) -> Dict[str, Any]:
    """
    Comprehensive validation of v3.2 hybrid architecture.
    
    Combines component registry validation and polar constraint validation
    for complete framework consistency checking.
    
    Args:
        framework_config: Framework configuration dictionary
        
    Returns:
        Dictionary with comprehensive validation results
    """
    # Run individual validations
    registry_validation = validate_component_registry(framework_config)
    polar_validation = validate_polar_constraint(framework_config)
    
    # Combine results
    hybrid_validation = {
        'framework_valid': False,
        'version_compliance': 'v3.2',
        'component_registry_validation': registry_validation,
        'polar_constraint_validation': polar_validation,
        'overall_errors': [],
        'overall_warnings': [],
        'validation_summary': {}
    }
    
    # Collect all errors and warnings
    hybrid_validation['overall_errors'].extend(registry_validation.get('errors', []))
    hybrid_validation['overall_errors'].extend(polar_validation.get('errors', []))
    hybrid_validation['overall_warnings'].extend(registry_validation.get('warnings', []))
    
    # Overall framework validation
    hybrid_validation['framework_valid'] = (
        registry_validation.get('valid', False) and
        polar_validation.get('polar_constraint_satisfied', False) and
        len(hybrid_validation['overall_errors']) == 0
    )
    
    # Create validation summary
    hybrid_validation['validation_summary'] = {
        'component_registry_valid': registry_validation.get('valid', False),
        'polar_constraint_satisfied': polar_validation.get('polar_constraint_satisfied', False),
        'registry_completeness': registry_validation.get('registry_completeness', 0.0),
        'total_components': registry_validation.get('component_count', 0),
        'total_axes': polar_validation.get('total_axes', 0),
        'valid_axes': polar_validation.get('valid_axes', 0),
        'orphaned_components': len(registry_validation.get('orphaned_components', [])),
        'missing_references': len(registry_validation.get('missing_references', [])),
        'polar_violations': len(polar_validation.get('violations', []))
    }
    
    return hybrid_validation

def validate_framework_v32_compliance(framework_config: Dict) -> Dict[str, Any]:
    """
    Validate Framework Specification v3.2 compliance.
    
    Specific validation for Brazil 2018 framework requirements:
    - Component registry present and valid
    - Axes reference exactly 2 anchors each
    - All referenced components exist
    - Framework identification complete
    
    Args:
        framework_config: Framework configuration dictionary
        
    Returns:
        Dictionary with v3.2 compliance results
    """
    compliance_results = {
        'v32_compliant': False,
        'compliance_score': 0.0,
        'required_sections': {},
        'hybrid_architecture_validation': {},
        'brazil_2018_specific_checks': {},
        'compliance_errors': [],
        'compliance_warnings': []
    }
    
    try:
        # Check required sections
        required_sections = ['name', 'version', 'components', 'axes']
        section_results = {}
        
        for section in required_sections:
            section_present = section in framework_config
            section_results[section] = {
                'present': section_present,
                'valid': section_present and framework_config[section] is not None
            }
            
            if not section_present:
                compliance_results['compliance_errors'].append(f"Missing required section: {section}")
        
        compliance_results['required_sections'] = section_results
        
        # Check version
        version = framework_config.get('version', '')
        if version not in ['v3.2', '3.2']:
            compliance_results['compliance_warnings'].append(
                f"Framework version '{version}' may not be v3.2 compliant"
            )
        
        # Validate hybrid architecture
        hybrid_validation = validate_hybrid_architecture(framework_config)
        compliance_results['hybrid_architecture_validation'] = hybrid_validation
        
        # Brazil 2018 specific checks
        brazil_checks = {
            'coordinate_system_present': 'coordinate_system' in framework_config,
            'algorithm_config_present': 'algorithm_config' in framework_config,
            'visualization_config_present': 'visualization' in framework_config,
            'theoretical_foundation_present': 'theoretical_foundation' in framework_config
        }
        
        compliance_results['brazil_2018_specific_checks'] = brazil_checks
        
        # Calculate compliance score
        total_checks = len(required_sections) + len(brazil_checks)
        passed_checks = (
            sum(1 for s in section_results.values() if s['valid']) +
            sum(1 for c in brazil_checks.values() if c) +
            (1 if hybrid_validation.get('framework_valid', False) else 0)
        )
        
        compliance_results['compliance_score'] = passed_checks / (total_checks + 1)  # +1 for hybrid validation
        
        # Overall compliance
        compliance_results['v32_compliant'] = (
            hybrid_validation.get('framework_valid', False) and
            all(s['valid'] for s in section_results.values()) and
            len(compliance_results['compliance_errors']) == 0
        )
        
        return compliance_results
        
    except Exception as e:
        compliance_results['compliance_errors'].append(f"Compliance validation error: {str(e)}")
        return compliance_results 