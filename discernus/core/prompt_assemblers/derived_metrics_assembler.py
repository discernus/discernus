import json
import yaml
from pathlib import Path
from typing import List, Dict, Any

# A placeholder for where CapabilityRegistry will live
# from discernus.core.capability_registry import CapabilityRegistry

class DerivedMetricsPromptAssembler:
    """
    Assembles a complete prompt for an LLM to generate Python code for calculating
    derived metrics based on a framework and raw analysis data.
    """

    # A simple placeholder for the registry until it's fully integrated
    ALLOWED_LIBRARIES = [
        'pandas', 'numpy', 'scipy', 'sklearn', 'json', 'math', 'statistics'
    ]

    def assemble_prompt(self, framework_path: Path, analysis_dir: Path, sample_size: int = 3) -> str:
        """
        Reads framework and analysis artifacts, samples the data, and constructs the prompt.

        Args:
            framework_path: Path to the framework.md file.
            analysis_dir: Path to the directory containing raw analysis JSON files.
            sample_size: The number of analysis files to include as a sample.

        Returns:
            The fully formatted prompt string.
        """
        framework_content = self._read_file(framework_path)
        analysis_samples = self._sample_analysis_data(analysis_dir, sample_size)

        prompt = f"""
You are a senior computational social scientist. Your task is to write a single, complete Python script that calculates derived metrics based on a provided analytical framework and a sample of raw data.

**INSTRUCTIONS:**
1.  Analyze the `FRAMEWORK` and `DATA SAMPLE` sections below.
2.  Write a Python script that defines a single function `calculate_derived_metrics(df)`.
3.  The function must take a pandas DataFrame as input. The DataFrame will contain the raw data, structured like the provided sample.
4.  The function must calculate all metrics defined in the `derived_metrics` section of the framework.
5.  The function must return a new pandas DataFrame containing the original columns plus the new derived metric columns.
6.  The script MUST be self-contained and ready for immediate execution.

**EXECUTION ENVIRONMENT CONSTRAINTS:**
- You may ONLY import libraries from the following approved list:
- ALLOWED_LIBRARIES: {', '.join(self.ALLOWED_LIBRARIES)}
- The script CANNOT perform any file I/O (e.g., reading or writing files).
- The script must not contain any markdown formatting (e.g., ```python).

---
**FRAMEWORK:**
{framework_content}

---
**DATA SAMPLE:**
Here is a sample of the raw analysis data. The full dataset will follow this structure.
```json
{json.dumps(analysis_samples, indent=2)}
```
---

Now, provide the complete Python script.
"""
        return prompt.strip()

    def _read_file(self, file_path: Path) -> str:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _sample_analysis_data(self, analysis_dir: Path, sample_size: int) -> List[Dict[str, Any]]:
        if not analysis_dir.is_dir():
            raise FileNotFoundError(f"Analysis directory not found: {analysis_dir}")
        
        sample_files = list(analysis_dir.glob("*.json"))[:sample_size]
        samples = []
        for file_path in sample_files:
            content = self._read_file(file_path)
            samples.append(json.loads(content))
        
        return samples
