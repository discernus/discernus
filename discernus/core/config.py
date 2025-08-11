#!/usr/bin/env python3
"""
Discernus Configuration Management
=================================

Handles configuration files, environment variables, and CLI defaults
following modern CLI tool conventions.

Supports:
- YAML config files (.discernus.yaml, discernus.yaml)
- Environment variables (DISCERNUS_*)
- XDG Base Directory specification
- Hierarchical config resolution (CLI > env > config > defaults)
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DiscernusConfig(BaseSettings):
    """
    Discernus configuration with automatic environment variable support.
    
    Configuration resolution order (highest to lowest priority):
    1. CLI arguments (handled by Click)
    2. Environment variables (DISCERNUS_*)
    3. Config files (.discernus.yaml, discernus.yaml)
    4. Default values
    """
    
    # Model configuration
    analysis_model: str = Field(default="vertex_ai/gemini-2.5-flash", description="Default LLM model for analysis")
    synthesis_model: str = Field(default="vertex_ai/gemini-2.5-pro", description="Default LLM model for synthesis")
    validation_model: str = Field(default="vertex_ai/gemini-2.5-pro", description="Default LLM model for validation (requires higher intelligence)")
    
    # Execution options
    auto_commit: bool = Field(default=True, description="Automatically commit successful runs to Git")
    skip_validation: bool = Field(default=False, description="Skip experiment validation")
    ensemble_runs: int = Field(default=1, description="Number of ensemble runs (currently disabled)")
    
    # Output options
    verbose: bool = Field(default=False, description="Enable verbose output")
    quiet: bool = Field(default=False, description="Enable quiet output (minimal)")
    no_color: bool = Field(default=False, description="Disable colored output")
    progress: bool = Field(default=True, description="Show progress indicators")
    
    # Advanced options
    dry_run: bool = Field(default=False, description="Show what would be done without executing")
    force: bool = Field(default=False, description="Force operations (for promote command)")
    
    model_config = SettingsConfigDict(
        env_prefix='DISCERNUS_',
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )


class ConfigManager:
    """
    Manages Discernus configuration files and settings.
    
    Handles config file discovery, loading, and merging with environment variables.
    """
    
    CONFIG_FILENAMES = ['.discernus.yaml', 'discernus.yaml', '.discernus.yml', 'discernus.yml']
    
    def __init__(self):
        self._config: Optional[DiscernusConfig] = None
        self._config_file_path: Optional[Path] = None
    
    def load_config(self, config_path: Optional[Path] = None) -> DiscernusConfig:
        """
        Load configuration from files and environment variables.
        
        Args:
            config_path: Explicit config file path, or None for auto-discovery
            
        Returns:
            Loaded configuration with all sources merged
        """
        if self._config is not None:
            return self._config
        
        # Find config file
        if config_path:
            self._config_file_path = config_path
        else:
            self._config_file_path = self._find_config_file()
        
        # Load config file data if it exists
        config_data = {}
        if self._config_file_path and self._config_file_path.exists():
            config_data = self._load_yaml_config(self._config_file_path)
        
        # Create configuration with file data and environment variables
        # Pydantic will automatically load environment variables with DISCERNUS_ prefix
        self._config = DiscernusConfig(**config_data)
        
        return self._config
    
    def _find_config_file(self) -> Optional[Path]:
        """
        Find config file using standard search order.
        
        Search order:
        1. Current directory
        2. Parent directories (up to project root)
        3. User home directory
        4. XDG config directory
        
        Returns:
            Path to first found config file, or None
        """
        search_paths = []
        
        # Current directory and parents
        current = Path.cwd()
        search_paths.append(current)
        
        # Walk up to find project root (look for .git or pyproject.toml)
        for parent in current.parents:
            search_paths.append(parent)
            if (parent / '.git').exists() or (parent / 'pyproject.toml').exists():
                break
        
        # User home directory
        search_paths.append(Path.home())
        
        # XDG config directory
        xdg_config = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))
        search_paths.append(xdg_config / 'discernus')
        
        # Search for config files
        for search_path in search_paths:
            for filename in self.CONFIG_FILENAMES:
                config_file = search_path / filename
                if config_file.exists():
                    return config_file
        
        return None
    
    def _load_yaml_config(self, config_path: Path) -> Dict[str, Any]:
        """Load and parse YAML config file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
                if not isinstance(data, dict):
                    raise ValueError(f"Config file must contain a YAML dictionary, got {type(data)}")
                return data
        except Exception as e:
            raise ValueError(f"Failed to load config file {config_path}: {e}")
    
    def get_config_file_path(self) -> Optional[Path]:
        """Get the path to the loaded config file, if any."""
        return self._config_file_path
    
    def create_default_config(self, config_path: Path) -> None:
        """Create a default config file with common settings."""
        default_config = {
            '# Discernus Configuration': None,
            '# This file configures default settings for the Discernus CLI': None,
            '# All settings can be overridden by environment variables (DISCERNUS_*)': None,
            '# or CLI arguments': None,
            '': None,
            '# Model Configuration': None,
            'analysis_model': 'vertex_ai/gemini-2.5-flash',
            'synthesis_model': 'vertex_ai/gemini-2.5-pro', 
            'validation_model': 'vertex_ai/gemini-2.5-pro',
            '': None,
            '# Execution Options': None, 
            'auto_commit': True,
            'skip_validation': False,
            'ensemble_runs': 1,
            '': None,
            '# Output Options': None,
            'verbose': False,
            'quiet': False,
            'no_color': False,
            'progress': True,
            '': None,
            '# Advanced Options': None,
            'dry_run': False,
            'force': False,
        }
        
        # Filter out comment keys and empty keys for actual YAML
        yaml_data = {k: v for k, v in default_config.items() 
                    if not k.startswith('#') and k != ''}
        
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write("# Discernus Configuration\n")
            f.write("# This file configures default settings for the Discernus CLI\n")
            f.write("# All settings can be overridden by environment variables (DISCERNUS_*)\n")
            f.write("# or CLI arguments\n\n")
            
            f.write("# Model Configuration\n")
            f.write(f"analysis_model: {yaml_data['analysis_model']}\n")
            f.write(f"synthesis_model: {yaml_data['synthesis_model']}\n\n")
            
            f.write("# Execution Options\n")
            f.write(f"auto_commit: {yaml_data['auto_commit']}\n")
            f.write(f"skip_validation: {yaml_data['skip_validation']}\n")
            f.write(f"ensemble_runs: {yaml_data['ensemble_runs']}\n\n")
            
            f.write("# Output Options\n")
            f.write(f"verbose: {yaml_data['verbose']}\n")
            f.write(f"quiet: {yaml_data['quiet']}\n")
            f.write(f"no_color: {yaml_data['no_color']}\n")
            f.write(f"progress: {yaml_data['progress']}\n\n")
            
            f.write("# Advanced Options\n")
            f.write(f"dry_run: {yaml_data['dry_run']}\n")
            f.write(f"force: {yaml_data['force']}\n")


# Global config manager instance
config_manager = ConfigManager()

def get_config() -> DiscernusConfig:
    """Get the global configuration instance."""
    return config_manager.load_config()

def get_config_file_path() -> Optional[Path]:
    """Get the path to the active config file."""
    return config_manager.get_config_file_path()