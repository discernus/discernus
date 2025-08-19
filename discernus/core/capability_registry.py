#!/usr/bin/env python3
"""
Capability Registry - THIN Extensibility System
===============================================

THIN Principle: Simple configuration-based system for academics to add
new tools, libraries, and capabilities without forking the codebase.

Philosophy: Software provides extension infrastructure, academics provide domain expertise.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
import importlib
import logging

logger = logging.getLogger(__name__)

class CapabilityRegistry:
    """
    Registry for managing extended capabilities in Discernus
    
    THIN Principle: Configuration-driven extensions with minimal code changes
    """
    
    def __init__(self, extensions_dir: str = "extensions", presets_dir: str = "discernus/core/presets"):
        # Use absolute path for presets to avoid working directory issues
        if Path(presets_dir).is_absolute():
            self.presets_dir = Path(presets_dir)
        else:
            # Find the repo root and use absolute path
            repo_root = Path(__file__).parent.parent.parent
            self.presets_dir = repo_root / presets_dir
        
        self.extensions_dir = Path(extensions_dir)
        self.extensions_dir.mkdir(exist_ok=True)
        
        # Core capabilities (always available)
        self.core_libraries = set()
        
        # Extended capabilities from configuration
        self.extended_libraries = set()
        self.extended_agents = {}
        self.capability_environments = {}
        
        # Load extensions
        self.extensions = {}  # Store full extension data for builtins access
        self._load_core_capabilities()
        self._load_extensions()
    
    def _load_core_capabilities(self):
        """Load the core set of allowed libraries from a preset file."""
        core_config_path = self.presets_dir / "core_capabilities.yaml"
        if core_config_path.exists():
            try:
                self._load_extension_file(core_config_path, is_core=True)
            except Exception as e:
                logger.error(f"CRITICAL: Failed to load core capabilities from {core_config_path}: {e}")
        else:
            logger.error(f"CRITICAL: Core capabilities file not found at {core_config_path}. No libraries will be allowed.")

    def _load_extensions(self):
        """Load capability extensions from configuration files"""
        
        # Look for extension files
        extension_files = list(self.extensions_dir.glob("*.yaml")) + list(self.extensions_dir.glob("*.yml"))
        
        for ext_file in extension_files:
            try:
                self._load_extension_file(ext_file)
            except Exception as e:
                logger.warning(f"Failed to load extension {ext_file}: {e}")
    
    def _load_extension_file(self, ext_file: Path, is_core: bool = False):
        """Load a single extension file"""
        
        with open(ext_file, 'r') as f:
            extension_config = yaml.safe_load(f)
        
        extension_name = extension_config.get('name', ext_file.stem)
        logger.info(f"Loading extension: {extension_name}")
        
        # Store full extension data for later access
        self.extensions[extension_name] = extension_config
        
        # Load additional libraries
        if 'libraries' in extension_config:
            new_libs = set(extension_config['libraries'])
            if is_core:
                self.core_libraries.update(new_libs)
                logger.info(f"Loaded {len(new_libs)} core libraries.")
            else:
                self.extended_libraries.update(new_libs)
                logger.info(f"Added extended libraries: {new_libs}")
        
        # Load new expert agents
        if 'agents' in extension_config:
            for agent_name, agent_config in extension_config['agents'].items():
                self.extended_agents[agent_name] = agent_config
                logger.info(f"Added agent: {agent_name}")
        
        # Load custom environments
        if 'environments' in extension_config:
            env_name = extension_config['environments'].get('name', extension_name)
            self.capability_environments[env_name] = extension_config['environments']
            logger.info(f"Added environment: {env_name}")
    
    def get_allowed_libraries(self) -> Set[str]:
        """Get all allowed libraries (core + extended)"""
        return self.core_libraries | self.extended_libraries
    
    def get_allowed_builtins(self) -> Set[str]:
        """Get the complete set of allowed builtin functions."""
        allowed_builtins = set()
        
        # Collect allowed builtins from all loaded extensions
        for ext_name, ext_data in self.extensions.items():
            builtins = ext_data.get('allowed_builtins', [])
            if isinstance(builtins, list):
                allowed_builtins.update(builtins)
        
        return allowed_builtins
    
    def get_agent_prompt(self, agent_name: str) -> Optional[str]:
        """Get agent prompt from extensions"""
        agent_config = self.extended_agents.get(agent_name)
        if agent_config:
            return agent_config.get('prompt', '')
        return None
    
    def get_custom_environment(self, environment_name: str) -> str:
        """Get custom environment setup code"""
        
        env_config = self.capability_environments.get(environment_name)
        if not env_config:
            return ""
        
        # Build environment setup
        setup_code = "# Custom environment setup\n"
        
        # Add imports
        if 'imports' in env_config:
            for import_stmt in env_config['imports']:
                setup_code += f"{import_stmt}\n"
        
        # Add initialization code
        if 'setup_code' in env_config:
            setup_code += f"\n{env_config['setup_code']}\n"
        
        # Add mock objects for missing libraries
        if 'mock_fallbacks' in env_config:
            setup_code += "\n# Mock fallbacks for missing libraries\n"
            for lib_name, mock_code in env_config['mock_fallbacks'].items():
                setup_code += f"try:\n    import {lib_name}\nexcept ImportError:\n    {mock_code}\n"
        
        return setup_code
    
    def create_extension_template(self, extension_name: str, description: str = ""):
        """Create a template extension file for academics"""
        
        template = {
            'name': extension_name,
            'description': description or f"Custom extension: {extension_name}",
            'version': '1.0.0',
            'author': 'Academic Researcher',
            
            # Example libraries to add
            'libraries': [
                '# Add your favorite libraries here',
                '# Example: spacy',
                '# Example: transformers',
                '# Example: scipy.spatial'
            ],
            
            # Example custom agent
            'agents': {
                f'{extension_name}_expert': {
                    'description': f'Expert agent for {extension_name} analysis',
                    'prompt': f'''You are a {extension_name}_expert specialized in [YOUR DOMAIN].

RESEARCH QUESTION: {{research_question}}

SOURCE TEXTS:
{{source_texts}}

EXPERT REQUEST: {{expert_request}}

Your Task:
Provide expert analysis using {extension_name} methodologies.
You have access to specialized tools for your domain.

If you need calculations, write Python code in ```python blocks.
Focus on your area of expertise and provide rigorous analysis.'''
                }
            },
            
            # Example custom environment
            'environments': {
                'name': f'{extension_name}_env',
                'description': f'Specialized environment for {extension_name}',
                'imports': [
                    '# import your_specialized_library',
                    '# from your_package import specialized_function'
                ],
                'setup_code': '''
# Your custom initialization code here
# Example:
# specialized_analyzer = YourLibrary()
# custom_config = {"parameter": "value"}
''',
                'mock_fallbacks': {
                    'your_library': '''
    class MockYourLibrary:
        def analyze(self, text):
            return "Mock analysis - library not available"
    your_library = MockYourLibrary()
'''
                }
            }
        }
        
        # Save template
        template_file = self.extensions_dir / f"{extension_name}.yaml"
        with open(template_file, 'w') as f:
            yaml.dump(template, f, default_flow_style=False, sort_keys=False)
        
        logger.info(f"Created extension template: {template_file}")
        return template_file
    
    def validate_extension(self, extension_file: Path) -> List[str]:
        """Validate an extension file and return any issues"""
        
        issues = []
        
        try:
            with open(extension_file, 'r') as f:
                config = yaml.safe_load(f)
        except Exception as e:
            return [f"Invalid YAML: {e}"]
        
        # Check required fields
        if 'name' not in config:
            issues.append("Missing required field: 'name'")
        
        # Validate libraries
        if 'libraries' in config and not isinstance(config['libraries'], list):
            issues.append("'libraries' must be a list")
        
        # Validate agents
        if 'agents' in config:
            if not isinstance(config['agents'], dict):
                issues.append("'agents' must be a dictionary")
            else:
                for agent_name, agent_config in config['agents'].items():
                    if 'prompt' not in agent_config:
                        issues.append(f"Agent '{agent_name}' missing 'prompt' field")
        
        # Test library imports
        if 'libraries' in config:
            for lib in config['libraries']:
                if isinstance(lib, str) and not lib.startswith('#'):
                    try:
                        importlib.import_module(lib.split('.')[0])
                    except ImportError:
                        issues.append(f"Library '{lib}' is not installed")
        
        return issues

# Global registry instance
_registry = None

def get_capability_registry() -> CapabilityRegistry:
    """Get the global capability registry"""
    global _registry
    if _registry is None:
        _registry = CapabilityRegistry()
    return _registry

def create_extension(extension_name: str, description: str = "") -> Path:
    """Convenience function to create an extension template"""
    registry = get_capability_registry()
    return registry.create_extension_template(extension_name, description)

if __name__ == "__main__":
    # Demo usage
    print("🔌 Capability Registry Demo")
    print("=" * 40)
    
    registry = CapabilityRegistry()
    
    print(f"Core libraries: {len(registry.core_libraries)}")
    print(f"Extended libraries: {len(registry.extended_libraries)}")
    print(f"Extended agents: {len(registry.extended_agents)}")
    
    # Create demo extension
    demo_file = registry.create_extension_template("psycholinguistics", "Psychological text analysis tools")
    print(f"\n📝 Created demo extension: {demo_file}")
    
    # Validate it
    issues = registry.validate_extension(demo_file)
    if issues:
        print(f"⚠️ Validation issues: {issues}")
    else:
        print("✅ Extension template is valid") 