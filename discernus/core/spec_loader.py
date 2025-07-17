#!/usr/bin/env python3
"""
Specification Loader - V4 Framework & V2 Experiment/Corpus Parser
================================================================

THIN Principle: Simple specification parsing with no complex intelligence.
Software extracts structured data; LLM prompts contain all the intelligence.

Supports:
- V4 Framework files (markdown with embedded JSON configuration in <details> section)
- V2 Experiment files (structured YAML)
- V2 Corpus directories (text file collections)

Architecture:
- FrameworkParser: Extracts JSON configuration from markdown files
- ExperimentParser: Loads and validates V2 experiment YAML files
- CorpusLoader: Scans directories and loads text files
- SpecLoader: Main orchestrator class
"""

import yaml
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpecificationError(Exception):
    """Base exception for specification parsing errors"""
    pass

class FrameworkError(SpecificationError):
    """Framework-specific parsing errors"""
    pass

class ExperimentError(SpecificationError):
    """Experiment-specific parsing errors"""
    pass

class CorpusError(SpecificationError):
    """Corpus-specific loading errors"""
    pass

class FrameworkParser:
    """
    Parses V4 Framework files (markdown with embedded JSON configuration in <details> section)
    
    THIN Principle: Simple JSON extraction, no framework intelligence
    """
    
    def __init__(self):
        # Updated to match Framework Specification v4.0 - JSON in <details> section
        self.json_config_pattern = re.compile(
            r'<details><summary>Machine-Readable Configuration</summary>\s*\n+```json\s*\n(.*?)\n```\s*\n+</details>', 
            re.DOTALL
        )
    
    def parse_framework(self, framework_path: Path) -> Dict[str, Any]:
        """
        Parse a V4 framework file and extract configuration
        
        Args:
            framework_path: Path to framework.md file
            
        Returns:
            Dict containing framework configuration and metadata
            
        Raises:
            FrameworkError: If parsing fails or required fields missing
        """
        if not framework_path.exists():
            raise FrameworkError(f"Framework file not found: {framework_path}")
        
        try:
            content = framework_path.read_text(encoding='utf-8')
        except Exception as e:
            raise FrameworkError(f"Failed to read framework file: {e}")
        
        # Extract JSON configuration from <details> section
        json_match = self.json_config_pattern.search(content)
        if not json_match:
            raise FrameworkError(
                f"No JSON configuration block found in {framework_path}. "
                f"Expected block in format: <details><summary>Machine-Readable Configuration</summary>\\n```json\\n...\\n```\\n</details>"
            )
        
        json_content = json_match.group(1)
        
        # Parse JSON
        try:
            config = json.loads(json_content)
        except json.JSONDecodeError as e:
            raise FrameworkError(f"Invalid JSON in configuration block: {e}")
        
        if not isinstance(config, dict):
            raise FrameworkError("Framework configuration must be a JSON dictionary")
        
        # Validate required fields
        required_fields = ['name', 'version', 'analysis_variants']
        for field in required_fields:
            if field not in config:
                raise FrameworkError(f"Missing required field: {field}")
        
        # Validate analysis_variants structure
        if not isinstance(config['analysis_variants'], dict):
            raise FrameworkError("analysis_variants must be a dictionary")
        
        for variant_name, variant_config in config['analysis_variants'].items():
            if not isinstance(variant_config, dict):
                raise FrameworkError(f"analysis_variants.{variant_name} must be a dictionary")
            if 'analysis_prompt' not in variant_config:
                raise FrameworkError(f"analysis_variants.{variant_name} missing required field: analysis_prompt")
        
        # Add metadata
        config['_metadata'] = {
            'file_path': str(framework_path),
            'file_size': framework_path.stat().st_size,
            'parsed_at': datetime.now().isoformat(),
            'full_content': content
        }
        
        logger.info(f"✅ Parsed framework: {config['name']} v{config['version']} with {len(config['analysis_variants'])} variants")
        
        return config
    
    def validate_framework(self, framework_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate framework configuration completeness
        
        Args:
            framework_config: Parsed framework configuration
            
        Returns:
            Validation result with status and details
        """
        validation_result = {
            'valid': True,
            'issues': [],
            'warnings': [],
            'completeness_score': 0
        }
        
        # Check required fields
        required_fields = ['name', 'version', 'analysis_variants']
        present_fields = 0
        
        for field in required_fields:
            if field in framework_config:
                present_fields += 1
            else:
                validation_result['issues'].append(f"Missing required field: {field}")
                validation_result['valid'] = False
        
        # Check analysis variants
        if 'analysis_variants' in framework_config:
            variants = framework_config['analysis_variants']
            if not variants:
                validation_result['issues'].append("No analysis variants defined")
                validation_result['valid'] = False
            else:
                for variant_name, variant_config in variants.items():
                    if 'analysis_prompt' not in variant_config:
                        validation_result['issues'].append(f"Variant {variant_name} missing analysis_prompt")
                        validation_result['valid'] = False
                    elif len(variant_config['analysis_prompt'].strip()) < 100:
                        validation_result['warnings'].append(f"Variant {variant_name} has very short analysis_prompt")
        
        # Calculate completeness score
        total_checks = len(required_fields) + len(framework_config.get('analysis_variants', {}))
        passed_checks = present_fields + len([v for v in framework_config.get('analysis_variants', {}).values() if 'analysis_prompt' in v])
        validation_result['completeness_score'] = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        return validation_result

class ExperimentParser:
    """
    Parses V2 Experiment files (structured YAML)
    
    THIN Principle: Simple YAML loading with validation
    """
    
    def parse_experiment(self, experiment_path: Path) -> Dict[str, Any]:
        """
        Parse a V2 experiment file
        
        Args:
            experiment_path: Path to experiment.md or experiment.yaml file
            
        Returns:
            Dict containing experiment configuration
            
        Raises:
            ExperimentError: If parsing fails or required fields missing
        """
        if not experiment_path.exists():
            raise ExperimentError(f"Experiment file not found: {experiment_path}")
        
        try:
            content = experiment_path.read_text(encoding='utf-8')
        except Exception as e:
            raise ExperimentError(f"Failed to read experiment file: {e}")
        
        # Handle both .md and .yaml files - extract YAML content
        if experiment_path.suffix == '.md':
            # Look for YAML frontmatter or configuration block
            yaml_match = re.search(r'^---\n(.*?)^---', content, re.DOTALL | re.MULTILINE)
            if yaml_match:
                yaml_content = yaml_match.group(1)
            else:
                # Try to find configuration block
                config_match = re.search(r'# --- Discernus Configuration ---\n(.*?)(?=\n---|\n# |$)', content, re.DOTALL)
                if config_match:
                    yaml_content = config_match.group(1)
                else:
                    raise ExperimentError("No YAML configuration found in experiment file")
        else:
            yaml_content = content
        
        # Parse YAML
        try:
            config = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            raise ExperimentError(f"Invalid YAML in experiment file: {e}")
        
        if not isinstance(config, dict):
            raise ExperimentError("Experiment configuration must be a YAML dictionary")
        
        # Validate required fields
        required_fields = ['framework_file', 'models']
        for field in required_fields:
            if field not in config:
                raise ExperimentError(f"Missing required field: {field}")
        
        # Validate models field
        if not isinstance(config['models'], list) or not config['models']:
            raise ExperimentError("models must be a non-empty list")
        
        # Set defaults for optional fields
        config.setdefault('runs_per_model', 1)
        config.setdefault('analysis_variant', 'default')
        
        # Resolve framework_file path relative to experiment file
        if not Path(config['framework_file']).is_absolute():
            config['framework_file'] = str(experiment_path.parent / config['framework_file'])
        
        # Add metadata
        config['_metadata'] = {
            'file_path': str(experiment_path),
            'file_size': experiment_path.stat().st_size,
            'parsed_at': datetime.now().isoformat()
        }
        
        logger.info(f"✅ Parsed experiment with {len(config['models'])} models, {config['runs_per_model']} runs per model")
        
        return config
    
    def validate_experiment(self, experiment_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate experiment configuration
        
        Args:
            experiment_config: Parsed experiment configuration
            
        Returns:
            Validation result with status and details
        """
        validation_result = {
            'valid': True,
            'issues': [],
            'warnings': [],
            'completeness_score': 0
        }
        
        # Check required fields
        required_fields = ['framework_file', 'models']
        present_fields = 0
        
        for field in required_fields:
            if field in experiment_config:
                present_fields += 1
            else:
                validation_result['issues'].append(f"Missing required field: {field}")
                validation_result['valid'] = False
        
        # Validate framework_file exists
        if 'framework_file' in experiment_config:
            framework_path = Path(experiment_config['framework_file'])
            if not framework_path.exists():
                validation_result['issues'].append(f"Framework file not found: {framework_path}")
                validation_result['valid'] = False
        
        # Validate models
        if 'models' in experiment_config:
            models = experiment_config['models']
            if not isinstance(models, list) or not models:
                validation_result['issues'].append("models must be a non-empty list")
                validation_result['valid'] = False
            else:
                for model in models:
                    if not isinstance(model, str):
                        validation_result['issues'].append(f"Model must be a string: {model}")
                        validation_result['valid'] = False
        
        # Check runs_per_model
        runs_per_model = experiment_config.get('runs_per_model', 1)
        if not isinstance(runs_per_model, int) or runs_per_model < 1:
            validation_result['issues'].append("runs_per_model must be a positive integer")
            validation_result['valid'] = False
        
        # Calculate completeness score
        total_checks = len(required_fields) + 2  # +2 for framework_file exists and models validation
        passed_checks = present_fields + (1 if Path(experiment_config.get('framework_file', '')).exists() else 0)
        passed_checks += (1 if isinstance(experiment_config.get('models'), list) and experiment_config.get('models') else 0)
        validation_result['completeness_score'] = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        return validation_result

class CorpusLoader:
    """
    Loads V2 Corpus directories (text file collections)
    
    THIN Principle: Simple file loading with basic validation
    """
    
    def __init__(self):
        self.supported_extensions = {'.txt', '.md'}
    
    def load_corpus(self, corpus_path: Path) -> Dict[str, Any]:
        """
        Load corpus from directory
        
        Args:
            corpus_path: Path to corpus directory
            
        Returns:
            Dict containing corpus data and metadata
            
        Raises:
            CorpusError: If loading fails or no valid files found
        """
        if not corpus_path.exists():
            raise CorpusError(f"Corpus directory not found: {corpus_path}")
        
        if not corpus_path.is_dir():
            raise CorpusError(f"Corpus path is not a directory: {corpus_path}")
        
        corpus_data = {
            'files': {},
            'metadata': {
                'corpus_path': str(corpus_path),
                'loaded_at': datetime.now().isoformat(),
                'total_files': 0,
                'total_size': 0,
                'file_extensions': set()
            }
        }
        
        # Scan directory for text files
        for file_path in corpus_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                try:
                    content = file_path.read_text(encoding='utf-8')
                    
                    corpus_data['files'][file_path.name] = {
                        'content': content,
                        'path': str(file_path),
                        'size': file_path.stat().st_size,
                        'extension': file_path.suffix.lower()
                    }
                    
                    corpus_data['metadata']['total_size'] += file_path.stat().st_size
                    corpus_data['metadata']['file_extensions'].add(file_path.suffix.lower())
                    
                except Exception as e:
                    logger.warning(f"Failed to read file {file_path}: {e}")
        
        corpus_data['metadata']['total_files'] = len(corpus_data['files'])
        corpus_data['metadata']['file_extensions'] = list(corpus_data['metadata']['file_extensions'])
        
        if corpus_data['metadata']['total_files'] == 0:
            raise CorpusError(f"No valid text files found in corpus directory: {corpus_path}")
        
        logger.info(f"✅ Loaded corpus with {corpus_data['metadata']['total_files']} files, {corpus_data['metadata']['total_size']} bytes")
        
        return corpus_data
    
    def validate_corpus(self, corpus_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate corpus data
        
        Args:
            corpus_data: Loaded corpus data
            
        Returns:
            Validation result with status and details
        """
        validation_result = {
            'valid': True,
            'issues': [],
            'warnings': [],
            'file_count': corpus_data['metadata']['total_files']
        }
        
        if corpus_data['metadata']['total_files'] == 0:
            validation_result['issues'].append("No files found in corpus")
            validation_result['valid'] = False
        
        # Check for very small files
        small_files = [
            filename for filename, file_data in corpus_data['files'].items()
            if len(file_data['content'].strip()) < 100
        ]
        
        if small_files:
            validation_result['warnings'].append(f"Found {len(small_files)} very small files (< 100 chars)")
        
        # Check for empty files
        empty_files = [
            filename for filename, file_data in corpus_data['files'].items()
            if not file_data['content'].strip()
        ]
        
        if empty_files:
            validation_result['issues'].append(f"Found {len(empty_files)} empty files")
            validation_result['valid'] = False
        
        return validation_result

class SpecLoader:
    """
    Main specification loader orchestrating all parsing components
    
    THIN Principle: Simple orchestration with clear error handling
    """
    
    def __init__(self):
        self.framework_parser = FrameworkParser()
        self.experiment_parser = ExperimentParser()
        self.corpus_loader = CorpusLoader()
    
    def load_specifications(self, framework_file: Path, experiment_file: Path, corpus_dir: Path) -> Dict[str, Any]:
        """
        Load and validate all specifications for an experiment
        
        Args:
            framework_file: Path to V4 framework file
            experiment_file: Path to V2 experiment file
            corpus_dir: Path to V2 corpus directory
            
        Returns:
            Dict containing all loaded specifications
            
        Raises:
            SpecificationError: If any specification fails to load or validate
        """
        result = {
            'framework': None,
            'experiment': None,
            'corpus': None,
            'validation': {
                'framework': None,
                'experiment': None,
                'corpus': None,
                'overall_valid': False
            },
            'metadata': {
                'loaded_at': datetime.now().isoformat(),
                'loader_version': '1.0.0'
            }
        }
        
        try:
            # Load framework
            logger.info(f"Loading framework: {framework_file}")
            result['framework'] = self.framework_parser.parse_framework(framework_file)
            result['validation']['framework'] = self.framework_parser.validate_framework(result['framework'])
            
            # Load experiment
            logger.info(f"Loading experiment: {experiment_file}")
            result['experiment'] = self.experiment_parser.parse_experiment(experiment_file)
            result['validation']['experiment'] = self.experiment_parser.validate_experiment(result['experiment'])
            
            # Load corpus
            logger.info(f"Loading corpus: {corpus_dir}")
            result['corpus'] = self.corpus_loader.load_corpus(corpus_dir)
            result['validation']['corpus'] = self.corpus_loader.validate_corpus(result['corpus'])
            
            # Overall validation
            result['validation']['overall_valid'] = all([
                result['validation']['framework']['valid'],
                result['validation']['experiment']['valid'],
                result['validation']['corpus']['valid']
            ])
            
            if result['validation']['overall_valid']:
                logger.info("✅ All specifications loaded and validated successfully")
            else:
                logger.warning("⚠️ Some specifications have validation issues")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to load specifications: {e}")
            raise SpecificationError(f"Failed to load specifications: {e}")
    
    def get_analysis_prompt(self, specifications: Dict[str, Any]) -> str:
        """
        Get the analysis prompt for the specified variant
        
        Args:
            specifications: Loaded specifications
            
        Returns:
            Analysis prompt string
            
        Raises:
            SpecificationError: If variant not found
        """
        framework = specifications['framework']
        experiment = specifications['experiment']
        
        variant = experiment.get('analysis_variant', 'default')
        
        if variant not in framework['analysis_variants']:
            available_variants = list(framework['analysis_variants'].keys())
            raise SpecificationError(f"Analysis variant '{variant}' not found. Available variants: {available_variants}")
        
        return framework['analysis_variants'][variant]['analysis_prompt']
    
    def get_experiment_models(self, specifications: Dict[str, Any]) -> List[str]:
        """
        Get the list of models to use for the experiment
        
        Args:
            specifications: Loaded specifications
            
        Returns:
            List of model names
        """
        return specifications['experiment']['models']
    
    def get_runs_per_model(self, specifications: Dict[str, Any]) -> int:
        """
        Get the number of runs per model
        
        Args:
            specifications: Loaded specifications
            
        Returns:
            Number of runs per model
        """
        return specifications['experiment'].get('runs_per_model', 1)
    
    def get_corpus_files(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """
        Get corpus files as filename -> content mapping
        
        Args:
            specifications: Loaded specifications
            
        Returns:
            Dict mapping filename to content
        """
        return {
            filename: file_data['content']
            for filename, file_data in specifications['corpus']['files'].items()
        } 