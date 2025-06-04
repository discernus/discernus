#!/usr/bin/env python3
"""
Narrative Gravity Wells Prompt Generator

Generates LLM analysis prompts from dipole configuration files.
This enables easy customization and extensibility of the framework.

Usage: python generate_prompt.py [--config-dir config] [--output prompt.txt]
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List

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
    Wrapper class for prompt generation functionality.
    Provides a class-based interface for Streamlit integration.
    """
    
    def __init__(self, config_dir: str = "config", framework_name: str = None):
        self.config_dir = config_dir
        self.framework_name = framework_name
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
                    from framework_manager import FrameworkManager
                    manager = FrameworkManager()
                    self.framework_name = manager.get_active_framework() or "unknown"
                except:
                    self.framework_name = "unknown"
        
    def generate_interactive_prompt(self) -> str:
        """Generate an interactive workflow prompt."""
        dipoles = load_dipoles(self.config_dir)
        framework = load_framework(self.config_dir)
        return generate_prompt(dipoles, framework, interactive=True, framework_name=self.framework_name)
    
    def generate_batch_prompt(self) -> str:
        """Generate a batch processing prompt."""
        dipoles = load_dipoles(self.config_dir)
        framework = load_framework(self.config_dir)
        return generate_prompt(dipoles, framework, interactive=False, framework_name=self.framework_name)
    
    def generate_simple_prompt(self) -> str:
        """Generate a simple single-analysis prompt."""
        dipoles = load_dipoles(self.config_dir)
        framework = load_framework(self.config_dir)
        return generate_prompt(dipoles, framework, interactive=False, framework_name=self.framework_name)

