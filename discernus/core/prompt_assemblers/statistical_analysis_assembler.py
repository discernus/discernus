import json
import yaml
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd

class StatisticalAnalysisPromptAssembler:
    """
    Assembles a prompt for an LLM to generate Python code for comprehensive
    statistical analysis of experimental data.
    """

    def assemble_prompt(self, framework_path: Path, experiment_path: Path, 
                       analysis_dir: Path, derived_metrics_dir: Path) -> str:
        """
        Constructs the prompt for statistical analysis code generation.

        Args:
            framework_path: Path to the framework.md file.
            experiment_path: Path to the experiment.md file.
            analysis_dir: Path to directory containing raw analysis JSON files.
            derived_metrics_dir: Path to directory containing derived metrics JSON files.

        Returns:
            The fully formatted prompt string.
        """
        # Read experiment and framework content (whole files, no parsing)
        experiment_content = self._read_file(experiment_path)
        framework_content = self._read_file(framework_path)
        
        # Sample raw data files for context
        raw_samples = self._sample_analysis_data(analysis_dir, 2)
        derived_samples = self._sample_derived_metrics_data(derived_metrics_dir, 2)
        
        # Load the YAML prompt template
        prompt_template = self._load_prompt_template()
        
        # Extract experiment information
        experiment_spec = self._parse_experiment_spec(experiment_path)
        experiment_name = experiment_spec.get('name', 'Unknown Experiment')
        experiment_description = experiment_spec.get('description', 'No description')
        research_questions = experiment_spec.get('questions', [])
        research_questions_text = "\n".join([f"- {q}" for q in research_questions]) if research_questions else "- No specific research questions provided"
        
        # Format the prompt template
        prompt = prompt_template.format(
            framework_content=framework_content,
            experiment_name=experiment_name,
            experiment_description=experiment_description,
            research_questions=research_questions_text
        )
        
        # Add data structure samples for context
        prompt += f"""

**DATA STRUCTURE SAMPLES FOR CONTEXT:**
Raw Analysis Sample (first 2 files):
{json.dumps(raw_samples, indent=2)}

Derived Metrics Sample (first 2 files):
{json.dumps(derived_samples, indent=2)}

**IMPORTANT**: The functions you generate should read data from workspace files in the current directory, not take parameters. Use glob or similar to find all JSON files in the current directory.

Respond with pure Python code only - no markdown, no explanations."""

        return prompt.strip()

    def _read_file(self, file_path: Path) -> str:
        """Read file content safely."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _sample_analysis_data(self, analysis_dir: Path, sample_size: int) -> List[Dict[str, Any]]:
        """Sample analysis data files for context."""
        if not analysis_dir.is_dir():
            raise FileNotFoundError(f"Analysis directory not found: {analysis_dir}")
        
        sample_files = list(analysis_dir.glob("*.json"))[:sample_size]
        samples = []
        for file_path in sample_files:
            content = self._read_file(file_path)
            samples.append(json.loads(content))
        
        return samples

    def _sample_derived_metrics_data(self, derived_metrics_dir: Path, sample_size: int) -> List[Dict[str, Any]]:
        """Sample derived metrics data files for context."""
        if not derived_metrics_dir.is_dir():
            raise FileNotFoundError(f"Derived metrics directory not found: {derived_metrics_dir}")
        
        sample_files = list(derived_metrics_dir.glob("*.json"))[:sample_size]
        samples = []
        for file_path in sample_files:
            content = self._read_file(file_path)
            samples.append(json.loads(content))
        
        return samples

    def _load_prompt_template(self) -> str:
        """Load external YAML prompt template following THIN architecture."""
        import os
        
        # Find prompt.yaml in agent directory
        agent_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'agents', 'automated_statistical_analysis')
        prompt_path = os.path.join(agent_dir, 'prompt.yaml')
        
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        # Load prompt template
        with open(prompt_path, 'r') as f:
            prompt_data = yaml.safe_load(f)
        
        if 'template' not in prompt_data:
            raise ValueError(f"Prompt file missing 'template' key: {prompt_path}")
        
        return prompt_data['template']

    def _parse_experiment_spec(self, experiment_path: Path) -> Dict[str, Any]:
        """Parse experiment specification for metadata."""
        try:
            experiment_content = self._read_file(experiment_path)
            # Simple parsing for experiment name and description
            lines = experiment_content.split('\n')
            name = "Unknown Experiment"
            description = "No description"
            questions = []
            
            for line in lines:
                if line.startswith('# '):
                    name = line[2:].strip()
                elif line.startswith('## Description') or line.startswith('## Overview'):
                    # Look for description in next few lines
                    for i, desc_line in enumerate(lines[lines.index(line)+1:lines.index(line)+5]):
                        if desc_line.strip() and not desc_line.startswith('#'):
                            description = desc_line.strip()
                            break
                elif line.startswith('## Questions') or line.startswith('## Research Questions'):
                    # Look for questions in next few lines
                    for i, q_line in enumerate(lines[lines.index(line)+1:lines.index(line)+10]):
                        if q_line.strip() and not q_line.startswith('#'):
                            if q_line.strip().startswith('- '):
                                questions.append(q_line.strip()[2:])
                            elif q_line.strip().startswith('* '):
                                questions.append(q_line.strip()[2:])
                            elif q_line.strip() and not q_line.startswith('```'):
                                questions.append(q_line.strip())
                        elif q_line.startswith('```'):
                            break
            
            return {
                'name': name,
                'description': description,
                'questions': questions
            }
        except Exception:
            return {
                'name': 'Unknown Experiment',
                'description': 'No description',
                'questions': []
            }
