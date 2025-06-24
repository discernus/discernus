#!/usr/bin/env python3
"""
Unified Framework Validator v2.0
===============================

🎯 CONSOLIDATED VALIDATOR - Replaces all fragmented validation systems

Comprehensive framework validation supporting:
- ✅ Dipole-based frameworks (MFT style)
- ✅ Independent wells frameworks (Three Wells style) 
- ✅ YAML format (current standard)
- ✅ Legacy JSON format (migration support)
- ✅ CLI interface for manual validation
- ✅ Importable component for orchestrator integration

Validation Layers:
1. Format Detection & Parsing
2. Structural Validation (architecture-aware)
3. Semantic Consistency Checks
4. Academic Standards Validation
5. Integration & Compatibility Checks

Usage:
    # CLI Interface
    python scripts/utilities/unified_framework_validator.py framework_templates/moral_foundations_theory/
    python scripts/utilities/unified_framework_validator.py --all --verbose
    
    # Programmatic Interface  
    from scripts.utilities.unified_framework_validator import UnifiedFrameworkValidator
    validator = UnifiedFrameworkValidator()
    result = validator.validate_framework("framework_templates/moral_foundations_theory/")
"""

import os
import sys
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Union
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import re
import math

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

class FrameworkArchitecture(Enum):
    """Framework architecture types (Discernus Coordinates terminology)"""
    AXIS_SET = "axis_set"        # Paired coordinate axes (was dipole-based)
    ANCHOR_SET = "anchor_set"    # Independent coordinate points (was independent wells)
    UNKNOWN = "unknown"

class ValidationSeverity(Enum):
    """Validation issue severity levels"""
    ERROR = "error"
    WARNING = "warning"
    SUGGESTION = "suggestion"
    INFO = "info"

@dataclass
class ValidationIssue:
    """Individual validation issue"""
    severity: ValidationSeverity
    category: str
    message: str
    location: str = ""
    fix_suggestion: str = ""
    
    def __str__(self):
        icon = {"error": "❌", "warning": "⚠️", "suggestion": "💡", "info": "ℹ️"}[self.severity.value]
        location_str = f" ({self.location})" if self.location else ""
        return f"{icon} [{self.category}]{location_str} {self.message}"

@dataclass
class FrameworkValidationResult:
    """Comprehensive framework validation results"""
    framework_name: str
    framework_path: str
    architecture: FrameworkArchitecture
    format_type: str
    
    # Validation status
    is_valid: bool = True
    validation_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Issue tracking
    issues: List[ValidationIssue] = field(default_factory=list)
    
    # Layer-specific results
    format_validation_passed: bool = True
    structure_validation_passed: bool = True
    semantic_validation_passed: bool = True
    academic_validation_passed: bool = True
    integration_validation_passed: bool = True
    
    # Framework info
    framework_metadata: Dict = field(default_factory=dict)
    wells_count: int = 0
    dipoles_count: int = 0
    
    def add_issue(self, severity: ValidationSeverity, category: str, message: str, 
                  location: str = "", fix_suggestion: str = ""):
        """Add validation issue"""
        issue = ValidationIssue(severity, category, message, location, fix_suggestion)
        self.issues.append(issue)
        
        if severity == ValidationSeverity.ERROR:
            self.is_valid = False
    
    def get_issues_by_severity(self, severity: ValidationSeverity) -> List[ValidationIssue]:
        """Get issues of specific severity"""
        return [issue for issue in self.issues if issue.severity == severity]
    
    def get_summary(self) -> Dict[str, int]:
        """Get issue count summary"""
        return {
            "errors": len(self.get_issues_by_severity(ValidationSeverity.ERROR)),
            "warnings": len(self.get_issues_by_severity(ValidationSeverity.WARNING)),
            "suggestions": len(self.get_issues_by_severity(ValidationSeverity.SUGGESTION)),
            "info": len(self.get_issues_by_severity(ValidationSeverity.INFO))
        }

