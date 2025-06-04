#!/usr/bin/env python3
"""
Moral Gravity Wells Prompt Generator

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

def generate_prompt(dipoles: Dict, framework: Dict, interactive: bool = True) -> str:
    """Generate LLM prompt from dipole and framework configurations."""
    
    timestamp = datetime.now().strftime("%Y.%m.%d.%H.%M")
    dipole_version = dipoles.get('version', 'unknown')
    framework_version = framework.get('version', 'unknown')
    
    prompt_lines = []
    
    # Header
    if interactive:
        prompt_lines.extend([
            "Gravity Wells Scoring Prompt - Interactive Analysis Workflow",
            f"Version: {timestamp} (Generated from dipoles v{dipole_version}, framework v{framework_version})",
            "",
            "## Initial Instructions:",
            "",
            "You are an expert political narrative analyst specializing in moral gravity wells analysis. This is an interactive workflow where you'll analyze multiple political texts and provide comparative insights.",
            "",
            "**WORKFLOW:**",
            "1. Start by asking the user to upload their first political narrative file for analysis",
            "2. After each analysis, provide both the JSON output AND separate commentary",
            "3. Ask for additional files to build comparative analysis",
            "4. For each subsequent file, provide comparative insights vs all previous files",
            "",
            "**FILE HANDLING:**",
            "- If your platform supports downloadable files, generate a downloadable JSON file using this naming convention: `YYYY_MM_DD_HHMMSS_[model_name]_analysis.json`",
            "- If downloadable files are not supported, display the formatted JSON clearly for copy/paste",
            "- Always provide the analysis commentary outside the JSON",
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
            "Moral Gravity Wells Analysis Prompt",
            f"Version: {timestamp} (Generated from dipoles v{dipole_version}, framework v{framework_version})",
            "",
            "You are an expert political narrative analyst. Analyze the provided text using the moral gravity wells framework.",
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
        "**ANALYSIS PROCESS:**",
        "1. Assign each well a score (one decimal place)",
        "2. Write concise analysis summary (maximum 500 characters)",
        "3. Generate JSON output with proper metadata",
        "",
        "**JSON OUTPUT FORMAT:**",
        "```json",
        "{",
        "    \"metadata\": {",
        "        \"title\": \"[Narrative Title] (analyzed by [Your Model Name])\",",
        "        \"filename\": \"YYYY_MM_DD_HHMMSS_[model_name]_analysis.json\",",
        "        \"model_name\": \"[Your Model Name]\",",
        "        \"model_version\": \"[Your Version]\",",
        f"        \"prompt_version\": \"{timestamp}\",",
        f"        \"dipoles_version\": \"{dipole_version}\",",
        f"        \"framework_version\": \"{framework_version}\",",
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
            "1. **JSON Output** (formatted for download/copy)",
            "2. **Analysis Commentary** (outside JSON):",
            "   - Key moral themes identified",
            "   - Positioning explanation (why scores were assigned)",
            "   - Notable rhetorical strategies",
            "   - Overall moral framing assessment",
            "3. **Comparative Analysis** (for 2nd+ files):",
            "   - How this narrative compares to previous files",
            "   - Key differences in moral positioning",
            "   - Evolution of themes across analyses",
            "4. **Request for next file** (unless user indicates they're done)",
            "",
            "---",
            "",
            "## Getting Started:",
            "",
            "Please upload your first political narrative file for moral gravity wells analysis. I'll provide both the JSON output and detailed commentary, then we can continue with additional files for comparative analysis.",
            "",
            "What file would you like me to analyze first?"
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