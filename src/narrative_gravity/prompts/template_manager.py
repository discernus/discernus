"""
Unified Prompt Template Management System

This system combines the sophistication of the v2.0 prompt generation with the flexibility
needed for production API use. It provides:

1. Template-based prompt construction (not hard-coded strings)
2. Framework-agnostic design supporting all frameworks
3. Modular components for easy experimentation
4. Consistent prompt quality across manual and API use
5. A/B testing support for prompt optimization

Usage:
    # API usage (runtime)
    template_manager = PromptTemplateManager()
    prompt = template_manager.generate_api_prompt(text, framework, model)
    
    # Manual usage (script)
    prompt = template_manager.generate_interactive_prompt(framework)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class PromptMode(Enum):
    """Prompt generation modes."""
    API = "api"              # For API/automated analysis  
    INTERACTIVE = "interactive"  # For manual LLM interaction
    BATCH = "batch"          # For batch processing
    EXPERIMENTAL = "experimental"  # For A/B testing


@dataclass
class PromptSettings:
    """Configurable prompt settings."""
    enforce_decimal_scale: bool = True
    include_model_identification: bool = True
    include_analysis_methodology: bool = True
    include_examples: bool = False
    max_language_cues: int = 3
    temperature_guidance: Optional[float] = None
    experimental_features: List[str] = field(default_factory=list)
    use_hierarchical_default: bool = False
    hierarchical_settings: Optional[Dict[str, Any]] = None


class PromptTemplateManager:
    """
    Unified template management for all prompt generation needs.
    
    Combines v2.0 sophistication with production flexibility.
    """
    
    def __init__(self, template_dir: str = None, settings_file: str = None):
        self.template_dir = Path(template_dir) if template_dir else Path(__file__).parent / "templates"
        if settings_file:
            self.settings_file = settings_file
        else:
            self.settings_file = Path(__file__).parent / "prompt_settings.json"
        self.settings = self._load_settings()
        self.templates = self._load_templates()
    
    def _load_settings(self) -> PromptSettings:
        """Load prompt configuration settings."""
        settings_path = Path(self.settings_file)
        
        if settings_path.exists():
            with open(settings_path, 'r') as f:
                data = json.load(f)
            
            # Extract only fields that exist in PromptSettings dataclass
            valid_fields = {
                'enforce_decimal_scale': data.get('enforce_decimal_scale', True),
                'include_model_identification': data.get('include_model_identification', True),
                'include_analysis_methodology': data.get('include_analysis_methodology', True),
                'include_examples': data.get('include_examples', False),
                'max_language_cues': data.get('max_language_cues', 3),
                'temperature_guidance': data.get('temperature_guidance', None),
                'experimental_features': data.get('experimental_features', []),
                'use_hierarchical_default': data.get('use_hierarchical_default', False),
                'hierarchical_settings': data.get('hierarchical_settings', None)
            }
                
            return PromptSettings(**valid_fields)
        else:
            # Return defaults
            return PromptSettings()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load prompt template components."""
        templates = {}
        
        if self.template_dir.exists():
            for template_file in self.template_dir.glob("*.txt"):
                template_name = template_file.stem
                with open(template_file, 'r') as f:
                    templates[template_name] = f.read()
        
        return templates
    
    def generate_api_prompt(self, text: str, framework: str, model: str = None) -> str:
        """
        Generate prompt for API/automated analysis.
        
        Optimized for reliable JSON extraction and consistent results.
        """
        # Check if hierarchical approach should be used as default
        if (self.settings.use_hierarchical_default and 
            hasattr(self.settings, 'hierarchical_settings') and 
            self.settings.hierarchical_settings and
            'api' in self.settings.hierarchical_settings.get('enabled_modes', [])):
            
            experiment_id = self.settings.hierarchical_settings['experiment_id']
            variant = self.settings.hierarchical_settings['variant']
            return self.generate_experimental_prompt(text, framework, experiment_id, variant)
        
        # Default non-hierarchical generation
        framework_config = self._load_framework_config(framework)
        
        components = [
            self._build_header(PromptMode.API, framework),
            self._build_role_definition(PromptMode.API),
            self._build_scoring_requirements(),
            self._build_framework_wells(framework_config),
            self._build_analysis_methodology(abbreviated=True),
            self._build_json_format(framework_config),
            self._build_text_section(text),
            self._build_instructions(PromptMode.API)
        ]
        
        return self._assemble_prompt(components)
    
    def generate_interactive_prompt(self, framework: str) -> str:
        """
        Generate prompt for manual LLM interaction.
        
        Includes full v2.0 sophistication for human-guided analysis.
        """
        # Check if hierarchical approach should be used as default
        if (self.settings.use_hierarchical_default and 
            hasattr(self.settings, 'hierarchical_settings') and 
            self.settings.hierarchical_settings and
            'interactive' in self.settings.hierarchical_settings.get('enabled_modes', [])):
            
            experiment_id = self.settings.hierarchical_settings['experiment_id']
            variant = self.settings.hierarchical_settings['variant']
            # For interactive mode, we need a sample text, so use a placeholder
            sample_text = "[TEXT TO BE PROVIDED BY USER]"
            return self.generate_experimental_prompt(sample_text, framework, experiment_id, variant)
        
        # Default non-hierarchical generation
        framework_config = self._load_framework_config(framework)
        
        components = [
            self._build_header(PromptMode.INTERACTIVE, framework),
            self._build_model_identification(),
            self._build_workflow_instructions(),
            self._build_role_definition(PromptMode.INTERACTIVE),
            self._build_scoring_requirements(),
            self._build_framework_wells(framework_config),
            self._build_analysis_methodology(abbreviated=False),
            self._build_json_format(framework_config),
            self._build_response_structure(),
            self._build_instructions(PromptMode.INTERACTIVE)
        ]
        
        return self._assemble_prompt(components)
    
    def generate_experimental_prompt(self, text: str, framework: str, 
                                   experiment_id: str, variant: str) -> str:
        """
        Generate prompt for A/B testing experiments.
        
        Allows testing different prompt variations while maintaining structure.
        """
        # Load experimental variations
        experiment_config = self._load_experiment_config(experiment_id, variant)
        framework_config = self._load_framework_config(framework)
        
        # Build with experimental modifications
        components = [
            self._build_header(PromptMode.EXPERIMENTAL, framework, experiment_id),
            self._build_role_definition(PromptMode.API, experiment_config),
            self._build_scoring_requirements(experiment_config),
            self._build_framework_wells(framework_config, experiment_config),
            self._build_analysis_methodology(experiment_config=experiment_config),
            self._build_json_format(framework_config),
            self._build_text_section(text),
            self._build_instructions(PromptMode.EXPERIMENTAL, experiment_config)
        ]
        
        return self._assemble_prompt(components)
    
    def _load_framework_config(self, framework: str) -> Dict[str, Any]:
        """Load framework configuration files - supports both old and new consolidated formats."""
        framework_path = Path("frameworks") / framework
        
        # Try new consolidated format first
        consolidated_path = framework_path / "framework_consolidated.json"
        if consolidated_path.exists():
            with open(consolidated_path, 'r') as f:
                consolidated_config = json.load(f)
            
            # Extract components from consolidated format
            return {
                "dipoles": {
                    "dipoles": consolidated_config.get("dipoles", []),
                    "framework_name": consolidated_config.get("framework_meta", {}).get("name", framework),
                    "description": consolidated_config.get("framework_meta", {}).get("description", ""),
                    "version": consolidated_config.get("framework_meta", {}).get("version", "v1.0.0")
                },
                "framework": {
                    "wells": consolidated_config.get("wells", {}),
                    "framework_name": consolidated_config.get("framework_meta", {}).get("name", framework),
                    "version": consolidated_config.get("framework_meta", {}).get("version", "v1.0.0"),
                    "description": consolidated_config.get("framework_meta", {}).get("description", "")
                },
                "name": framework
            }
        
        # Fallback to old separate files format
        dipoles_path = framework_path / "dipoles.json"
        framework_config_path = framework_path / "framework.json"
        
        if dipoles_path.exists() and framework_config_path.exists():
            # Load dipoles configuration
            with open(dipoles_path, 'r') as f:
                dipoles_config = json.load(f)
            
            # Load framework configuration  
            with open(framework_config_path, 'r') as f:
                framework_config = json.load(f)
            
            return {
                "dipoles": dipoles_config,
                "framework": framework_config,
                "name": framework
            }
        
        # If neither format exists, raise an error
        raise FileNotFoundError(f"Framework '{framework}' not found. Expected either 'framework_consolidated.json' or both 'dipoles.json' and 'framework.json' in {framework_path}")
    
    def _load_experiment_config(self, experiment_id: str, variant: str) -> Dict[str, Any]:
        """Load experimental prompt variations."""
        experiment_path = self.template_dir / "experiments" / f"{experiment_id}.json"
        
        if experiment_path.exists():
            with open(experiment_path, 'r') as f:
                experiments = json.load(f)
            return experiments.get(variant, {})
        else:
            return {}
    
    def _build_header(self, mode: PromptMode, framework: str, experiment_id: str = None) -> str:
        """Build prompt header with version and metadata."""
        timestamp = datetime.now().strftime("%Y.%m.%d.%H.%M")
        
        if experiment_id:
            title = f"Experimental Narrative Gravity Analysis - {experiment_id}"
        elif mode == PromptMode.INTERACTIVE:
            title = "Interactive Narrative Gravity Analysis Workflow"
        else:
            title = "Narrative Gravity Analysis"
        
        return f"""{title}
Version: {timestamp} | Framework: {framework} | Mode: {mode.value}

"""
    
    def _build_model_identification(self) -> str:
        """Build model identification section."""
        if not self.settings.include_model_identification:
            return ""
        
        return """## Model Identification:

**IMPORTANT: Before we begin the analysis, I need to confirm model identification information:**

Can you reliably identify your exact model name and version number? If you're uncertain about either:
- Your exact model name (e.g., 'ChatGPT', 'Claude', 'Gemini')
- Your specific version (e.g., 'GPT-4', '3.5 Sonnet', 'Pro')

Please respond with: 'I cannot reliably identify my model details' and I will ask the user to provide this information.

If you CAN reliably identify both your model name and version, please proceed with the analysis workflow below.

---

"""
    
    def _build_workflow_instructions(self) -> str:
        """Build interactive workflow instructions."""
        return """## Interactive Workflow:

**PROCESS:**
1. Start by asking the user to upload their first narrative file for analysis
2. After each analysis, provide both the JSON output AND separate commentary
3. Ask for additional files to build comparative analysis
4. For each subsequent file, provide comparative insights vs all previous files

**FILE HANDLING:**
- Please format your JSON response in a code block for easy copy/paste
- Use ```json code blocks to make the output easily copyable
- Always provide the analysis commentary outside the JSON code block

---

"""
    
    def _build_role_definition(self, mode: PromptMode, experiment_config: Dict = None) -> str:
        """Build role definition for the LLM."""
        if experiment_config and "role_definition" in experiment_config:
            return experiment_config["role_definition"] + "\n\n"
        
        if mode == PromptMode.INTERACTIVE:
            role = "You are an expert narrative analyst specializing in narrative gravity wells analysis. This is an interactive workflow where you'll analyze multiple texts and provide comparative insights."
        else:
            role = "You are an expert narrative analyst. Analyze the provided text using the narrative gravity wells framework."
        
        return f"{role}\n\n"
    
    def _build_scoring_requirements(self, experiment_config: Dict = None) -> str:
        """Build scoring requirements section."""
        if not self.settings.enforce_decimal_scale:
            return ""
        
        if experiment_config and "scoring_requirements" in experiment_config:
            return experiment_config["scoring_requirements"] + "\n\n"
        
        return """**CRITICAL SCORING REQUIREMENTS:**

🚨 **MANDATORY DECIMAL SCALE: 0.0 to 1.0 ONLY** 🚨
- Use ONLY decimal values between 0.0 and 1.0 (e.g., 0.3, 0.7, 0.9)
- DO NOT use integers 1-10 or any other scale
- DO NOT use percentages or any scale other than 0.0-1.0
- Example valid scores: 0.1, 0.4, 0.6, 0.8, 1.0
- Example INVALID scores: 1, 5, 10, 25%, 0.5/1.0

"""
    
    def _build_framework_wells(self, framework_config: Dict, experiment_config: Dict = None) -> str:
        """Build framework-specific wells descriptions."""
        # Handle different dipoles structures
        dipoles_config = framework_config["dipoles"]
        
        if "dipoles" in dipoles_config:
            # Full dipoles structure (like civic_virtue)
            dipoles = dipoles_config["dipoles"]
        elif "primary" in dipoles_config:
            # Simple dipoles structure (like political_spectrum)
            # Convert to expected format
            dipoles = [{
                "name": "Primary",
                "positive": {
                    "name": dipoles_config["primary"]["positive"],
                    "description": f"Emphasis on {dipoles_config['primary']['positive'].lower()} themes",
                    "language_cues": []
                },
                "negative": {
                    "name": dipoles_config["primary"]["negative"],
                    "description": f"Emphasis on {dipoles_config['primary']['negative'].lower()} themes",
                    "language_cues": []
                }
            }]
        else:
            # Fallback for unknown structure
            dipoles = []
        
        lines = ["**FRAMEWORK WELLS:**\n"]
        
        for dipole in dipoles:
            positive = dipole["positive"]
            negative = dipole["negative"]
            
            # Get language cues (limited by settings)
            pos_cues = positive.get('language_cues', [])[:self.settings.max_language_cues]
            neg_cues = negative.get('language_cues', [])[:self.settings.max_language_cues]
            
            lines.append(f"**{positive['name']} vs. {negative['name']} ({dipole['name']} Dimension)**")
            lines.append(f"- {positive['name']}: {positive['description']}")
            if pos_cues:
                lines.append(f"  Language cues: {', '.join(pos_cues)}")
            lines.append(f"- {negative['name']}: {negative['description']}")
            if neg_cues:
                lines.append(f"  Language cues: {', '.join(neg_cues)}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _build_analysis_methodology(self, abbreviated: bool = False, experiment_config: Dict = None) -> str:
        """Build analysis methodology section."""
        if not self.settings.include_analysis_methodology:
            return ""
        
        if experiment_config and "methodology" in experiment_config:
            return experiment_config["methodology"] + "\n\n"
        
        if abbreviated:
            return """**ANALYSIS APPROACH:**
- Focus on conceptual strength, not keyword frequency
- Score based on how strongly each orientation shapes the narrative's structure
- Provide brief justification for scores

"""
        else:
            return """**CONCEPTUAL ASSESSMENT METHODOLOGY:**

This framework employs a **conceptual assessment approach** that prioritizes semantic understanding over surface-level keyword counting. You should:

1. **Identify Underlying Frameworks**: First, identify the underlying frameworks and values being expressed in each section of the narrative, regardless of specific language used.

2. **Extract Central Themes**: Determine which themes are central to the overall argument vs. merely mentioned in passing. Focus on what drives the core narrative logic.

3. **Use Language Cues as Indicators**: The provided language cues are illustrative examples, not exhaustive lists. Look for conceptually similar terms, phrases, and ideas that convey the same orientations.

4. **Assess Conceptual Strength**: Score based on how strongly each orientation shapes the narrative's fundamental structure and arguments, not just frequency of related words.

**THREE-STEP ANALYSIS PROCESS:**
1. **Theme Extraction**: Identify the core themes and values driving the narrative's central arguments
2. **Centrality Assessment**: Determine which themes are foundational vs. peripheral to the overall message
3. **Holistic Scoring**: Assign scores based on conceptual strength and centrality, not linguistic frequency

"""
    
    def _build_json_format(self, framework_config: Dict) -> str:
        """Build JSON format specification."""
        timestamp = datetime.now().strftime("%Y.%m.%d.%H.%M")
        
        # Handle different dipoles structures
        dipoles_config = framework_config["dipoles"]
        
        if "dipoles" in dipoles_config:
            # Full dipoles structure (like civic_virtue)
            dipoles = dipoles_config["dipoles"]
        elif "primary" in dipoles_config:
            # Simple dipoles structure (like political_spectrum)
            dipoles = [{
                "positive": {"name": dipoles_config["primary"]["positive"]},
                "negative": {"name": dipoles_config["primary"]["negative"]}
            }]
        else:
            # Fallback for unknown structure
            dipoles = []
        
        framework_name = framework_config["name"]
        
        # Get all well names
        well_names = []
        for dipole in dipoles:
            well_names.append(dipole["positive"]["name"])
            well_names.append(dipole["negative"]["name"])
        
        lines = [
            "**RESPONSE FORMAT (JSON):**",
            "",
            "```json",
            "{",
            '  "scores": {'
        ]
        
        for i, well_name in enumerate(well_names):
            comma = "," if i < len(well_names) - 1 else ""
            lines.append(f'    "{well_name}": 0.0{comma}')
        
        lines.extend([
            "  },",
            '  "analysis": "Brief explanation of scoring rationale"',
            "}",
            "```",
            ""
        ])
        
        return "\n".join(lines)
    
    def _build_text_section(self, text: str) -> str:
        """Build text analysis section."""
        return f"""**TEXT TO ANALYZE:**

{text}

"""
    
    def _build_response_structure(self) -> str:
        """Build response structure guidance for interactive mode."""
        return """**RESPONSE STRUCTURE:**
1. **JSON Output** (in ```json code block for easy copy/paste)
2. **Analysis Commentary** (outside JSON code block):
   - **Key themes identified**: Core frameworks and values driving the narrative
   - **Theme centrality analysis**: Which themes are foundational vs. peripheral
   - **Conceptual reasoning**: Why scores were assigned based on semantic strength
   - **Notable rhetorical strategies**: How thematic appeals are constructed
   - **Overall framing assessment**: Holistic evaluation within the framework
3. **Comparative Analysis** (for 2nd+ files):
   - How this narrative compares to previous files
   - Key differences in positioning and thematic emphasis

"""
    
    def _build_instructions(self, mode: PromptMode, experiment_config: Dict = None) -> str:
        """Build final instructions section."""
        if experiment_config and "instructions" in experiment_config:
            return experiment_config["instructions"]
        
        if mode == PromptMode.INTERACTIVE:
            return """**Getting Started:**

Please confirm whether you can reliably identify your model name and version. If not, I'll ask the user to provide this information.

Once confirmed, please ask the user to upload their first narrative file for analysis."""
        else:
            return """**INSTRUCTIONS:**
1. Read the provided text carefully
2. Score each well based on conceptual strength (0.0-1.0 scale ONLY)
3. Write a concise analysis summary (maximum 500 characters)
4. Provide the JSON output as specified above with scores and analysis summary"""
    
    def _assemble_prompt(self, components: List[str]) -> str:
        """Assemble components into final prompt."""
        # Filter out empty components
        filtered_components = [comp for comp in components if comp.strip()]
        return "\n".join(filtered_components)
    
    def save_experiment_template(self, experiment_id: str, variants: Dict[str, Dict]) -> None:
        """Save experimental prompt variations for A/B testing."""
        experiment_path = self.template_dir / "experiments" / f"{experiment_id}.json"
        experiment_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(experiment_path, 'w') as f:
            json.dump(variants, f, indent=2)
    
    def list_available_experiments(self) -> List[str]:
        """List available experimental prompt variants."""
        experiment_dir = self.template_dir / "experiments"
        if not experiment_dir.exists():
            return []
        
        return [f.stem for f in experiment_dir.glob("*.json")]
    
    def list_available_frameworks(self) -> List[str]:
        """List available frameworks."""
        frameworks_dir = Path("frameworks")
        if frameworks_dir.exists():
            return [f.name for f in frameworks_dir.iterdir() if f.is_dir()]
        return []
    
    @property
    def frameworks(self) -> Dict[str, str]:
        """Property for backward compatibility."""
        return {name: name for name in self.list_available_frameworks()} 