class UnifiedFrameworkValidator:
    """
    Unified framework validator supporting multiple architectures and formats.
    
    Consolidates all framework validation logic into single comprehensive system.
    """
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
        # Expected framework files by architecture (Discernus Coordinates)
        self.framework_file_patterns = {
            FrameworkArchitecture.AXIS_SET: [
                "*_framework.yaml",
                "framework.yaml", 
                "framework_consolidated.yaml"
            ],
            FrameworkArchitecture.ANCHOR_SET: [
                "*_framework.yaml",
                "framework.yaml", 
                "framework_consolidated.yaml"
            ]
        }
    
    def validate_framework(self, framework_path: Union[str, Path]) -> FrameworkValidationResult:
        """
        Main validation entry point.
        
        Args:
            framework_path: Path to framework directory or file
            
        Returns:
            FrameworkValidationResult with comprehensive validation results
        """
        framework_path = Path(framework_path)
        
        # Initialize result
        result = FrameworkValidationResult(
            framework_name=framework_path.name if framework_path.is_dir() else framework_path.stem,
            framework_path=str(framework_path),
            architecture=FrameworkArchitecture.UNKNOWN,
            format_type="unknown"
        )
        
        if self.verbose:
            print(f"🔍 Validating framework: {result.framework_name}")
        
        # 1. Format Detection & Loading
        framework_data = self._detect_and_load_framework(framework_path, result)
        if not framework_data:
            return result
        
        # 2. Architecture Detection
        result.architecture = self._detect_architecture(framework_data)
        if self.verbose:
            print(f"📐 Detected architecture: {result.architecture.value}")
        
        # 3. Layer-by-layer validation
        result.structure_validation_passed = self._validate_structure(framework_data, result)
        result.semantic_validation_passed = self._validate_semantics(framework_data, result)
        result.academic_validation_passed = self._validate_academic_standards(framework_data, result)
        result.integration_validation_passed = self._validate_integration(framework_data, result)
        
        # 4. Extract metadata
        self._extract_framework_metadata(framework_data, result)
        
        if self.verbose:
            summary = result.get_summary()
            print(f"📊 Validation complete: {summary['errors']} errors, {summary['warnings']} warnings")
        
        return result
    
    def _detect_and_load_framework(self, framework_path: Path, result: FrameworkValidationResult) -> Optional[Dict]:
        """Detect framework format and load data"""
        
        if framework_path.is_file():
            # Direct file path
            framework_file = framework_path
        else:
            # Directory - find framework file
            framework_file = self._find_framework_file(framework_path)
            if not framework_file:
                result.add_issue(
                    ValidationSeverity.ERROR,
                    "format_detection",
                    f"No framework file found in {framework_path}",
                    fix_suggestion="Ensure framework directory contains a framework file (*.yaml, framework.json, etc.)"
                )
                result.format_validation_passed = False
                return None
        
        # Load framework data
        try:
            if framework_file.suffix.lower() in ['.yaml', '.yml']:
                result.format_type = "yaml"
                with open(framework_file, 'r', encoding='utf-8') as f:
                    framework_data = yaml.safe_load(f)
            elif framework_file.suffix.lower() == '.json':
                result.format_type = "json"
                with open(framework_file, 'r', encoding='utf-8') as f:
                    framework_data = json.load(f)
            else:
                result.add_issue(
                    ValidationSeverity.ERROR,
                    "format_detection", 
                    f"Unsupported file format: {framework_file.suffix}",
                    fix_suggestion="Use .yaml, .yml, or .json format"
                )
                result.format_validation_passed = False
                return None
                
            if self.verbose:
                print(f"📄 Loaded {result.format_type.upper()} framework from {framework_file.name}")
            
            return framework_data
            
        except yaml.YAMLError as e:
            result.add_issue(
                ValidationSeverity.ERROR,
                "yaml_parsing",
                f"YAML parsing error: {e}",
                fix_suggestion="Check YAML syntax and formatting"
            )
            result.format_validation_passed = False
            return None
        except json.JSONDecodeError as e:
            result.add_issue(
                ValidationSeverity.ERROR,
                "json_parsing", 
                f"JSON parsing error: {e}",
                fix_suggestion="Check JSON syntax and formatting"
            )
            result.format_validation_passed = False
            return None
        except Exception as e:
            result.add_issue(
                ValidationSeverity.ERROR,
                "file_loading",
                f"Error loading framework file: {e}"
            )
            result.format_validation_passed = False
            return None
    
    def _find_framework_file(self, framework_dir: Path) -> Optional[Path]:
        """Find framework file in directory"""
        
        # Try all patterns in order of preference
        for architecture in FrameworkArchitecture:
            if architecture == FrameworkArchitecture.UNKNOWN:
                continue
            for pattern in self.framework_file_patterns[architecture]:
                matches = list(framework_dir.glob(pattern))
                if matches:
                    return matches[0]  # Return first match
        
        return None
    
    def _detect_architecture(self, framework_data: Dict) -> FrameworkArchitecture:
        """Detect framework architecture from data structure (Discernus Coordinates)"""
        
        # Check for anchor set structure (independent coordinate points)
        if 'anchors' in framework_data and isinstance(framework_data['anchors'], dict):
            anchors = framework_data['anchors']
            if anchors:
                # Check if anchors have independent coordinate structure
                first_anchor = list(anchors.values())[0]
                if isinstance(first_anchor, dict) and 'angle' in first_anchor:
                    return FrameworkArchitecture.ANCHOR_SET
        
        # Check for axis set structure (paired coordinate axes)
        if 'axes' in framework_data and isinstance(framework_data['axes'], dict):
            axes = framework_data['axes']
            if axes:
                # Check if axes have paired structure
                first_axis = list(axes.values())[0]
                if isinstance(first_axis, dict):
                    # Look for any valid axis pair types
                    pair_keys = ['positive', 'negative', 'integrative', 'disintegrative']
                    found_pairs = [key for key in pair_keys if key in first_axis]
                    if len(found_pairs) >= 2:
                        return FrameworkArchitecture.AXIS_SET
        
        return FrameworkArchitecture.UNKNOWN
    
    def _validate_structure(self, framework_data: Dict, result: FrameworkValidationResult) -> bool:
        """Validate framework structure based on detected architecture (Discernus Coordinates)"""
        
        is_valid = True
        
        if result.architecture == FrameworkArchitecture.ANCHOR_SET:
            is_valid = self._validate_anchor_set_structure(framework_data, result)
        elif result.architecture == FrameworkArchitecture.AXIS_SET:
            is_valid = self._validate_axis_set_structure(framework_data, result)
        else:
            result.add_issue(
                ValidationSeverity.ERROR,
                "structure_validation",
                "Unknown framework architecture - must use Discernus Coordinates structure (anchor-set or axis-set)",
                fix_suggestion="Convert framework to use 'anchors' (anchor-set) or 'axes' (axis-set) architecture"
            )
            is_valid = False
        
        return is_valid
    
    def _validate_anchor_set_structure(self, framework_data: Dict, result: FrameworkValidationResult) -> bool:
        """Validate anchor-set framework structure (independent coordinate points)"""
        is_valid = True
        
        # Required fields for anchor-set frameworks
        required_fields = ['name', 'anchors', 'coordinate_system']
        for field in required_fields:
            if field not in framework_data:
                result.add_issue(
                    ValidationSeverity.ERROR,
                    "structure_validation",
                    f"Missing required field: {field}",
                    location="root",
                    fix_suggestion=f"Add {field} field to framework definition"
                )
                is_valid = False
        
        # Validate anchors structure
        if 'anchors' in framework_data:
            anchors = framework_data['anchors']
            if not isinstance(anchors, dict):
                result.add_issue(
                    ValidationSeverity.ERROR,
                    "structure_validation",
                    "Anchors must be a dictionary",
                    location="anchors"
                )
                is_valid = False
            else:
                result.wells_count = len(anchors)  # anchors == coordinate points
                
                for anchor_name, anchor_data in anchors.items():
                    if not isinstance(anchor_data, dict):
                        result.add_issue(
                            ValidationSeverity.ERROR,
                            "structure_validation",
                            f"Anchor '{anchor_name}' must be an object",
                            location=f"anchors.{anchor_name}"
                        )
                        is_valid = False
                        continue
                    
                    # Check required anchor fields
                    required_anchor_fields = ['description', 'angle', 'weight', 'type']
                    for field in required_anchor_fields:
                        if field not in anchor_data:
                            result.add_issue(
                                ValidationSeverity.ERROR,
                                "structure_validation",
                                f"Anchor '{anchor_name}' missing required field: {field}",
                                location=f"anchors.{anchor_name}"
                            )
                            is_valid = False
                    
                    # Validate angle range
                    if 'angle' in anchor_data:
                        angle = anchor_data['angle']
                        if not isinstance(angle, (int, float)) or not (0 <= angle < 360):
                            result.add_issue(
                                ValidationSeverity.ERROR,
                                "structure_validation",
                                f"Anchor '{anchor_name}' angle must be numeric between 0-359",
                                location=f"anchors.{anchor_name}.angle"
                            )
                            is_valid = False
                    
                    # Validate weight
                    if 'weight' in anchor_data:
                        weight = anchor_data['weight']
                        if not isinstance(weight, (int, float)) or weight <= 0:
                            result.add_issue(
                                ValidationSeverity.ERROR,
                                "structure_validation",
                                f"Anchor '{anchor_name}' weight must be positive number",
                                location=f"anchors.{anchor_name}.weight"
                            )
                            is_valid = False
                    
                    # Validate type
                    if 'type' in anchor_data:
                        anchor_type = anchor_data['type']
                        valid_types = ['individualizing', 'binding', 'liberty_based', 'integrative', 'disintegrative']
                        if anchor_type not in valid_types:
                            result.add_issue(
                                ValidationSeverity.WARNING,
                                "structure_validation",
                                f"Anchor '{anchor_name}' has non-standard type: {anchor_type}",
                                location=f"anchors.{anchor_name}.type",
                                fix_suggestion=f"Consider using standard types: {', '.join(valid_types)}"
                            )
        
        return is_valid
    
    def _validate_axis_set_structure(self, framework_data: Dict, result: FrameworkValidationResult) -> bool:
        """Validate axis-set framework structure (paired coordinate axes)"""
        is_valid = True
        
        # Required fields for axis-set frameworks
        required_fields = ['name', 'axes', 'coordinate_system']
        for field in required_fields:
            if field not in framework_data:
                result.add_issue(
                    ValidationSeverity.ERROR,
                    "structure_validation",
                    f"Missing required field: {field}",
                    location="root",
                    fix_suggestion=f"Add {field} field to framework definition"
                )
                is_valid = False
        
        # Validate axes structure
        if 'axes' in framework_data:
            axes = framework_data['axes']
            if not isinstance(axes, dict):
                result.add_issue(
                    ValidationSeverity.ERROR,
                    "structure_validation",
                    "Axes must be a dictionary",
                    location="axes"
                )
                is_valid = False
            else:
                coordinate_count = 0
                
                for axis_name, axis_data in axes.items():
                    if not isinstance(axis_data, dict):
                        result.add_issue(
                            ValidationSeverity.ERROR,
                            "structure_validation",
                            f"Axis '{axis_name}' must be an object",
                            location=f"axes.{axis_name}"
                        )
                        is_valid = False
                        continue
                    
                    # Check for paired structure (positive/negative or integrative/disintegrative)
                    pair_keys = ['positive', 'negative', 'integrative', 'disintegrative']
                    found_pairs = [key for key in pair_keys if key in axis_data]
                    
                    if len(found_pairs) < 2:
                        result.add_issue(
                            ValidationSeverity.ERROR,
                            "structure_validation",
                            f"Axis '{axis_name}' must have paired coordinates (e.g., positive/negative)",
                            location=f"axes.{axis_name}",
                            fix_suggestion="Add paired coordinate definitions for this axis"
                        )
                        is_valid = False
                    else:
                        coordinate_count += len(found_pairs)
                
                result.wells_count = coordinate_count
        
        return is_valid
    

    
    def _validate_semantics(self, framework_data: Dict, result: FrameworkValidationResult) -> bool:
        """Validate semantic consistency (Discernus Coordinates)"""
        is_valid = True
        
        # Architecture-specific semantic validation
        if result.architecture == FrameworkArchitecture.ANCHOR_SET:
            is_valid = self._validate_anchor_set_semantics(framework_data, result)
        elif result.architecture == FrameworkArchitecture.AXIS_SET:
            is_valid = self._validate_axis_set_semantics(framework_data, result)
        
        return is_valid
    
    def _validate_anchor_set_semantics(self, framework_data: Dict, result: FrameworkValidationResult) -> bool:
        """Validate anchor-set framework semantics (independent coordinate points)"""
        is_valid = True
        
        if 'anchors' not in framework_data:
            return is_valid
        
        anchors = framework_data['anchors']
        angles = []
        
        for anchor_name, anchor_data in anchors.items():
            if not isinstance(anchor_data, dict):
                continue
            
            # Check angle uniqueness
            if 'angle' in anchor_data:
                angle = anchor_data['angle']
                if angle in angles:
                    result.add_issue(
                        ValidationSeverity.WARNING,
                        "semantic_validation",
                        f"Duplicate angle: {angle}° for anchor '{anchor_name}'",
                        location=f"anchors.{anchor_name}.angle",
                        fix_suggestion="Consider using unique angles for better coordinate distribution"
                    )
                angles.append(angle)
            
            # Validate language cues if present
            if 'language_cues' in anchor_data:
                cues = anchor_data['language_cues']
                if isinstance(cues, list):
                    if len(cues) < 3:
                        result.add_issue(
                            ValidationSeverity.WARNING,
                            "semantic_validation",
                            f"Anchor '{anchor_name}' has few language cues ({len(cues)})",
                            location=f"anchors.{anchor_name}.language_cues",
                            fix_suggestion="Consider adding more language cues for better detection"
                        )
                elif cues is not None:
                    result.add_issue(
                        ValidationSeverity.ERROR,
                        "semantic_validation",
                        f"Anchor '{anchor_name}' language_cues must be a list",
                        location=f"anchors.{anchor_name}.language_cues"
                    )
                    is_valid = False
        
        return is_valid
    
    def _validate_axis_set_semantics(self, framework_data: Dict, result: FrameworkValidationResult) -> bool:
        """Validate axis-set framework semantics (paired coordinate axes)"""
        is_valid = True
        
        if 'axes' not in framework_data:
            return is_valid
        
        axes = framework_data['axes']
        angles = []
        
        for axis_name, axis_data in axes.items():
            if not isinstance(axis_data, dict):
                continue
            
            # Validate paired coordinates
            pair_keys = ['positive', 'negative', 'integrative', 'disintegrative']
            for pair_key in pair_keys:
                if pair_key in axis_data:
                    coordinate_data = axis_data[pair_key]
                    if isinstance(coordinate_data, dict):
                        # Check angle uniqueness
                        if 'angle' in coordinate_data:
                            angle = coordinate_data['angle']
                            if angle in angles:
                                result.add_issue(
                                    ValidationSeverity.WARNING,
                                    "semantic_validation",
                                    f"Duplicate angle: {angle}° for {axis_name}.{pair_key}",
                                    location=f"axes.{axis_name}.{pair_key}.angle",
                                    fix_suggestion="Consider using unique angles for better coordinate distribution"
                                )
                            angles.append(angle)
                        
                        # Validate language cues if present
                        if 'language_cues' in coordinate_data:
                            cues = coordinate_data['language_cues']
                            if isinstance(cues, list):
                                if len(cues) < 3:
                                    result.add_issue(
                                        ValidationSeverity.WARNING,
                                        "semantic_validation",
                                        f"Coordinate '{axis_name}.{pair_key}' has few language cues ({len(cues)})",
                                        location=f"axes.{axis_name}.{pair_key}.language_cues",
                                        fix_suggestion="Consider adding more language cues for better detection"
                                    )
                            elif cues is not None:
                                result.add_issue(
                                    ValidationSeverity.ERROR,
                                    "semantic_validation",
                                    f"Coordinate '{axis_name}.{pair_key}' language_cues must be a list",
                                    location=f"axes.{axis_name}.{pair_key}.language_cues"
                                )
                                is_valid = False
        
        return is_valid
    
    def _validate_academic_standards(self, framework_data: Dict, result: FrameworkValidationResult) -> bool:
        """Validate academic rigor and standards"""
        is_valid = True
        
        # Check for theoretical foundation
        theoretical_found = False
        theoretical_locations = ['theoretical_foundation', 'framework_meta.theoretical_foundation']
        
        for location in theoretical_locations:
            if self._get_nested_value(framework_data, location):
                theoretical_found = True
                theoretical_data = self._get_nested_value(framework_data, location)
                
                # Validate academic components
                if isinstance(theoretical_data, dict):
                    if 'primary_sources' in theoretical_data:
                        sources = theoretical_data['primary_sources']
                        if isinstance(sources, list):
                            for i, source in enumerate(sources):
                                if not self._is_valid_citation(source):
                                    result.add_issue(
                                        ValidationSeverity.WARNING,
                                        "academic_validation",
                                        f"Citation {i+1} may not follow academic format",
                                        location=f"{location}.primary_sources[{i}]",
                                        fix_suggestion="Use standard academic citation format"
                                    )
                        else:
                            result.add_issue(
                                ValidationSeverity.WARNING,
                                "academic_validation",
                                "Primary sources should be a list",
                                location=f"{location}.primary_sources"
                            )
                    
                    if 'theoretical_approach' in theoretical_data:
                        approach = theoretical_data['theoretical_approach']
                        if isinstance(approach, str) and len(approach) < 100:
                            result.add_issue(
                                ValidationSeverity.SUGGESTION,
                                "academic_validation",
                                "Theoretical approach description is quite brief",
                                location=f"{location}.theoretical_approach",
                                fix_suggestion="Provide more detailed methodology description"
                            )
                break
        
        if not theoretical_found:
            result.add_issue(
                ValidationSeverity.WARNING,
                "academic_validation",
                "No theoretical foundation section found",
                fix_suggestion="Add theoretical_foundation section with primary sources and methodology"
            )
        
        # Check for version information
        version_found = False
        version_locations = ['version', 'framework_meta.version']
        
        for location in version_locations:
            if self._get_nested_value(framework_data, location):
                version_found = True
                break
        
        if not version_found:
            result.add_issue(
                ValidationSeverity.WARNING,
                "academic_validation",
                "No version information found",
                fix_suggestion="Add version field for reproducibility"
            )
        
        return is_valid
    
    def _validate_integration(self, framework_data: Dict, result: FrameworkValidationResult) -> bool:
        """Validate integration compatibility"""
        is_valid = True
        
        # Check for compatibility declarations
        if 'compatibility' not in framework_data:
            result.add_issue(
                ValidationSeverity.SUGGESTION,
                "integration_validation",
                "No compatibility section found",
                fix_suggestion="Add compatibility section for better integration support"
            )
        
        # Check for prompt configuration
        prompt_locations = ['prompt_configuration', 'prompt_config']
        prompt_found = any(self._get_nested_value(framework_data, loc) for loc in prompt_locations)
        
        if not prompt_found:
            result.add_issue(
                ValidationSeverity.SUGGESTION,
                "integration_validation",
                "No prompt configuration found",
                fix_suggestion="Add prompt_configuration section for LLM integration"
            )
        
        return is_valid
    
    def _extract_framework_metadata(self, framework_data: Dict, result: FrameworkValidationResult):
        """Extract framework metadata for result"""
        
        # Extract basic metadata
        metadata = {}
        
        # Name
        name_locations = ['name', 'framework_meta.name', 'framework_name']
        for location in name_locations:
            name = self._get_nested_value(framework_data, location)
            if name:
                metadata['name'] = name
                break
        
        # Version
        version_locations = ['version', 'framework_meta.version']
        for location in version_locations:
            version = self._get_nested_value(framework_data, location)
            if version:
                metadata['version'] = version
                break
        
        # Description
        desc_locations = ['description', 'framework_meta.description']
        for location in desc_locations:
            desc = self._get_nested_value(framework_data, location)
            if desc:
                metadata['description'] = desc
                break
        
        # Architecture-specific metadata (Discernus Coordinates)
        if result.architecture == FrameworkArchitecture.ANCHOR_SET:
            if 'anchors' in framework_data:
                metadata['anchors'] = len(framework_data['anchors'])
                metadata['coordinate_points'] = len(framework_data['anchors'])  # Independent coordinate points
        elif result.architecture == FrameworkArchitecture.AXIS_SET:
            if 'axes' in framework_data:
                metadata['axes'] = len(framework_data['axes'])
                # Count total coordinate points from all axes
                coordinate_count = 0
                for axis_data in framework_data['axes'].values():
                    if isinstance(axis_data, dict):
                        coordinate_count += len([k for k in ['positive', 'negative', 'integrative', 'disintegrative'] if k in axis_data])
                metadata['coordinate_points'] = coordinate_count
        
        result.framework_metadata = metadata
    
    def _get_nested_value(self, data: Dict, path: str) -> Any:
        """Get nested dictionary value using dot notation"""
        keys = path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current
    
    def _is_valid_citation(self, citation: str) -> bool:
        """Basic citation format validation"""
        if not isinstance(citation, str) or len(citation) < 20:
            return False
        
        # Basic heuristics
        has_author = bool(re.search(r'[A-Z][a-z]+', citation[:30]))
        has_year = bool(re.search(r'(19|20)\d{2}', citation))
        has_punctuation = bool(re.search(r'[.,():]', citation))
        
        return has_author and has_year and has_punctuation
    
    def validate_all_frameworks(self, frameworks_dir: str = "frameworks") -> List[FrameworkValidationResult]:
        """Validate all frameworks in directory"""
        frameworks_path = Path(frameworks_dir)
        results = []
        
        if not frameworks_path.exists():
            print(f"❌ Frameworks directory not found: {frameworks_path}")
            return results
        
        print(f"🔍 Validating all frameworks in {frameworks_path}")
        
        for framework_dir in frameworks_path.iterdir():
            if framework_dir.is_dir() and not framework_dir.name.startswith('.'):
                if self.verbose:
                    print(f"\n{'='*60}")
                    print(f"🔍 Validating: {framework_dir.name}")
                
                result = self.validate_framework(framework_dir)
                results.append(result)
                
                # Print summary for each framework
                if not self.verbose:
                    status = "✅ PASS" if result.is_valid else "❌ FAIL"
                    summary = result.get_summary()
                    print(f"{status} {framework_dir.name} ({summary['errors']} errors, {summary['warnings']} warnings)")
        
        return results

