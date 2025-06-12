#!/usr/bin/env python3
"""
Framework Specification Validator v2.0
======================================

Validates framework configurations against the formal Framework Specification v2.0.
Provides structural, semantic, and academic validation with detailed reporting.

Usage:
    python scripts/validate_framework_spec.py frameworks/civic_virtue/framework.json
    python scripts/validate_framework_spec.py --all
    python scripts/validate_framework_spec.py --framework civic_virtue --fix-issues
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
import jsonschema
from jsonschema import validate, ValidationError, Draft202012Validator

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class FrameworkValidationResult:
    """Results of framework validation."""
    
    def __init__(self, framework_name: str):
        self.framework_name = framework_name
        self.is_valid = True
        self.errors = []
        self.warnings = []
        self.suggestions = []
        self.schema_validation_passed = False
        self.semantic_validation_passed = False
        self.academic_validation_passed = False
        
    def add_error(self, category: str, message: str, fix_suggestion: str = None):
        """Add validation error."""
        self.is_valid = False
        self.errors.append({
            'category': category,
            'message': message,
            'fix_suggestion': fix_suggestion
        })
        
    def add_warning(self, category: str, message: str, suggestion: str = None):
        """Add validation warning."""
        self.warnings.append({
            'category': category,
            'message': message,
            'suggestion': suggestion
        })
        
    def add_suggestion(self, category: str, message: str):
        """Add improvement suggestion."""
        self.suggestions.append({
            'category': category,
            'message': message
        })

class FrameworkSpecValidator:
    """Comprehensive framework specification validator."""
    
    def __init__(self, schema_path: str = None):
        self.schema_path = schema_path or "schemas/framework_v2.0.json"
        self.schema = self._load_schema()
        
    def _load_schema(self) -> Dict[str, Any]:
        """Load the framework specification schema."""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Schema file not found: {self.schema_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in schema file: {e}")
            sys.exit(1)
    
    def validate_framework(self, framework_path: str) -> FrameworkValidationResult:
        """Comprehensive framework validation."""
        framework_name = Path(framework_path).parent.name
        result = FrameworkValidationResult(framework_name)
        
        # Load framework data
        try:
            with open(framework_path, 'r') as f:
                framework_data = json.load(f)
        except FileNotFoundError:
            result.add_error("file_access", f"Framework file not found: {framework_path}")
            return result
        except json.JSONDecodeError as e:
            result.add_error("json_syntax", f"Invalid JSON syntax: {e}")
            return result
        
        # 1. Schema validation
        result.schema_validation_passed = self._validate_schema(framework_data, result)
        
        # 2. Semantic validation
        if result.schema_validation_passed:
            result.semantic_validation_passed = self._validate_semantics(framework_data, result)
        
        # 3. Academic validation
        if result.schema_validation_passed:
            result.academic_validation_passed = self._validate_academic_rigor(framework_data, result)
        
        # 4. Best practices check
        self._check_best_practices(framework_data, result)
        
        return result
    
    def _validate_schema(self, framework_data: Dict[str, Any], result: FrameworkValidationResult) -> bool:
        """Validate against JSON schema."""
        try:
            validator = Draft202012Validator(self.schema)
            validator.validate(framework_data)
            return True
        except ValidationError as e:
            # Parse validation error for user-friendly message
            error_path = " -> ".join(str(p) for p in e.absolute_path) if e.absolute_path else "root"
            result.add_error(
                "schema_validation",
                f"Schema validation failed at {error_path}: {e.message}",
                self._get_schema_fix_suggestion(e)
            )
            return False
        except Exception as e:
            result.add_error("schema_validation", f"Schema validation error: {e}")
            return False
    
    def _validate_semantics(self, framework_data: Dict[str, Any], result: FrameworkValidationResult) -> bool:
        """Validate semantic consistency."""
        is_valid = True
        
        # Check well angle uniqueness
        wells = framework_data.get('wells', {})
        angles = [well['angle'] for well in wells.values()]
        if len(angles) != len(set(angles)):
            result.add_error(
                "semantic_validation",
                "Duplicate well angles found - each well must have unique angular position",
                "Ensure all wells have different angle values"
            )
            is_valid = False
        
        # Check cluster span consistency
        positioning = framework_data.get('positioning_strategy', {})
        clusters = {}  # Initialize clusters variable
        if positioning.get('type') == 'clustered_positioning':
            clusters = positioning.get('clusters', {})
            total_span = sum(cluster['span'] for cluster in clusters.values())
            if total_span > 360:
                result.add_error(
                    "semantic_validation",
                    f"Total cluster span ({total_span}°) exceeds 360°",
                    "Reduce cluster spans or use overlapping clusters"
                )
                is_valid = False
        
        # Check well type consistency with clusters
        if clusters:
            cluster_types = set()
            for cluster in clusters.values():
                cluster_types.update(cluster['well_types'])
            
            well_types = set(well['type'] for well in wells.values())
            missing_types = well_types - cluster_types
            if missing_types:
                result.add_warning(
                    "semantic_validation",
                    f"Well types not covered by clusters: {missing_types}",
                    "Add cluster coverage for all well types or update positioning strategy"
                )
        
        # Check weight distribution
        weights = [well['weight'] for well in wells.values()]
        if max(weights) / min(weights) > 5.0:
            result.add_warning(
                "semantic_validation",
                f"Large weight variation (max/min = {max(weights)/min(weights):.1f})",
                "Consider more balanced weight distribution for better analysis"
            )
        
        return is_valid
    
    def _validate_academic_rigor(self, framework_data: Dict[str, Any], result: FrameworkValidationResult) -> bool:
        """Validate academic foundation."""
        is_valid = True
        
        theoretical = framework_data.get('theoretical_foundation', {})
        
        # Check citation format
        sources = theoretical.get('primary_sources', [])
        for i, source in enumerate(sources):
            if not self._is_valid_citation(source):
                result.add_warning(
                    "academic_validation",
                    f"Citation {i+1} may not follow academic format: {source[:50]}...",
                    "Use standard academic citation format (APA, MLA, or Chicago)"
                )
        
        # Check theoretical approach depth
        approach = theoretical.get('theoretical_approach', '')
        if len(approach) < 200:
            result.add_warning(
                "academic_validation",
                "Theoretical approach description is quite brief",
                "Provide more detailed methodology and theoretical grounding"
            )
        
        # Check for validation studies
        if not theoretical.get('validation_studies'):
            result.add_suggestion(
                "academic_validation",
                "Consider adding empirical validation studies to strengthen framework credibility"
            )
        
        # Check well descriptions
        wells = framework_data.get('wells', {})
        for well_name, well_data in wells.items():
            description = well_data.get('description', '')
            if len(description) < 50:
                result.add_warning(
                    "academic_validation",
                    f"Well '{well_name}' has brief description",
                    "Provide more detailed academic definition and theoretical basis"
                )
        
        return is_valid
    
    def _check_best_practices(self, framework_data: Dict[str, Any], result: FrameworkValidationResult):
        """Check adherence to best practices."""
        
        # Check for color accessibility
        colors = framework_data.get('well_type_colors', {})
        if colors:
            for type_name, color in colors.items():
                if not self._is_accessible_color(color):
                    result.add_suggestion(
                        "best_practices",
                        f"Color {color} for type '{type_name}' may not be accessible"
                    )
        
        # Check metric definitions
        metrics = framework_data.get('metrics', {})
        for metric_code, metric_data in metrics.items():
            if not metric_data.get('formula'):
                result.add_suggestion(
                    "best_practices",
                    f"Metric '{metric_code}' lacks mathematical formula"
                )
            if not metric_data.get('interpretation'):
                result.add_suggestion(
                    "best_practices",
                    f"Metric '{metric_code}' lacks interpretation guidance"
                )
        
        # Check compatibility declarations
        compatibility = framework_data.get('compatibility', {})
        if not compatibility:
            result.add_suggestion(
                "best_practices",
                "Consider adding compatibility declarations for better interoperability"
            )
    
    def _is_valid_citation(self, citation: str) -> bool:
        """Basic citation format validation."""
        # Simple heuristics for citation validation
        has_author = any(char.isupper() for char in citation[:20])
        has_year = any(year in citation for year in [str(y) for y in range(1900, 2030)])
        has_punctuation = any(punct in citation for punct in ['.', ',', '(', ')'])
        return has_author and has_year and has_punctuation
    
    def _is_accessible_color(self, hex_color: str) -> bool:
        """Check if color meets accessibility guidelines."""
        # Convert hex to RGB and check contrast (simplified)
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16) 
            b = int(hex_color[5:7], 16)
            # Simple luminance check
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return 0.2 < luminance < 0.8  # Avoid very dark or very light colors
        except:
            return False
    
    def _get_schema_fix_suggestion(self, error: ValidationError) -> str:
        """Generate fix suggestion for schema validation error."""
        if "required" in error.message:
            return f"Add the required field: {error.message.split()[-1]}"
        elif "pattern" in error.message:
            return "Check the format requirements in the schema documentation"
        elif "minimum" in error.message or "maximum" in error.message:
            return "Adjust the value to be within the allowed range"
        else:
            return "Check the schema documentation for correct format"

def print_validation_report(result: FrameworkValidationResult, verbose: bool = False):
    """Print formatted validation report."""
    print(f"\n🔍 Framework Validation Report: {result.framework_name}")
    print("=" * 60)
    
    # Overall status
    if result.is_valid:
        print("✅ VALIDATION PASSED")
    else:
        print("❌ VALIDATION FAILED")
    
    # Component status
    print(f"\n📋 Component Status:")
    print(f"  Schema Validation:   {'✅' if result.schema_validation_passed else '❌'}")
    print(f"  Semantic Validation: {'✅' if result.semantic_validation_passed else '❌'}")
    print(f"  Academic Validation: {'✅' if result.academic_validation_passed else '❌'}")
    
    # Errors
    if result.errors:
        print(f"\n❌ Errors ({len(result.errors)}):")
        for i, error in enumerate(result.errors, 1):
            print(f"  {i}. [{error['category']}] {error['message']}")
            if error.get('fix_suggestion') and verbose:
                print(f"     💡 Fix: {error['fix_suggestion']}")
    
    # Warnings
    if result.warnings:
        print(f"\n⚠️  Warnings ({len(result.warnings)}):")
        for i, warning in enumerate(result.warnings, 1):
            print(f"  {i}. [{warning['category']}] {warning['message']}")
            if warning.get('suggestion') and verbose:
                print(f"     💡 Suggestion: {warning['suggestion']}")
    
    # Suggestions
    if result.suggestions and verbose:
        print(f"\n💡 Improvement Suggestions ({len(result.suggestions)}):")
        for i, suggestion in enumerate(result.suggestions, 1):
            print(f"  {i}. [{suggestion['category']}] {suggestion['message']}")

def validate_all_frameworks(validator: FrameworkSpecValidator, verbose: bool = False) -> List[FrameworkValidationResult]:
    """Validate all frameworks in the frameworks directory."""
    frameworks_dir = Path("frameworks")
    results = []
    
    if not frameworks_dir.exists():
        print("❌ Frameworks directory not found")
        return results
    
    for framework_dir in frameworks_dir.iterdir():
        if framework_dir.is_dir():
            framework_file = framework_dir / "framework.json"
            if framework_file.exists():
                print(f"\n🔍 Validating {framework_dir.name}...")
                result = validator.validate_framework(str(framework_file))
                results.append(result)
                print_validation_report(result, verbose)
            else:
                print(f"⚠️  No framework.json found in {framework_dir.name}")
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Validate framework specifications against v2.0 schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Validate single framework:
    python scripts/validate_framework_spec.py frameworks/civic_virtue/framework.json
    
  Validate all frameworks:
    python scripts/validate_framework_spec.py --all
    
  Verbose output with suggestions:
    python scripts/validate_framework_spec.py --all --verbose
    
  Generate summary report:
    python scripts/validate_framework_spec.py --all --summary
        """
    )
    
    parser.add_argument(
        "framework_file",
        nargs="?",
        help="Path to framework.json file to validate"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all frameworks in frameworks/ directory"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed suggestions and fix recommendations"
    )
    
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show summary report of all validations"
    )
    
    parser.add_argument(
        "--schema",
        default="schemas/framework_v2.0.json",
        help="Path to framework schema file"
    )
    
    args = parser.parse_args()
    
    if not args.framework_file and not args.all:
        parser.print_help()
        sys.exit(1)
    
    # Initialize validator
    validator = FrameworkSpecValidator(args.schema)
    
    print("🎯 Framework Specification Validator v2.0")
    print(f"📋 Using schema: {args.schema}")
    
    if args.all:
        # Validate all frameworks
        results = validate_all_frameworks(validator, args.verbose)
        
        if args.summary:
            # Print summary
            print(f"\n📊 VALIDATION SUMMARY")
            print("=" * 40)
            total = len(results)
            passed = sum(1 for r in results if r.is_valid)
            failed = total - passed
            
            print(f"Total frameworks: {total}")
            print(f"Passed: {passed} ✅")
            print(f"Failed: {failed} ❌")
            
            if failed > 0:
                print(f"\nFailed frameworks:")
                for result in results:
                    if not result.is_valid:
                        print(f"  • {result.framework_name} ({len(result.errors)} errors)")
    
    else:
        # Validate single framework
        result = validator.validate_framework(args.framework_file)
        print_validation_report(result, args.verbose)
        
        # Exit with error code if validation failed
        if not result.is_valid:
            sys.exit(1)

if __name__ == "__main__":
    main() 