def generate_prompt(dipoles: Dict, framework: Dict, interactive: bool = True, framework_name: str = None) -> str:
    """Generate LLM prompt from dipole and framework configurations."""
    
    timestamp = datetime.now().strftime("%Y.%m.%d.%H.%M")
    
    # Clean version strings to avoid double-v prefixes
    dipole_version = dipoles.get('version', 'unknown')
    framework_version = framework.get('version', 'unknown')
    
    # Remove existing 'v' prefix if present to avoid duplication
    if dipole_version.startswith('v'):
        dipole_version = dipole_version[1:]
    if framework_version.startswith('v'):
        framework_version = framework_version[1:]
    
    prompt_lines = []
    
    # Header
    if interactive:
        prompt_lines.extend([
            "Gravity Wells Scoring Prompt - Interactive Analysis Workflow",
            f"Version: {timestamp} (Generated from dipoles v{dipole_version}, framework v{framework_version})",
            "",
            "## Model Identification:",
            "",
            "**IMPORTANT: Before we begin the analysis, I need to confirm model identification information:**",
            "",
            "Can you reliably identify your exact model name and version number? If you're uncertain about either:",
            "- Your exact model name (e.g., 'ChatGPT', 'Claude', 'Gemini')",
            "- Your specific version (e.g., 'GPT-4', '3.5 Sonnet', 'Pro')",
            "",
            "Please respond with: 'I cannot reliably identify my model details' and I will ask the user to provide this information.",
            "",
            "If you CAN reliably identify both your model name and version, please proceed with the analysis workflow below.",
            "",
            "---",
            "",
            "## Initial Instructions:",
            "",
            "You are an expert political narrative analyst specializing in narrative gravity wells analysis. This is an interactive workflow where you'll analyze multiple political texts and provide comparative insights.",
            "",
            "**WORKFLOW:**",
            "1. Start by asking the user to upload their first political narrative file for analysis",
            "2. After each analysis, provide both the JSON output AND separate commentary",
            "3. Ask for additional files to build comparative analysis",
            "4. For each subsequent file, provide comparative insights vs all previous files",
            "",
            "**FILE HANDLING:**",
            "- Please format your JSON response in a code block for easy copy/paste",
            "- Use ```json code blocks to make the output easily copyable",
            "- Always provide the analysis commentary outside the JSON code block",
            "",
            "---",
            "",
            "## Analysis Instructions:",
            "",
            "When the user uploads a file, analyze it using the following framework:",
            "",
            "**SCORING CRITERIA:**",
            "Score each narrative on the following gravity wells (0.0 = no presence, 1.0 = maximum presence):",
            ""
        ])
    else:
        prompt_lines.extend([
            "Narrative Gravity Wells Analysis Prompt",
            f"Version: {timestamp} (Generated from dipoles v{dipole_version}, framework v{framework_version})",
            "",
            "You are an expert political narrative analyst. Analyze the provided text using the narrative gravity wells framework.",
            "",
            "**SCORING CRITERIA:**",
            "Score the narrative on each of the following gravity wells (0.0 = no presence, 1.0 = maximum presence):",
            ""
        ])
    
    # Generate dipole descriptions
    for dipole in dipoles['dipoles']:
        positive = dipole['positive']
        negative = dipole['negative']
        
        # Format language cues outside f-string to avoid backslash issues
        positive_cues = ', '.join(['"' + cue + '"' for cue in positive['language_cues']])
        negative_cues = ', '.join(['"' + cue + '"' for cue in negative['language_cues']])
        
        prompt_lines.extend([
            f"**{positive['name']} vs. {negative['name']} ({dipole['name']} Dimension)**",
            f"- {positive['name']}: {positive['description']}",
            f"  Language cues: {positive_cues}",
            f"- {negative['name']}: {negative['description']}",
            f"  Language cues: {negative_cues}",
            ""
        ])
    
    # Analysis process
    prompt_lines.extend([
        "**CONCEPTUAL ASSESSMENT METHODOLOGY:**",
        "",
        "This framework employs a **conceptual assessment approach** that prioritizes semantic understanding over surface-level keyword counting. You should:",
        "",
        "1. **Identify Underlying Moral Frameworks**: First, identify the underlying moral frameworks and values being expressed in each section of the narrative, regardless of specific language used.",
        "",
        "2. **Extract Central Themes**: Determine which moral themes are central to the overall argument vs. merely mentioned in passing. Focus on what drives the core narrative logic.",
        "",
        "3. **Use Language Cues as Indicators**: The provided language cues are illustrative examples, not exhaustive lists. Look for conceptually similar terms, phrases, and ideas that convey the same moral orientations.",
        "",
        "4. **Assess Conceptual Strength**: Score based on how strongly each moral orientation shapes the narrative's fundamental structure and arguments, not just frequency of related words.",
        "",
        "**THREE-STEP ANALYSIS PROCESS:**",
        "1. **Theme Extraction**: Identify the core moral themes and values driving the narrative's central arguments",
        "2. **Centrality Assessment**: Determine which themes are foundational vs. peripheral to the overall message",
        "3. **Holistic Scoring**: Assign scores based on conceptual strength and centrality, not linguistic frequency",
        "",
        "**ANALYSIS PROCESS:**",
        "1. Assign each well a score (one decimal place)",
        "2. Write concise analysis summary (maximum 500 characters)",
        "3. Generate JSON output with proper metadata",
        "",
        "**MODEL IDENTIFICATION FOR JSON:**",
        "- If you can reliably self-identify: Use your actual model name and version",
        "- If you cannot reliably self-identify: Ask the user to provide this information before proceeding",
        "- Format: 'model_name': 'Exact Model Name', 'model_version': 'Exact Version'",
        "",
        "**JSON OUTPUT FORMAT:**",
        "```json",
        "{",
        "    \"metadata\": {",
        "        \"title\": \"[Narrative Title] (analyzed by [Model Name])\",",
        "        \"filename\": \"YYYY_MM_DD_HHMMSS_[model_name]_analysis.json\",",
        "        \"model_name\": \"[Exact Model Name - either self-identified or user-provided]\",",
        "        \"model_version\": \"[Exact Version - either self-identified or user-provided]\",",
        f"        \"prompt_version\": \"{timestamp}\",",
        f"        \"dipoles_version\": \"v{dipole_version}\",",
        f"        \"framework_version\": \"v{framework_version}\",",
        f"        \"framework_name\": \"{framework_name or 'unknown'}\",",
        "        \"summary\": \"[Your 500-character analysis summary]\"",
        "    },",
        "    \"scores\": {"
    ])
    
    # Generate well list for JSON format
    well_names = []
    for dipole in dipoles['dipoles']:
        well_names.append(dipole['positive']['name'])
        well_names.append(dipole['negative']['name'])
    
    for i, well_name in enumerate(well_names):
        comma = "," if i < len(well_names) - 1 else ""
        prompt_lines.append(f"        \"{well_name}\": 0.0{comma}")
    
    prompt_lines.extend([
        "    }",
        "}",
        "```",
        ""
    ])
    
    if interactive:
        prompt_lines.extend([
            "**RESPONSE STRUCTURE:**",
            "1. **JSON Output** (in ```json code block for easy copy/paste):",
            "2. **Analysis Commentary** (outside JSON code block):",
            "   - **Key moral themes identified**: Core moral frameworks and values driving the narrative",
            "   - **Theme centrality analysis**: Which themes are foundational vs. peripheral to the overall argument",
            "   - **Conceptual reasoning**: Why scores were assigned based on semantic strength and narrative importance",
            "   - **Notable rhetorical strategies**: How moral appeals are constructed and deployed",
            "   - **Overall moral framing assessment**: Holistic evaluation of the narrative's moral positioning",
            "3. **Comparative Analysis** (for 2nd+ files):",
            "   - How this narrative compares to previous files",
            "   - Key differences in moral positioning and thematic emphasis",
            "   - Evolution of themes across analyses",
            "4. **Request for next file** (unless user indicates they're done)",
            "",
            "---",
            "",
            "## Getting Started:",
            "",
            "**STEP 1: Model Identification**",
            "First, please confirm whether you can reliably identify your model name and version. If not, I'll ask the user to provide this information.",
            "",
            "**STEP 2: Analysis Workflow**", 
            "Once model information is confirmed, please ask the user to upload their first political narrative file for narrative gravity wells analysis. I'll provide both the JSON output and detailed commentary, then we can continue with additional files for comparative analysis.",
            "",
            "Can you reliably identify your exact model name and version number?"
        ])
    else:
        prompt_lines.extend([
            "**INSTRUCTIONS:**",
            "1. Read the provided text carefully",
            "2. Score each well based on conceptual strength, not keyword frequency",
            "3. Provide the JSON output as specified above",
            "4. Include a brief analysis summary explaining your scoring rationale"
        ])
    
    return '\n'.join(prompt_lines)

def main():
    """Generate prompt from configuration files."""
    parser = argparse.ArgumentParser(description="Generate LLM prompts from configuration")
    parser.add_argument("--config-dir", default="config", help="Configuration directory")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--interactive", action="store_true", default=True, 
                       help="Generate interactive workflow prompt")
    parser.add_argument("--simple", action="store_true", 
                       help="Generate simple single-analysis prompt")
    
    args = parser.parse_args()
    
    # Load configurations
    try:
        dipoles = load_dipoles(args.config_dir)
        framework = load_framework(args.config_dir)
    except FileNotFoundError as e:
        print(f"❌ Configuration error: {e}")
        return 1
    
    # Generate prompt
    interactive_mode = not args.simple
    prompt = generate_prompt(dipoles, framework, interactive_mode)
    
    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(prompt)
        
        print(f"✅ Prompt generated: {output_path}")
        print(f"   Mode: {'Interactive' if interactive_mode else 'Simple'}")
        print(f"   Dipoles: {len(dipoles['dipoles'])} pairs")
        print(f"   Wells: {len(dipoles['dipoles']) * 2} total")
    else:
        print(prompt)
    
    return 0

if __name__ == "__main__":
    exit(main()) 