def print_validation_report(result: FrameworkValidationResult, verbose: bool = False):
    """Print comprehensive validation report"""
    
    print(f"\n{'='*70}")
    print(f"🎯 Framework Validation Report: {result.framework_name}")
    print(f"{'='*70}")
    
    # Basic info
    print(f"📁 Path: {result.framework_path}")
    print(f"📐 Architecture: {result.architecture.value}")
    print(f"📄 Format: {result.format_type}")
    
    # Use new Discernus Coordinates terminology
    if result.architecture == FrameworkArchitecture.AXIS_SET:
        # For axis_set, show both coordinate points and axes count
        axes_count = result.framework_metadata.get('axes', 0)
        print(f"📊 Anchors: {result.wells_count}, Axes: {axes_count}")
    elif result.architecture == FrameworkArchitecture.ANCHOR_SET:
        print(f"📊 Anchors: {result.wells_count}")
    else:
        print(f"📊 Coordinate Points: {result.wells_count}")
    
    print(f"⏰ Validated: {result.validation_timestamp}")
    
    # Overall status
    status_icon = "✅" if result.is_valid else "❌"
    print(f"\n{status_icon} Overall Status: {'VALID' if result.is_valid else 'INVALID'}")
    
    # Layer status
    print(f"\n📋 Validation Layers:")
    layers = [
        ("Format", result.format_validation_passed),
        ("Structure", result.structure_validation_passed),
        ("Semantics", result.semantic_validation_passed),
        ("Academic", result.academic_validation_passed),
        ("Integration", result.integration_validation_passed)
    ]
    
    for layer_name, passed in layers:
        icon = "✅" if passed else "❌"
        print(f"  {icon} {layer_name}")
    
    # Issue summary
    summary = result.get_summary()
    if any(summary.values()):
        print(f"\n📊 Issue Summary:")
        if summary['errors']:
            print(f"  ❌ {summary['errors']} errors")
        if summary['warnings']:
            print(f"  ⚠️ {summary['warnings']} warnings") 
        if summary['suggestions']:
            print(f"  💡 {summary['suggestions']} suggestions")
        if summary['info']:
            print(f"  ℹ️ {summary['info']} info")
    
    # Detailed issues
    if result.issues and (verbose or summary['errors'] > 0):
        print(f"\n📝 Detailed Issues:")
        
        for severity in [ValidationSeverity.ERROR, ValidationSeverity.WARNING, ValidationSeverity.SUGGESTION, ValidationSeverity.INFO]:
            issues = result.get_issues_by_severity(severity)
            if issues:
                severity_name = severity.value.upper()
                print(f"\n{severity.value.upper()}S:")
                
                for i, issue in enumerate(issues, 1):
                    print(f"  {i}. {issue}")
                    if verbose and issue.fix_suggestion:
                        print(f"     💡 Fix: {issue.fix_suggestion}")
    
    # Framework metadata
    if verbose and result.framework_metadata:
        print(f"\n📋 Framework Metadata:")
        for key, value in result.framework_metadata.items():
            print(f"  {key}: {value}")

