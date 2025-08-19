import json
import yaml
from pathlib import Path
from typing import Dict, Any
import pandas as pd

class StatisticalAnalysisPromptAssembler:
    """
    Assembles a prompt for an LLM to generate Python code for comprehensive
    statistical analysis of experimental data.
    """

    def assemble_prompt(self, framework_path: Path, experiment_path: Path, 
                       raw_scores_df: pd.DataFrame, derived_metrics_df: pd.DataFrame) -> str:
        """
        Constructs the prompt for statistical analysis code generation.

        Args:
            framework_path: Path to the framework.md file.
            experiment_path: Path to the experiment.md file.
            raw_scores_df: DataFrame with raw dimensional scores.
            derived_metrics_df: DataFrame with derived metrics calculated.

        Returns:
            The fully formatted prompt string.
        """
        # Read experiment and framework content
        experiment_content = self._read_file(experiment_path)
        framework_content = self._read_file(framework_path)
        
        # Parse research questions and hypotheses from experiment
        experiment_yaml = self._parse_experiment_yaml(experiment_content)
        research_questions = experiment_yaml.get('research_questions', [])
        
        # Parse framework for analytical context
        framework_yaml = self._parse_framework_yaml(framework_content)
        framework_name = framework_yaml.get('name', 'Unknown Framework')
        
        # Create data samples for the prompt
        raw_sample = raw_scores_df.head(2).to_dict('records')
        derived_sample = derived_metrics_df.head(2).to_dict('records')
        
        prompt = f"""You are a Python code generator. Your response must contain ONLY executable Python code, no explanations, no markdown blocks, no comments outside the code.

Generate a function `perform_statistical_analysis(raw_df: pd.DataFrame, derived_df: pd.DataFrame) -> dict` that:
1. Takes raw scores and derived metrics DataFrames as input
2. Performs comprehensive statistical analysis appropriate for the research questions
3. Returns a dictionary with statistical results (descriptive stats, correlations, significance tests, etc.)
4. Uses only these allowed libraries: pandas, numpy, scipy, scipy.stats, statistics, math

RESEARCH CONTEXT:
Framework: {framework_name}
Research Questions: {json.dumps(research_questions, indent=2)}

DATA STRUCTURE SAMPLES:
Raw Scores Sample (first 2 rows):
{json.dumps(raw_sample, indent=2)}

Derived Metrics Sample (first 2 rows):
{json.dumps(derived_sample, indent=2)}

ANALYSIS REQUIREMENTS:
- Descriptive statistics for all dimensions and derived metrics
- Correlation analysis between dimensions
- Reliability analysis (Cronbach's alpha where appropriate)
- Significance testing for research hypotheses
- Effect size calculations
- Return all results as a structured dictionary

Respond with pure Python code only - no markdown, no explanations."""

        return prompt.strip()

    def _read_file(self, file_path: Path) -> str:
        """Read file content safely."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _parse_experiment_yaml(self, content: str) -> Dict[str, Any]:
        """Parse YAML from experiment's machine-readable appendix."""
        try:
            if '## Configuration Appendix' in content:
                _, appendix_content = content.split('## Configuration Appendix', 1)
                if '```yaml' in appendix_content:
                    yaml_start = appendix_content.find('```yaml') + 7
                    yaml_end = appendix_content.rfind('```')
                    yaml_content = appendix_content[yaml_start:yaml_end].strip() if yaml_end > yaml_start else appendix_content[yaml_start:].strip()
                    return yaml.safe_load(yaml_content)
            raise ValueError("Configuration appendix not found in experiment.")
        except Exception as e:
            raise ValueError(f"Failed to parse experiment YAML: {e}")

    def _parse_framework_yaml(self, content: str) -> Dict[str, Any]:
        """Parse YAML from framework's machine-readable appendix."""
        try:
            if '## Part 2: The Machine-Readable Appendix' in content:
                _, appendix_content = content.split('## Part 2: The Machine-Readable Appendix', 1)
                if '```yaml' in appendix_content:
                    yaml_start = appendix_content.find('```yaml') + 7
                    yaml_end = appendix_content.rfind('```')
                    yaml_content = appendix_content[yaml_start:yaml_end].strip() if yaml_end > yaml_start else appendix_content[yaml_start:].strip()
                    return yaml.safe_load(yaml_content)
            raise ValueError("Machine-readable appendix not found in framework.")
        except Exception as e:
            raise ValueError(f"Failed to parse framework YAML: {e}")
