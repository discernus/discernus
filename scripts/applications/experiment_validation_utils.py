#!/usr/bin/env python3
"""
Experiment Validation Utilities

Comprehensive validation utilities for experiment definitions with
clear error messages and actionable guidance for users.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import re

class ValidationSeverity(Enum):
    """Validation issue severity levels"""
    ERROR = "error"      # Blocks execution
    WARNING = "warning"  # May cause issues
    INFO = "info"       # Suggestions for improvement

@dataclass
class ValidationIssue:
    """Individual validation issue"""
    severity: ValidationSeverity
    category: str
    message: str
    location: str
    suggestion: str
    example: Optional[str] = None

@dataclass
class ValidationReport:
    """Complete validation report"""
    is_valid: bool
    issues: List[ValidationIssue]
    summary: Dict[str, int]
    
    def add_issue(self, severity: ValidationSeverity, category: str, 
                  message: str, location: str, suggestion: str, 
                  example: Optional[str] = None):
        """Add a validation issue"""
        self.issues.append(ValidationIssue(
            severity=severity,
            category=category,
            message=message,
            location=location,
            suggestion=suggestion,
            example=example
        ))
        
        # Update summary
        if severity.value not in self.summary:
            self.summary[severity.value] = 0
        self.summary[severity.value] += 1
        
        # Update validity
        if severity == ValidationSeverity.ERROR:
            self.is_valid = False

class ExperimentValidator:
    """Comprehensive experiment definition validator"""
    
    def __init__(self):
        self.report = ValidationReport(
            is_valid=True,
            issues=[],
            summary={}
        )
    
    def validate_experiment_file(self, file_path: Path) -> ValidationReport:
        """Main validation entry point"""
        self.report = ValidationReport(is_valid=True, issues=[], summary={})
        
        if not file_path.exists():
            self.report.add_issue(
                ValidationSeverity.ERROR,
                "file_access",
                f"Experiment file not found: {file_path}",
                str(file_path),
                "Check the file path and ensure the file exists",
                "experiment_file = Path('experiments/my_experiment.yaml')"
            )
            return self.report
        
        # Parse YAML/JSON
        try:
            experiment_data = self._load_experiment_file(file_path)
        except Exception as e:
            self.report.add_issue(
                ValidationSeverity.ERROR,
                "file_format",
                f"Cannot parse experiment file: {str(e)}",
                str(file_path),
                "Check YAML/JSON syntax using a validator or editor with syntax highlighting",
                "Use yamllint or paste into an online YAML validator"
            )
            return self.report
        
        # Validate structure
        self._validate_experiment_structure(experiment_data, file_path)
        
        # Validate components
        if 'components' in experiment_data:
            self._validate_components_section(experiment_data['components'], file_path)
        
        # Validate execution matrix
        if 'execution' in experiment_data:
            self._validate_execution_section(experiment_data['execution'], file_path)
        
        return self.report
    
    def _load_experiment_file(self, file_path: Path) -> Dict[str, Any]:
        """Load experiment file with proper error handling"""
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.suffix.lower() in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            elif file_path.suffix.lower() == '.json':
                return json.load(f)
            else:
                # Try YAML first, then JSON
                content = f.read()
                try:
                    return yaml.safe_load(content)
                except:
                    return json.loads(content)
    
    def _validate_experiment_structure(self, data: Dict[str, Any], file_path: Path):
        """Validate basic experiment structure"""
        required_sections = ['experiment_meta', 'components', 'execution']
        
        for section in required_sections:
            if section not in data:
                self.report.add_issue(
                    ValidationSeverity.ERROR,
                    "structure",
                    f"Missing required section: {section}",
                    f"{file_path}:root",
                    f"Add the {section} section to your experiment definition",
                    f"{section}:\n  # Add {section} configuration here"
                )
        
        # Validate experiment_meta
        if 'experiment_meta' in data:
            self._validate_experiment_meta(data['experiment_meta'], file_path)
    
    def _validate_experiment_meta(self, meta: Dict[str, Any], file_path: Path):
        """Validate experiment metadata"""
        required_meta = ['name', 'version', 'description']
        
        for field in required_meta:
            if field not in meta:
                self.report.add_issue(
                    ValidationSeverity.ERROR,
                    "metadata",
                    f"Missing required metadata field: {field}",
                    f"{file_path}:experiment_meta",
                    f"Add {field} to experiment_meta section",
                    f'{field}: "Your {field} here"'
                )
        
        # Validate version format
        if 'version' in meta:
            version = meta['version']
            if not re.match(r'^v?\d+\.\d+(\.\d+)?', str(version)):
                self.report.add_issue(
                    ValidationSeverity.WARNING,
                    "metadata",
                    f"Version format should follow semantic versioning: {version}",
                    f"{file_path}:experiment_meta:version",
                    "Use format like 'v1.0.0' or '1.0.0'",
                    'version: "v1.0.0"'
                )
    
    def _validate_components_section(self, components: Dict[str, Any], file_path: Path):
        """Validate components section"""
        supported_components = ['frameworks', 'prompt_templates', 'weighting_schemes', 'corpus', 'models']
        
        for component_type, component_list in components.items():
            if component_type not in supported_components:
                self.report.add_issue(
                    ValidationSeverity.WARNING,
                    "components",
                    f"Unknown component type: {component_type}",
                    f"{file_path}:components:{component_type}",
                    f"Supported types: {', '.join(supported_components)}",
                    "Check spelling and component type documentation"
                )
                continue
            
            if not isinstance(component_list, list):
                self.report.add_issue(
                    ValidationSeverity.ERROR,
                    "components",
                    f"Component {component_type} must be a list",
                    f"{file_path}:components:{component_type}",
                    f"Change {component_type} to a list format",
                    f"{component_type}:\n  - id: component_id\n    version: v1.0"
                )
                continue
            
            # Validate individual components
            for i, component in enumerate(component_list):
                self._validate_component_item(component, component_type, i, file_path)
    
    def _validate_component_item(self, component: Dict[str, Any], component_type: str, 
                                index: int, file_path: Path):
        """Validate individual component item"""
        location = f"{file_path}:components:{component_type}[{index}]"
        
        # Required fields
        if 'id' not in component:
            self.report.add_issue(
                ValidationSeverity.ERROR,
                "components",
                f"Missing 'id' field in {component_type} component",
                location,
                "Add an 'id' field to identify the component",
                'id: "component_identifier"'
            )
        
        # Framework-specific validation
        if component_type == 'frameworks':
            self._validate_framework_component(component, location)
        
        # Corpus-specific validation
        elif component_type == 'corpus':
            self._validate_corpus_component(component, location)
        
        # Model-specific validation
        elif component_type == 'models':
            self._validate_model_component(component, location)
    
    def _validate_framework_component(self, framework: Dict[str, Any], location: str):
        """Validate framework component"""
        if 'type' in framework and framework['type'] == 'file_path':
            if 'file_path' not in framework:
                self.report.add_issue(
                    ValidationSeverity.ERROR,
                    "framework",
                    "Framework with type 'file_path' must specify 'file_path'",
                    location,
                    "Add file_path pointing to your framework YAML file",
                    'file_path: "frameworks/my_framework/framework.yaml"'
                )
            else:
                # Check if file exists
                file_path = Path(framework['file_path'])
                if not file_path.exists():
                    self.report.add_issue(
                        ValidationSeverity.ERROR,
                        "framework",
                        f"Framework file not found: {file_path}",
                        location,
                        "Check the file path or create the framework file",
                        "Ensure the path is relative to project root"
                    )
                else:
                    # Validate framework file structure
                    self._validate_framework_file(file_path, location)
    
    def _validate_framework_file(self, file_path: Path, parent_location: str):
        """Validate framework file structure"""
        try:
            with open(file_path, 'r') as f:
                framework_data = yaml.safe_load(f)
        except Exception as e:
            self.report.add_issue(
                ValidationSeverity.ERROR,
                "framework",
                f"Cannot parse framework file: {e}",
                f"{parent_location}:file_path",
                "Check YAML syntax in framework file",
                "Use yamllint to validate the framework file"
            )
            return
        
        # Check required framework fields
        required_fields = ['name', 'dipoles']
        for field in required_fields:
            if field not in framework_data:
                self.report.add_issue(
                    ValidationSeverity.ERROR,
                    "framework",
                    f"Framework missing required field: {field}",
                    f"{file_path}:{field}",
                    f"Add {field} to your framework definition",
                    f"{field}: # Add {field} configuration"
                )
    
    def _validate_corpus_component(self, corpus: Dict[str, Any], location: str):
        """Validate corpus component"""
        if 'type' in corpus and corpus['type'] == 'file_collection':
            if 'file_path' not in corpus:
                self.report.add_issue(
                    ValidationSeverity.ERROR,
                    "corpus",
                    "Corpus with type 'file_collection' must specify 'file_path'",
                    location,
                    "Add file_path pointing to your corpus directory",
                    'file_path: "corpus/my_texts"'
                )
            else:
                # Check if directory exists
                corpus_path = Path(corpus['file_path'])
                if not corpus_path.exists():
                    self.report.add_issue(
                        ValidationSeverity.ERROR,
                        "corpus",
                        f"Corpus directory not found: {corpus_path}",
                        location,
                        "Check the directory path or create the corpus directory",
                        "Ensure the path contains text files matching your pattern"
                    )
                elif corpus_path.is_dir():
                    # Check for files matching pattern
                    pattern = corpus.get('pattern', '*')
                    matching_files = list(corpus_path.glob(pattern))
                    if not matching_files:
                        self.report.add_issue(
                            ValidationSeverity.WARNING,
                            "corpus",
                            f"No files found matching pattern '{pattern}' in {corpus_path}",
                            location,
                            f"Add files matching pattern '{pattern}' or adjust the pattern",
                            f"Common patterns: '*.txt', '*.md', '**/*.txt'"
                        )
    
    def _validate_model_component(self, model: Dict[str, Any], location: str):
        """Validate model component"""
        if 'provider' not in model:
            self.report.add_issue(
                ValidationSeverity.WARNING,
                "model",
                "Model should specify 'provider' for clarity",
                location,
                "Add provider field (e.g., 'openai', 'anthropic', 'huggingface')",
                'provider: "openai"'
            )
        
        # Check for common model name typos
        if 'id' in model:
            model_id = model['id']
            known_models = ['gpt-4', 'gpt-3.5-turbo', 'claude-3-sonnet', 'claude-3-haiku']
            if model_id not in known_models and not any(known in model_id for known in ['gpt', 'claude']):
                self.report.add_issue(
                    ValidationSeverity.INFO,
                    "model",
                    f"Unknown model ID: {model_id}",
                    location,
                    f"Verify model availability. Common models: {', '.join(known_models[:3])}",
                    "Check with your model provider for available models"
                )
    
    def _validate_execution_section(self, execution: Dict[str, Any], file_path: Path):
        """Validate execution section"""
        if 'matrix' not in execution:
            self.report.add_issue(
                ValidationSeverity.ERROR,
                "execution",
                "Missing 'matrix' in execution section",
                f"{file_path}:execution",
                "Add execution matrix defining your experimental runs",
                'matrix:\n  - run_id: "test_run"\n    # Add run parameters'
            )
            return
        
        matrix = execution['matrix']
        if not isinstance(matrix, list):
            self.report.add_issue(
                ValidationSeverity.ERROR,
                "execution",
                "Execution matrix must be a list",
                f"{file_path}:execution:matrix",
                "Change matrix to list format",
                'matrix:\n  - run_id: "run1"\n  - run_id: "run2"'
            )
            return
        
        # Validate matrix entries
        for i, run in enumerate(matrix):
            if not isinstance(run, dict):
                self.report.add_issue(
                    ValidationSeverity.ERROR,
                    "execution",
                    f"Matrix entry {i} must be a dictionary",
                    f"{file_path}:execution:matrix[{i}]",
                    "Each matrix entry should be a dictionary with run parameters",
                    'run_id: "unique_run_identifier"'
                )
                continue
            
            if 'run_id' not in run:
                self.report.add_issue(
                    ValidationSeverity.ERROR,
                    "execution",
                    f"Matrix entry {i} missing 'run_id'",
                    f"{file_path}:execution:matrix[{i}]",
                    "Add unique run_id to identify this experimental run",
                    'run_id: "descriptive_run_name"'
                )
    
    def print_report(self, show_suggestions: bool = True):
        """Print formatted validation report"""
        print("🔍 EXPERIMENT VALIDATION REPORT")
        print("=" * 60)
        
        if self.report.is_valid:
            print("✅ VALIDATION PASSED")
        else:
            print("❌ VALIDATION FAILED")
        
        # Summary
        print(f"\nSummary:")
        for severity, count in self.report.summary.items():
            emoji = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[severity]
            print(f"  {emoji} {count} {severity}(s)")
        
        if not self.report.issues:
            print("\n🎉 No issues found!")
            return
        
        # Group issues by category
        by_category = {}
        for issue in self.report.issues:
            if issue.category not in by_category:
                by_category[issue.category] = []
            by_category[issue.category].append(issue)
        
        # Print issues
        print(f"\nIssues:")
        for category, issues in by_category.items():
            print(f"\n📁 {category.upper()}:")
            for issue in issues:
                emoji = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[issue.severity.value]
                print(f"  {emoji} {issue.message}")
                print(f"     Location: {issue.location}")
                if show_suggestions and issue.suggestion:
                    print(f"     Fix: {issue.suggestion}")
                if show_suggestions and issue.example:
                    print(f"     Example: {issue.example}")
                print()

def main():
    """CLI entry point for validation utility"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate experiment definition files")
    parser.add_argument("experiment_file", help="Path to experiment YAML/JSON file")
    parser.add_argument("--no-suggestions", action="store_true", 
                       help="Hide suggestions and examples")
    
    args = parser.parse_args()
    
    validator = ExperimentValidator()
    report = validator.validate_experiment_file(Path(args.experiment_file))
    validator.print_report(show_suggestions=not args.no_suggestions)
    
    return 0 if report.is_valid else 1

if __name__ == "__main__":
    exit(main()) 