def print_summary_report(results: List[FrameworkValidationResult]):
    """Print summary report for multiple frameworks"""
    
    if not results:
        print("No frameworks validated.")
        return
    
    print(f"\n{'='*70}")
    print(f"📊 VALIDATION SUMMARY REPORT")
    print(f"{'='*70}")
    
    total = len(results)
    valid = sum(1 for r in results if r.is_valid)
    invalid = total - valid
    
    print(f"📈 Overview:")
    print(f"  Total frameworks: {total}")
    print(f"  ✅ Valid: {valid}")
    print(f"  ❌ Invalid: {invalid}")
    print(f"  📊 Success rate: {(valid/total)*100:.1f}%")
    
    # Architecture breakdown
    arch_counts = {}
    for result in results:
        arch = result.architecture.value
        arch_counts[arch] = arch_counts.get(arch, 0) + 1
    
    print(f"\n📐 Architecture Distribution:")
    for arch, count in arch_counts.items():
        print(f"  {arch}: {count}")
    
    # Top issues
    all_issues = []
    for result in results:
        all_issues.extend(result.issues)
    
    if all_issues:
        # Count issues by category
        issue_counts = {}
        for issue in all_issues:
            key = f"{issue.severity.value}:{issue.category}"
            issue_counts[key] = issue_counts.get(key, 0) + 1
        
        print(f"\n🔍 Common Issues:")
        sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
        for issue_key, count in sorted_issues[:10]:  # Top 10
            severity, category = issue_key.split(':', 1)
            icon = {"error": "❌", "warning": "⚠️", "suggestion": "💡", "info": "ℹ️"}[severity]
            print(f"  {icon} {category}: {count} occurrences")
    
    # Failed frameworks
    if invalid > 0:
        print(f"\n❌ Failed Frameworks:")
        for result in results:
            if not result.is_valid:
                error_count = len(result.get_issues_by_severity(ValidationSeverity.ERROR))
                print(f"  • {result.framework_name} ({error_count} errors)")

