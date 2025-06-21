#!/usr/bin/env python3
"""
Comprehensive Experimental Specification Validator for Academic Research

⚠️ DEPRECATED: This validator has been replaced by experiment_validation_utils.py.

Use scripts/applications/experiment_validation_utils.py instead.

This legacy validator is not integrated into the production orchestrator and duplicates
functionality already available in the production pipeline:

REPLACEMENT SYSTEM:
- scripts/applications/experiment_validation_utils.py (production system)
- Used by: comprehensive_experiment_orchestrator.py
- Features: Clear error messages, actionable guidance, structured validation reporting

MIGRATION:
- The orchestrator uses experiment_validation_utils.ExperimentValidator
- No code changes needed - this system was not being used in production

For new development, use the integrated validation system:
    from scripts.applications.experiment_validation_utils import ExperimentValidator

Validates experiment definitions for:
- Academic compliance and institutional requirements
- Complete experimental design specification
- Statistical hypothesis validation
- Corpus and component specifications
- Research ethics and reproducibility requirements

Supports both YAML and JSON formats with automatic conversion.
"""

import json
import yaml
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import re

@dataclass
class ValidationResult:
    """Result of experiment validation"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    academic_compliance: Dict[str, bool] = field(default_factory=dict)

class ExperimentSpecValidator:
    """Comprehensive validator for academic experiment specifications"""
    
    def __init__(self):
        self.required_fields = {
            'experiment_meta': [
                'name', 'description', 'version', 'created',
                'hypotheses', 'research_context', 'success_criteria'
            ],
            'components': [
                'frameworks', 'prompt_templates', 'weighting_schemes', 'models', 'corpus'
            ],
            'execution': [
                'description', 'cost_controls', 'quality_assurance'
            ]
        }
        
        self.academic_fields = [
            'principal_investigator', 'institution', 'ethical_clearance', 
            'funding_source', 'publication_intent'
        ]
        
        self.statistical_fields = [
            'statistical_validation_study', 'hypothesis_validation_criteria'
        ]
    
    def validate_experiment(self, experiment_file: Path) -> ValidationResult:
        """Main validation method"""
        result = ValidationResult(is_valid=True)
        
        try:
            # Step 1: Load and convert if needed
            experiment_data = self._load_experiment_file(experiment_file)
            
            # Step 2: Schema validation
            self._validate_schema(experiment_data, result)
            
            # Step 3: Academic compliance validation
            self._validate_academic_compliance(experiment_data, result)
            
            # Step 4: Statistical design validation
            self._validate_statistical_design(experiment_data, result)
            
            # Step 5: Experimental design validation
            self._validate_experimental_design(experiment_data, result)
            
            # Step 6: Component specification validation
            self._validate_component_specifications(experiment_data, result)
            
            # Step 7: Research ethics validation
            self._validate_research_ethics(experiment_data, result)
            
            # Step 8: Reproducibility validation
            self._validate_reproducibility_requirements(experiment_data, result)
            
            # Final validation status
            result.is_valid = len(result.errors) == 0
            
        except Exception as e:
            result.is_valid = False
            result.errors.append(f"Critical validation error: {str(e)}")
        
        return result
    
    def _load_experiment_file(self, experiment_file: Path) -> Dict[str, Any]:
        """Load experiment file (YAML or JSON) with automatic conversion"""
        if not experiment_file.exists():
            raise FileNotFoundError(f"Experiment file not found: {experiment_file}")
        
        file_content = experiment_file.read_text(encoding='utf-8')
        
        # Determine format and parse
        if experiment_file.suffix.lower() in ['.yaml', '.yml']:
            try:
                data = yaml.safe_load(file_content)
                print(f"✅ Loaded YAML experiment definition: {experiment_file}")
                return data
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML format: {e}")
        
        elif experiment_file.suffix.lower() == '.json':
            try:
                data = json.loads(file_content)
                print(f"✅ Loaded JSON experiment definition: {experiment_file}")
                return data
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format: {e}")
        
        else:
            # Try to detect format by content
            try:
                data = yaml.safe_load(file_content)
                print(f"✅ Auto-detected YAML format: {experiment_file}")
                return data
            except:
                try:
                    data = json.loads(file_content)
                    print(f"✅ Auto-detected JSON format: {experiment_file}")
                    return data
                except:
                    raise ValueError(f"Could not parse file as YAML or JSON: {experiment_file}")
    
    def convert_yaml_to_json(self, yaml_file: Path, output_file: Optional[Path] = None) -> Path:
        """Convert YAML experiment to JSON for orchestrator"""
        experiment_data = self._load_experiment_file(yaml_file)
        
        if output_file is None:
            output_file = yaml_file.with_suffix('.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(experiment_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Converted {yaml_file} → {output_file}")
        return output_file
    
    def _validate_schema(self, data: Dict[str, Any], result: ValidationResult):
        """Validate basic schema structure"""
        # Check top-level sections
        for section in self.required_fields:
            if section not in data:
                result.errors.append(f"Missing required section: '{section}'")
                continue
            
            # Check required fields within each section
            section_data = data[section]
            for field in self.required_fields[section]:
                if field not in section_data:
                    result.errors.append(f"Missing required field: '{section}.{field}'")
        
        # Validate experiment metadata
        if 'experiment_meta' in data:
            meta = data['experiment_meta']
            
            # Validate hypotheses format
            if 'hypotheses' in meta and isinstance(meta['hypotheses'], list):
                if len(meta['hypotheses']) == 0:
                    result.warnings.append("No hypotheses specified - consider adding research hypotheses")
                
                for i, hypothesis in enumerate(meta['hypotheses']):
                    if not isinstance(hypothesis, str) or len(hypothesis.strip()) < 10:
                        result.errors.append(f"Hypothesis {i+1} is too short or invalid format")
            
            # Validate success criteria
            if 'success_criteria' in meta and isinstance(meta['success_criteria'], list):
                if len(meta['success_criteria']) == 0:
                    result.warnings.append("No success criteria specified - recommended for academic research")
    
    def _validate_academic_compliance(self, data: Dict[str, Any], result: ValidationResult):
        """Validate academic and institutional compliance"""
        experiment_meta = data.get('experiment_meta', {})
        
        # Track academic compliance
        for field in self.academic_fields:
            has_field = field in experiment_meta and experiment_meta[field]
            result.academic_compliance[field] = has_field
            
            if not has_field:
                if field == 'ethical_clearance':
                    result.warnings.append("No ethical clearance specified - may be required for publication")
                elif field == 'principal_investigator':
                    result.warnings.append("No principal investigator specified - recommended for academic work")
                elif field == 'institution':
                    result.warnings.append("No institution specified - recommended for academic work")
        
        # Check for publication readiness
        if experiment_meta.get('publication_intent'):
            missing_pub_requirements = []
            if not experiment_meta.get('principal_investigator'):
                missing_pub_requirements.append('principal_investigator')
            if not experiment_meta.get('institution'):
                missing_pub_requirements.append('institution')
            if not experiment_meta.get('ethical_clearance'):
                missing_pub_requirements.append('ethical_clearance')
            
            if missing_pub_requirements:
                result.warnings.append(
                    f"Publication intent specified but missing: {', '.join(missing_pub_requirements)}"
                )
    
    def _validate_statistical_design(self, data: Dict[str, Any], result: ValidationResult):
        """Validate statistical design and hypothesis testing"""
        experiment_meta = data.get('experiment_meta', {})
        
        # Check for statistical validation requirements
        if 'hypothesis_validation_criteria' in data.get('success_validation', {}):
            criteria = data['success_validation']['hypothesis_validation_criteria']
            
            # Validate hypothesis structure
            for h_key, h_criteria in criteria.items():
                if not h_key.startswith('h') and not h_key.startswith('H'):
                    result.warnings.append(f"Hypothesis key '{h_key}' doesn't follow H1/H2/H3 convention")
                
                # Check for statistical thresholds
                if isinstance(h_criteria, dict):
                    has_statistical_test = any('p_value' in str(k) or 'significance' in str(k) 
                                             for k in h_criteria.keys())
                    if not has_statistical_test:
                        result.suggestions.append(
                            f"Consider adding statistical significance criteria for {h_key}"
                        )
        
        # Check for power analysis or sample size considerations
        corpus_count = len(data.get('components', {}).get('corpus', []))
        if corpus_count > 0:
            if corpus_count < 10:
                result.warnings.append(
                    f"Small corpus size ({corpus_count} texts) may limit statistical power"
                )
            elif corpus_count > 100:
                result.suggestions.append(
                    "Large corpus - consider power analysis to optimize sample size"
                )
    
    def _validate_experimental_design(self, data: Dict[str, Any], result: ValidationResult):
        """Validate experimental design completeness"""
        execution = data.get('execution', {})
        
        # Check quality assurance settings
        qa = execution.get('quality_assurance', {})
        if not qa.get('enable_qa_validation'):
            result.warnings.append("Quality assurance disabled - recommended for research reliability")
        
        if qa.get('qa_confidence_threshold', 0) < 70:
            result.warnings.append("QA confidence threshold below 70% - may affect result reliability")
        
        # Check cost controls
        cost_controls = execution.get('cost_controls', {})
        if not cost_controls.get('max_total_cost'):
            result.warnings.append("No cost limit specified - recommended for budget management")
        
        # Check replication
        matrix = execution.get('matrix', [])
        if matrix:
            runs_per_text = matrix[0].get('runs_per_text', 1)
            if runs_per_text < 2:
                result.suggestions.append("Consider multiple runs per text for reliability assessment")
    
    def _validate_component_specifications(self, data: Dict[str, Any], result: ValidationResult):
        """Validate component specifications"""
        components = data.get('components', {})
        
        # Validate frameworks
        frameworks = components.get('frameworks', [])
        if not frameworks:
            result.errors.append("No frameworks specified")
        else:
            for i, framework in enumerate(frameworks):
                if 'id' not in framework:
                    result.errors.append(f"Framework {i+1} missing 'id' field")
                if 'version' not in framework:
                    result.warnings.append(f"Framework {i+1} missing version - recommended for reproducibility")
        
        # Validate corpus specifications
        corpus = components.get('corpus', [])
        if not corpus:
            result.errors.append("No corpus specified")
        else:
            for i, corpus_item in enumerate(corpus):
                if 'id' not in corpus_item:
                    result.errors.append(f"Corpus item {i+1} missing 'id' field")
                if 'file_path' not in corpus_item:
                    result.errors.append(f"Corpus item {i+1} missing 'file_path' field")
                
                # Check for expected categories for validation studies
                if 'expected_category' in corpus_item:
                    category = corpus_item['expected_category']
                    if not any(threshold in corpus_item for threshold in 
                              ['expected_dignity_score', 'expected_tribalism_score']):
                        result.suggestions.append(
                            f"Corpus item {i+1} has category but no expected score thresholds"
                        )
        
        # Validate models
        models = components.get('models', [])
        if not models:
            result.errors.append("No models specified")
    
    def _validate_research_ethics(self, data: Dict[str, Any], result: ValidationResult):
        """Validate research ethics compliance"""
        experiment_meta = data.get('experiment_meta', {})
        
        # Check data classification
        data_classification = experiment_meta.get('data_classification', 'unclassified')
        if data_classification not in ['unclassified', 'sensitive', 'confidential']:
            result.warnings.append(f"Unusual data classification: {data_classification}")
        
        # Check for human subjects considerations
        corpus = data.get('components', {}).get('corpus', [])
        has_speech_data = any('speech' in item.get('description', '').lower() 
                             for item in corpus)
        
        if has_speech_data and not experiment_meta.get('ethical_clearance'):
            result.warnings.append(
                "Speech data detected but no ethical clearance specified - may be required"
            )
    
    def _validate_reproducibility_requirements(self, data: Dict[str, Any], result: ValidationResult):
        """Validate reproducibility package requirements"""
        execution = data.get('execution', {})
        academic_compliance = execution.get('academic_compliance', {})
        
        # Check reproducibility package settings
        if not academic_compliance.get('generate_reproducibility_package'):
            result.suggestions.append(
                "Consider enabling reproducibility package generation for academic standards"
            )
        
        if not academic_compliance.get('publication_ready_exports'):
            result.suggestions.append(
                "Consider enabling publication-ready exports for academic dissemination"
            )
        
        # Check for version specification in components
        components = data.get('components', {})
        components_without_versions = []
        
        for component_type, component_list in components.items():
            if isinstance(component_list, list):
                for component in component_list:
                    if isinstance(component, dict) and 'version' not in component:
                        components_without_versions.append(f"{component_type}:{component.get('id', 'unknown')}")
        
        if components_without_versions:
            result.suggestions.append(
                f"Consider adding versions for reproducibility: {', '.join(components_without_versions[:3])}"
                + ("..." if len(components_without_versions) > 3 else "")
            )

def print_validation_results(result: ValidationResult, experiment_file: Path):
    """Print comprehensive validation results"""
    print(f"\n📋 EXPERIMENT VALIDATION RESULTS: {experiment_file}")
    print("=" * 60)
    
    # Overall status
    if result.is_valid:
        print("✅ VALIDATION PASSED - Experiment specification is valid")
    else:
        print("❌ VALIDATION FAILED - Issues must be resolved")
    
    # Academic compliance summary
    if result.academic_compliance:
        print(f"\n🎓 ACADEMIC COMPLIANCE:")
        for field, compliant in result.academic_compliance.items():
            status = "✅" if compliant else "⚠️"
            print(f"   {status} {field.replace('_', ' ').title()}")
    
    # Errors
    if result.errors:
        print(f"\n❌ ERRORS ({len(result.errors)}):")
        for error in result.errors:
            print(f"   • {error}")
    
    # Warnings
    if result.warnings:
        print(f"\n⚠️  WARNINGS ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"   • {warning}")
    
    # Suggestions
    if result.suggestions:
        print(f"\n💡 SUGGESTIONS ({len(result.suggestions)}):")
        for suggestion in result.suggestions:
            print(f"   • {suggestion}")
    
    print("\n" + "=" * 60)
    
    if result.is_valid:
        print("🚀 Ready for orchestrator execution!")
    else:
        print("🔧 Please address errors before proceeding.")

def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Comprehensive Academic Experiment Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate YAML experiment definition
  python experiment_validator.py experiment.yaml
  
  # Convert YAML to JSON for orchestrator
  python experiment_validator.py experiment.yaml --convert
  
  # Validate with detailed academic compliance checking
  python experiment_validator.py experiment.json --academic-strict

Academic Validation Features:
  - Complete experimental design validation
  - Academic compliance and institutional requirements
  - Statistical hypothesis validation
  - Research ethics and reproducibility checking
  - YAML/JSON format support with automatic conversion
        """
    )
    
    parser.add_argument(
        'experiment_file',
        type=Path,
        help='Path to experiment definition file (YAML or JSON)'
    )
    
    parser.add_argument(
        '--convert',
        action='store_true',
        help='Convert YAML to JSON for orchestrator (if input is YAML)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output file for conversion (default: input file with .json extension)'
    )
    
    parser.add_argument(
        '--academic-strict',
        action='store_true',
        help='Use strict academic validation (warnings become errors)'
    )
    
    args = parser.parse_args()
    
    # Validate experiment
    validator = ExperimentSpecValidator()
    result = validator.validate_experiment(args.experiment_file)
    
    # Convert warnings to errors in strict mode
    if args.academic_strict and result.warnings:
        result.errors.extend([f"STRICT: {w}" for w in result.warnings])
        result.warnings = []
        result.is_valid = False
    
    # Print results
    print_validation_results(result, args.experiment_file)
    
    # Convert if requested
    if args.convert and args.experiment_file.suffix.lower() in ['.yaml', '.yml']:
        try:
            output_file = validator.convert_yaml_to_json(args.experiment_file, args.output)
            print(f"\n✅ Conversion completed: {output_file}")
            print("🚀 JSON file ready for orchestrator execution!")
        except Exception as e:
            print(f"\n❌ Conversion failed: {e}")
            sys.exit(1)
    
    # Exit with appropriate code
    sys.exit(0 if result.is_valid else 1)

if __name__ == "__main__":
    main() 