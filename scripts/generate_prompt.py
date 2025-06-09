#!/usr/bin/env python3
"""
Narrative Gravity Wells Prompt Generator

Generates LLM analysis prompts from framework configurations using the unified template system.
This enables easy customization and extensibility of the framework.

Usage: python generate_prompt.py [--framework civic_virtue] [--mode interactive] [--output prompt.txt]

MIGRATION NOTICE:
This script now uses the new unified template system (src/prompts/template_manager.py).
The old PromptGenerator class is maintained for backward compatibility but is deprecated.

NEW RECOMMENDED USAGE:
    from src.prompts.template_manager import PromptTemplateManager
    template_manager = PromptTemplateManager()
    prompt = template_manager.generate_interactive_prompt(framework)
"""

import json
import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.narrative_gravity.prompts.template_manager import PromptTemplateManager, PromptMode

def load_dipoles(config_dir: str = "config") -> Dict:
    """Load dipole definitions from configuration file."""
    config_path = Path(config_dir) / "dipoles.json"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Dipoles configuration not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return json.load(f)

def load_framework(config_dir: str = "config") -> Dict:
    """Load framework configuration for prompt metadata."""
    config_path = Path(config_dir) / "framework.json"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Framework configuration not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return json.load(f)

class PromptGenerator:
    """
    DEPRECATED: Legacy wrapper for backward compatibility.
    
    NEW CODE SHOULD USE: src.prompts.template_manager.PromptTemplateManager
    
    This class provides backward compatibility for existing code that uses
    the old PromptGenerator interface. It wraps the new PromptTemplateManager.
    """
    
    def __init__(self, config_dir: str = "config", framework_name: str = None):
        print("⚠️  DEPRECATION WARNING: PromptGenerator is deprecated.")
        print("   Use src.prompts.template_manager.PromptTemplateManager instead.")
        print("   See PROMPT_ARCHITECTURE.md for migration guide.")
        
        self.config_dir = config_dir
        self.framework_name = framework_name
        
        # Initialize the new template manager
        self.template_manager = PromptTemplateManager()
        
        if not framework_name:
            # Try to get framework name from the files themselves
            try:
                dipoles = load_dipoles(config_dir)
                framework = load_framework(config_dir)
                self.framework_name = dipoles.get('framework_name') or framework.get('framework_name')
            except FileNotFoundError:
                pass
            
            # Fallback to FrameworkManager if not found in files
            if not self.framework_name:
                try:
                    from src.narrative_gravity.framework_manager import FrameworkManager
                    manager = FrameworkManager()
                    self.framework_name = manager.get_active_framework() or "civic_virtue"
                except:
                    self.framework_name = "civic_virtue"
        
    def generate_interactive_prompt(self) -> str:
        """Generate an interactive workflow prompt using new template system."""
        return self.template_manager.generate_interactive_prompt(self.framework_name)
    
    def generate_batch_prompt(self) -> str:
        """Generate a batch processing prompt using new template system."""
        sample_text = "Sample text for batch processing."
        return self.template_manager.generate_api_prompt(sample_text, self.framework_name)
    
    def generate_simple_prompt(self) -> str:
        """Generate a simple single-analysis prompt using new template system."""
        sample_text = "Sample text for simple analysis."
        return self.template_manager.generate_api_prompt(sample_text, self.framework_name)

def generate_prompt(dipoles: Dict, framework: Dict, interactive: bool = True, framework_name: str = None) -> str:
    """
    DEPRECATED: Legacy function for backward compatibility.
    
    NEW CODE SHOULD USE: PromptTemplateManager.generate_*_prompt() methods
    
    This function provides backward compatibility by using the new template system.
    """
    print("⚠️  DEPRECATION WARNING: generate_prompt() function is deprecated.")
    print("   Use PromptTemplateManager methods instead.")
    
    template_manager = PromptTemplateManager()
    
    # Determine framework name
    if not framework_name:
        framework_name = dipoles.get('framework_name') or framework.get('framework_name') or "civic_virtue"
    
    if interactive:
        return template_manager.generate_interactive_prompt(framework_name)
    else:
        sample_text = "Sample text for prompt generation."
        return template_manager.generate_api_prompt(sample_text, framework_name)

def main():
    """Generate prompt using unified template system."""
    parser = argparse.ArgumentParser(description="Generate LLM prompts using unified template system")
    parser.add_argument("--framework", default="civic_virtue", 
                       help="Framework to use (civic_virtue, political_spectrum, moral_rhetorical_posture)")
    parser.add_argument("--mode", choices=["interactive", "api", "batch"], default="interactive",
                       help="Prompt generation mode")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--experiment-id", help="Experimental prompt variant ID")
    parser.add_argument("--variant", help="Experimental variant name")
    
    args = parser.parse_args()
    
    # Initialize template manager
    template_manager = PromptTemplateManager()
    
    try:
        # Generate prompt based on mode
        if args.experiment_id and args.variant:
            # Experimental mode requires sample text
            sample_text = "Sample text for experimental prompt generation."
            prompt = template_manager.generate_experimental_prompt(
                sample_text, args.framework, args.experiment_id, args.variant
            )
            mode_description = f"Experimental ({args.experiment_id}/{args.variant})"
        elif args.mode == "interactive":
            prompt = template_manager.generate_interactive_prompt(args.framework)
            mode_description = "Interactive"
        elif args.mode == "api":
            # API mode requires sample text
            sample_text = "Sample text for API prompt generation."
            prompt = template_manager.generate_api_prompt(sample_text, args.framework)
            mode_description = "API"
        else:  # batch
            sample_text = "Sample text for batch prompt generation."
            prompt = template_manager.generate_api_prompt(sample_text, args.framework)
            mode_description = "Batch"
        
        # Output
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                f.write(prompt)
            
            print(f"✅ Prompt generated: {output_path}")
            print(f"   Framework: {args.framework}")
            print(f"   Mode: {mode_description}")
            print(f"   Template System: Unified v1.0")
        else:
            print(prompt)
        
    except Exception as e:
        print(f"❌ Error generating prompt: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 