import json
import yaml
from pathlib import Path
from typing import List, Dict, Any

class DataAggregationPromptAssembler:
    """
    Assembles a prompt for an LLM to generate Python code for aggregating
    structured data from multiple JSON files.
    """

    def assemble_prompt(self, framework_path: Path, analysis_file_paths: List[Path]) -> str:
        """
        Constructs the prompt using the framework's output schema and a sample file.

        Args:
            framework_path: Path to the framework.md file.
            analysis_file_paths: A list of paths to the analysis JSON files.

        Returns:
            The fully formatted prompt string.
        """
        framework_content = self._read_file(framework_path)
        framework_yaml = self._parse_framework(framework_content)
        output_schema = framework_yaml.get("output_schema")

        if not output_schema:
            raise ValueError("`output_schema` not found in framework's machine-readable appendix.")
            
        if not analysis_file_paths:
            raise ValueError("analysis_file_paths cannot be empty.")
            
        # Use the first analysis file as a representative sample
        sample_content = self._read_file(analysis_file_paths[0])

        prompt = f"""You are a Python code generator. Your response must contain ONLY executable Python code, no explanations, no markdown blocks, no comments outside the code.

Generate a function `aggregate_data(file_paths: list) -> pd.DataFrame` that:
1. Reads analysis_result JSON files from the file_paths list
2. For each file, if result_content contains raw_analysis_response, parse it directly
3. If result_content is missing raw_analysis_response, look for a separate raw_analysis_response_v6_[hash] file in the same directory
4. Extract dimensional scores from the nested JSON structure within the DISCERNUS_ANALYSIS_JSON_v6 delimiters
5. Create a 'dimensions' column containing the complete dimensional_scores dictionary for each document
6. Also include document_id and document_name for identification
7. Ignores all evidence data (text content only - evidence arrays should be ignored for scalability)
8. Returns a pandas DataFrame where each row has a 'dimensions' column containing the nested score structure

DATA STRUCTURE SAMPLE:
{json.dumps(json.loads(sample_content), indent=2)}

Respond with pure Python code only - no markdown, no explanations."""
        return prompt.strip()

    def _read_file(self, file_path: Path) -> str:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _parse_framework(self, content: str) -> Dict[str, Any]:
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
