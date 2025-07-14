#!/usr/bin/env python3
"""
Ensemble Configuration Agent
============================

THIN Principle: This agent translates a researcher's plain-English experimental design
into a specific, machine-readable YAML configuration for reproducible analysis.
"""

import sys
from pathlib import Path
import yaml
import re
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.gateway.model_registry import ModelRegistry
    from discernus.gateway.llm_gateway import LLMGateway
    from discernus.core.llm_roles import get_expert_prompt
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"EnsembleConfigurationAgent dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class EnsembleConfigurationAgent:
    """
    Translates natural language experiment design into a machine-readable
    YAML configuration block for the EnsembleOrchestrator.
    """

    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Could not import required dependencies for EnsembleConfigurationAgent")
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)

    def assess_model_health_situation(self, situation_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess a model health situation and provide intelligent recommendations.
        
        Args:
            situation_context: Dictionary containing:
                - required_models: List of models needed by experiment
                - failed_models: List of models that failed health checks
                - healthy_models: List of models that passed health checks
                - health_results: Full health check results
                - project_path: Path to the project
        
        Returns:
            Dictionary with recommendation including:
                - action: 'proceed', 'substitute', 'cancel'
                - explanation: Human-readable explanation
                - adjusted_models: Optional list of substitute models
        """
        try:
            # Prepare context for the LLM
            prompt = f"""
You are an expert research configuration advisor. A researcher is trying to run an experiment but some of their requested models have health issues.

SITUATION:
- Required models: {situation_context['required_models']}
- Failed models: {situation_context['failed_models']}
- Available healthy models: {situation_context['healthy_models']}

HEALTH ISSUES:
"""
            for model in situation_context['failed_models']:
                error = situation_context['health_results']['results'][model]['message']
                prompt += f"- {model}: {error}\n"

            prompt += """
TASK: Analyze this situation and provide a recommendation. Consider:
1. Research impact of missing models
2. Available alternatives from healthy models
3. Whether the experiment can proceed meaningfully

Respond with a JSON object containing:
- "action": "proceed", "substitute", or "cancel"
- "explanation": Clear explanation of your recommendation
- "adjusted_models": Array of substitute models if applicable

Be concise but helpful. Focus on maintaining research quality while being practical.
"""

            # Get LLM recommendation
            response, _ = self.gateway.execute_call(
                model="anthropic/claude-3-haiku-20240307",
                prompt=prompt,
                system_prompt="You are a helpful research configuration advisor. Always respond with valid JSON."
            )
            
            # Parse the response
            import json
            try:
                recommendation = json.loads(response.strip())
                
                # Validate the response has required fields
                if 'action' not in recommendation:
                    recommendation['action'] = 'cancel'
                if 'explanation' not in recommendation:
                    recommendation['explanation'] = 'Unable to generate recommendation'
                    
                return recommendation
                
            except json.JSONDecodeError:
                return {
                    'action': 'cancel',
                    'explanation': 'Unable to parse agent recommendation. Please address model issues manually.'
                }
                
        except Exception as e:
            return {
                'action': 'cancel',
                'explanation': f'Error getting recommendation: {str(e)}'
            }

    def generate_configuration(self, experiment_md_path: str) -> bool:
        """
        Reads an experiment.md file, generates a YAML config from the plain-English
        description if one doesn't exist, and writes it back to the file.

        Returns:
            bool: True if a new configuration was generated, False otherwise.
        """
        experiment_path = Path(experiment_md_path)
        if not experiment_path.exists():
            print(f"❌ Experiment file not found at: {experiment_path}")
            return False

        content = experiment_path.read_text()

        # Check if YAML block already exists
        if "```yaml" in content:
            print("YAML configuration already exists. Skipping generation.")
            return False

        # Extract the methodology section for the LLM
        methodology_section = self._extract_methodology(content)
        if not methodology_section:
            print("Could not find a methodology/design section to generate configuration from.")
            return False

        # Generate the YAML configuration using an LLM
        yaml_config = self._call_config_generator_llm(methodology_section)
        if not yaml_config:
            print("❌ Failed to generate YAML configuration from LLM.")
            return False

        # Append the new YAML block to the experiment file
        self._append_yaml_to_experiment(experiment_path, yaml_config)

        return True

    def _extract_methodology(self, content: str) -> str:
        """Extracts the relevant methodology section from the markdown."""
        # A simple heuristic to find the most relevant part of the text
        match = re.search(r'(#+)\s*(Methodology|Experimental Design|Analysis Plan|Ensemble Specifications)\s*#*', content, re.IGNORECASE)
        if not match:
            return content # Fallback to using the whole document
        
        start_index = match.start()
        # Find the next header of the same or higher level
        next_header_match = re.search(r'^#{{{level_num},}}\s+'.format(level_num=len(match.group(1))), content[start_index + len(match.group(0)):], re.MULTILINE)
        if next_header_match:
            end_index = start_index + len(match.group(0)) + next_header_match.start()
            return content[start_index:end_index]
        else:
            return content[start_index:]

    def _call_config_generator_llm(self, methodology_text: str) -> str:
        """Calls an LLM to generate the YAML configuration."""
        
        # Dynamically get available models from the registry
        available_models = self.model_registry.list_models()
        model_details = [f"- {name}: {self.model_registry.get_model_details(name)}" for name in available_models]

        prompt = f"""
You are an expert in computational social science experimental design. Your task is to convert a researcher's plain-English methodology into a precise, reproducible YAML configuration.

**Available Models:**
{chr(10).join(model_details)}

**Researcher's Methodology:**
---
{methodology_text}
---

**Your Task:**
Based on the researcher's methodology, generate a YAML configuration block. The YAML should only contain the following keys: `models` (a list of exact model identifiers), `num_runs` (an integer), and `remove_synthesis` (a boolean).

- Interpret requests for model tiers (e.g., "top-tier", "cost-effective") and select the appropriate model identifiers.
- If the researcher asks for reliability or consistency checks, set `num_runs` to at least 3. If not specified, default to 1.
- If the experiment mentions "bias isolation", "raw aggregation", or similar, set `remove_synthesis` to `true`. Otherwise, set it to `false`.

**Output ONLY the raw YAML block, with no other text or explanation.**
"""
        
        model_name = "anthropic/claude-3-haiku-20240307"

        try:
            yaml_content, _ = self.gateway.execute_call(model=model_name, prompt=prompt)
            
            if not yaml_content:
                print("❌ LLM response was empty.")
                return ""
                
            # Strip markdown fence if present
            yaml_match = re.search(r'```yaml\n(.*?)```', yaml_content, re.DOTALL)
            if yaml_match:
                yaml_content = yaml_match.group(1)

            # Basic validation to ensure it's valid YAML
            yaml.safe_load(yaml_content)
            return yaml_content
        except (Exception, yaml.YAMLError) as e:
            print(f"❌ Error generating or validating YAML from LLM: {e}")
            return ""

    def _append_yaml_to_experiment(self, experiment_path: Path, yaml_config: str):
        """Appends the generated YAML to the end of the experiment.md file."""
        
        content_to_append = f"""
---
**Generated Configuration (for reproducibility):**
```yaml
{yaml_config.strip()}
```
"""
        with open(experiment_path, 'a') as f:
            f.write(content_to_append)
        print(f"✅ Successfully appended generated YAML configuration to {experiment_path}")

if __name__ == '__main__':
    # This is a placeholder for a potential CLI entry point or test runner
    print("EnsembleConfigurationAgent: Ready for integration with an execution harness.") 