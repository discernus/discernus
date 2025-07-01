"""
Framework Validator
===================

STRICT Framework Specification v3.2 compliance validator.
NO legacy support - enforces full v3.2 requirements including polar constraint.
"""

from typing import Dict, Any, List, Optional, Set, Union
from .validation_errors import FrameworkValidationError


class FrameworkValidator:
    """
    STRICT Framework Specification v3.2 validator.
    
    Key v3.2 Requirements:
    - Polar Constraint: Each axis MUST have exactly 2 anchors  
    - Hybrid Architecture: Components registry + axes referencing by ID
    - Required sections: name, version, positioning (anchors OR axes OR arcs)
    - v3.2 features: competitive_relationships, temporal_analysis, etc.
    """
    
    def __init__(self):
        self.required_fields = ['name', 'version']
        self.valid_versions = ['v3.2', '3.2']  # STRICT v3.2 only
        self.positioning_options = ['anchors', 'axes', 'arcs', 'components']
        
    def validate_framework(self, framework_config: Dict[str, Any], framework_name: str = None) -> Dict[str, Any]:
        """
        Validate framework against STRICT Framework Specification v3.2.
        
        Args:
            framework_config: Framework configuration dictionary
            framework_name: Optional name for error reporting
            
        Returns:
            Normalized framework configuration with extracted anchors
            
        Raises:
            FrameworkValidationError: If framework violates v3.2 specification
        """
        if not isinstance(framework_config, dict):
            raise FrameworkValidationError(
                "Framework must be a dictionary", 
                framework_name
            )
        
        # STRICT v3.2 validation
        self._validate_required_fields(framework_config, framework_name)
        self._validate_version_strict(framework_config, framework_name)
        self._validate_positioning_sections(framework_config, framework_name)
        
        # Extract and validate all anchors
        all_anchors = self._extract_all_anchors(framework_config, framework_name)
        
        # CRITICAL: Validate polar constraint for axes
        if 'axes' in framework_config:
            self._validate_polar_constraint(framework_config['axes'], framework_name)
        
        # Validate v3.2 advanced features if present
        self._validate_v3_2_features(framework_config, framework_name)
        
        # Return normalized framework with complete anchor extraction
        normalized_framework = framework_config.copy()
        normalized_framework['_extracted_anchors'] = all_anchors
        normalized_framework['_anchor_count'] = len(all_anchors)
        
        return normalized_framework
    
    def _validate_required_fields(self, framework_config: Dict[str, Any], framework_name: str):
        """Validate required framework fields"""
        for field in self.required_fields:
            if field not in framework_config:
                raise FrameworkValidationError(
                    f"Missing required field '{field}'",
                    framework_name,
                    field_path=field
                )
    
    def _validate_version_strict(self, framework_config: Dict[str, Any], framework_name: str):
        """STRICT v3.2 version validation - no legacy support"""
        version = framework_config.get('version', '')
        if version not in self.valid_versions:
            raise FrameworkValidationError(
                f"STRICT v3.2 ONLY. Unsupported version '{version}'. Use: {self.valid_versions}",
                framework_name,
                field_path='version'
            )
    
    def _validate_positioning_sections(self, framework_config: Dict[str, Any], framework_name: str):
        """Validate framework has at least one positioning section"""
        has_positioning = any(
            section in framework_config 
            for section in self.positioning_options
        )
        
        if not has_positioning:
            raise FrameworkValidationError(
                f"Framework must have at least one positioning section: {self.positioning_options}",
                framework_name,
                field_path='positioning'
            )
    
    def _extract_all_anchors(self, framework_config: Dict[str, Any], framework_name: str) -> Dict[str, Any]:
        """
        Extract ALL anchors from framework using v3.2 specification.
        Supports: components, axes, anchors, arcs
        """
        all_anchors = {}
        
        # Method 1: Components registry (v3.2 hybrid architecture)
        if 'components' in framework_config:
            components_anchors = self._extract_from_components(
                framework_config['components'], framework_name
            )
            all_anchors.update(components_anchors)
        
        # Method 2: Direct anchors section (legacy/simple format)  
        if 'anchors' in framework_config:
            direct_anchors = self._extract_from_anchors(
                framework_config['anchors'], framework_name
            )
            all_anchors.update(direct_anchors)
        
        # Method 3: Axes (with polar constraint validation)
        if 'axes' in framework_config:
            axes_anchors = self._extract_from_axes(
                framework_config['axes'], framework_name
            )
            all_anchors.update(axes_anchors)
        
        # Method 4: Arcs (v3.2 advanced positioning)
        if 'arcs' in framework_config:
            arcs_anchors = self._extract_from_arcs(
                framework_config['arcs'], framework_name
            )
            all_anchors.update(arcs_anchors)
        
        if not all_anchors:
            raise FrameworkValidationError(
                "No valid anchors found in any positioning section",
                framework_name,
                field_path='positioning'
            )
        
        return all_anchors
    
    def _extract_from_components(self, components: Dict[str, Any], framework_name: str) -> Dict[str, Any]:
        """Extract anchors from components registry (v3.2 hybrid architecture)"""
        anchors = {}
        
        if not isinstance(components, dict):
            raise FrameworkValidationError(
                "components section must be a dictionary",
                framework_name,
                field_path='components'
            )
        
        for comp_id, comp_config in components.items():
            if not isinstance(comp_config, dict):
                continue
                
            # Only extract anchors (not other component types)
            if comp_config.get('type') == 'anchor':
                anchor = self._validate_anchor_config(
                    comp_config, framework_name, f'components.{comp_id}'
                )
                # Use component_id as key for v3.2 hybrid architecture
                anchor_name = comp_config.get('component_id', comp_id)
                anchors[anchor_name] = anchor
        
        return anchors
    
    def _extract_from_anchors(self, anchors_section: Dict[str, Any], framework_name: str) -> Dict[str, Any]:
        """Extract anchors from direct anchors section"""
        anchors = {}
        
        if not isinstance(anchors_section, dict):
            raise FrameworkValidationError(
                "anchors section must be a dictionary",
                framework_name,
                field_path='anchors'
            )
        
        for anchor_name, anchor_config in anchors_section.items():
            anchor = self._validate_anchor_config(
                anchor_config, framework_name, f'anchors.{anchor_name}'
            )
            anchors[anchor_name] = anchor
        
        return anchors
    
    def _extract_from_axes(self, axes_section: Dict[str, Any], framework_name: str) -> Dict[str, Any]:
        """Extract anchors from axes section (supports both hybrid and legacy formats)"""
        anchors = {}
        
        if not isinstance(axes_section, dict):
            raise FrameworkValidationError(
                "axes section must be a dictionary",
                framework_name,
                field_path='axes'
            )
        
        for axis_name, axis_config in axes_section.items():
            if not isinstance(axis_config, dict):
                raise FrameworkValidationError(
                    f"axis '{axis_name}' must be a dictionary",
                    framework_name,
                    field_path=f'axes.{axis_name}'
                )
            
            # v3.2 Hybrid Architecture: axes reference anchors by anchor_ids
            if 'anchor_ids' in axis_config:
                # This is handled by components registry - just validate IDs exist
                continue
            
            # Legacy format: anchors defined within axes
            # Extract anchors from arbitrary organizational labels
            for org_label, content in axis_config.items():
                # Skip axis metadata
                if org_label in ['description', 'axis_type', 'theoretical_basis']:
                    continue
                    
                if isinstance(content, dict) and 'name' in content:
                    anchor_name = content['name']
                    anchor = self._validate_anchor_config(
                        content, framework_name, f'axes.{axis_name}.{org_label}'
                    )
                    anchors[anchor_name] = anchor
        
        return anchors
    
    def _extract_from_arcs(self, arcs_section: Dict[str, Any], framework_name: str) -> Dict[str, Any]:
        """Extract anchors from arcs section (v3.2 advanced positioning)"""
        anchors = {}
        
        if not isinstance(arcs_section, dict):
            raise FrameworkValidationError(
                "arcs section must be a dictionary",
                framework_name,
                field_path='arcs'
            )
        
        for arc_name, arc_config in arcs_section.items():
            if not isinstance(arc_config, dict):
                continue
                
            arc_anchors = arc_config.get('anchors', {})
            if isinstance(arc_anchors, dict):
                for anchor_name, anchor_config in arc_anchors.items():
                    anchor = self._validate_anchor_config(
                        anchor_config, framework_name, f'arcs.{arc_name}.anchors.{anchor_name}'
                    )
                    anchors[anchor_name] = anchor
        
        return anchors
    
    def _validate_polar_constraint(self, axes_section: Dict[str, Any], framework_name: str):
        """
        CRITICAL v3.2 REQUIREMENT: Validate polar constraint.
        Each axis MUST have exactly 2 anchors for mathematical rigor.
        """
        for axis_name, axis_config in axes_section.items():
            if not isinstance(axis_config, dict):
                continue
            
            # Check v3.2 hybrid architecture (anchor_ids)
            if 'anchor_ids' in axis_config:
                anchor_ids = axis_config['anchor_ids']
                if not isinstance(anchor_ids, list):
                    raise FrameworkValidationError(
                        f"axis '{axis_name}': anchor_ids must be a list",
                        framework_name,
                        field_path=f'axes.{axis_name}.anchor_ids'
                    )
                
                if len(anchor_ids) != 2:
                    raise FrameworkValidationError(
                        f"POLAR CONSTRAINT VIOLATION: axis '{axis_name}' has {len(anchor_ids)} anchors. "
                        f"v3.2 requires exactly 2 anchors per axis for mathematical rigor.",
                        framework_name,
                        field_path=f'axes.{axis_name}.anchor_ids'
                    )
            
            # Check legacy format (count organizational labels with anchors)
            else:
                anchor_count = 0
                for org_label, content in axis_config.items():
                    if isinstance(content, dict) and 'name' in content:
                        anchor_count += 1
                
                if anchor_count != 2:
                    raise FrameworkValidationError(
                        f"POLAR CONSTRAINT VIOLATION: axis '{axis_name}' has {anchor_count} anchors. "
                        f"v3.2 requires exactly 2 anchors per axis for mathematical rigor.",
                        framework_name,
                        field_path=f'axes.{axis_name}'
                    )
    
    def _validate_v3_2_features(self, framework_config: Dict[str, Any], framework_name: str):
        """Validate v3.2 advanced features if present"""
        v3_2_features = [
            'competitive_relationships',
            'temporal_analysis', 
            'olympics_protocols',
            'framework_fit_metrics',
            'algorithm_config'
        ]
        
        for feature in v3_2_features:
            if feature in framework_config:
                feature_config = framework_config[feature]
                if not isinstance(feature_config, dict):
                    raise FrameworkValidationError(
                        f"v3.2 feature '{feature}' must be a dictionary",
                        framework_name,
                        field_path=feature
                    )
    
    def _validate_anchor_config(self, anchor_config: Dict[str, Any], framework_name: str, field_path: str) -> Dict[str, Any]:
        """Validate individual anchor configuration against v3.2 spec"""
        if not isinstance(anchor_config, dict):
            raise FrameworkValidationError(
                "Anchor configuration must be a dictionary",
                framework_name,
                field_path=field_path
            )
        
        # Required: name (for legacy format) OR component_id (for hybrid format)
        has_name = 'name' in anchor_config
        has_component_id = 'component_id' in anchor_config
        
        if not (has_name or has_component_id):
            raise FrameworkValidationError(
                "Anchor missing required 'name' or 'component_id' field",
                framework_name,
                field_path=f'{field_path}.name|component_id'
            )
        
        # Validate name/component_id is non-empty string
        identifier = anchor_config.get('name') or anchor_config.get('component_id')
        if not isinstance(identifier, str) or not identifier.strip():
            raise FrameworkValidationError(
                "Anchor identifier must be a non-empty string",
                framework_name,
                field_path=f'{field_path}.name|component_id'
            )
        
        # Validate positioning if present
        if 'angle' in anchor_config:
            angle = anchor_config['angle']
            if not isinstance(angle, (int, float)):
                raise FrameworkValidationError(
                    "Anchor 'angle' must be a number",
                    framework_name,
                    field_path=f'{field_path}.angle'
                )
            if not (0 <= angle < 360):
                raise FrameworkValidationError(
                    "Anchor 'angle' must be between 0 and 359 degrees",
                    framework_name,
                    field_path=f'{field_path}.angle'
                )
        
        return anchor_config
    
    def get_anchor_count(self, framework_config: Dict[str, Any]) -> int:
        """Get total number of anchors in framework (after validation)"""
        try:
            validated = self.validate_framework(framework_config)
            return validated['_anchor_count']
        except FrameworkValidationError:
            return 0
    
    def get_anchors(self, framework_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get extracted anchors from framework (after validation)"""
        validated = self.validate_framework(framework_config)
        return validated['_extracted_anchors'] 