def main():
    """CLI main function"""
    parser = argparse.ArgumentParser(
        description="Unified Framework Validator v2.0 - Comprehensive framework validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Validate single framework:
    python scripts/utilities/unified_framework_validator.py framework_templates/moral_foundations_theory/
    
  Validate specific framework file:
    python scripts/utilities/unified_framework_validator.py framework_templates/moral_foundations_theory/moral_foundations_theory_founding_template.yaml
    
  Validate all frameworks:
    python scripts/utilities/unified_framework_validator.py --all
    
  Verbose output with detailed suggestions:
    python scripts/utilities/unified_framework_validator.py --all --verbose
    
  Generate summary report:
    python scripts/utilities/unified_framework_validator.py --all --summary
        """
    )
    
    parser.add_argument(
        "framework_path",
        nargs="?",
        help="Path to framework directory or file to validate"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all frameworks in frameworks/ directory"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed validation output and suggestions"
    )
    
    parser.add_argument(
        "--summary",
        action="store_true", 
        help="Show summary report after validation"
    )
    
    parser.add_argument(
        "--frameworks-dir",
        default="framework_templates",
        help="Directory containing framework templates (default: framework_templates)"
    )
    
    args = parser.parse_args()
    
    if not args.framework_path and not args.all:
        parser.print_help()
        sys.exit(1)
    
    print("🎯 Unified Framework Validator v2.0")
    print("="*50)
    
    # Initialize validator
    validator = UnifiedFrameworkValidator(verbose=args.verbose)
    
    if args.all:
        # Validate all frameworks
        results = validator.validate_all_frameworks(args.frameworks_dir)
        
        if args.verbose:
            # Print detailed reports
            for result in results:
                print_validation_report(result, verbose=True)
        
        if args.summary or not args.verbose:
            print_summary_report(results)
        
        # Exit with error code if any validation failed
        if any(not r.is_valid for r in results):
            sys.exit(1)
    
    else:
        # Validate single framework
        result = validator.validate_framework(args.framework_path)
        print_validation_report(result, verbose=args.verbose)
        
        # Exit with error code if validation failed
        if not result.is_valid:
            sys.exit(1)

if __name__ == "__main__":
    main() 