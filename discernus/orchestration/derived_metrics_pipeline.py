import pandas as pd
from pathlib import Path
from typing import Optional

from discernus.core.prompt_assemblers.derived_metrics_assembler import DerivedMetricsPromptAssembler
from discernus.gateway.llm_gateway import LLMGateway
from discernus.core.secure_code_executor import SecureCodeExecutor
from discernus.gateway.model_registry import ModelRegistry

class DerivedMetricsPipeline:
    """
    Orchestrates the generation and execution of derived metrics code.
    """

    def __init__(self,
                 framework_path: Path,
                 analysis_dir: Path,
                 prompt_assembler: Optional[DerivedMetricsPromptAssembler] = None,
                 llm_gateway: Optional[LLMGateway] = None,
                 code_executor: Optional[SecureCodeExecutor] = None):
        
        self.framework_path = framework_path
        self.analysis_dir = analysis_dir
        
        # Allow dependency injection for testing
        self.prompt_assembler = prompt_assembler or DerivedMetricsPromptAssembler()
        self.llm_gateway = llm_gateway or LLMGateway(ModelRegistry())
        self.code_executor = code_executor or SecureCodeExecutor()

    def run(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes the full pipeline.

        Args:
            raw_df: The raw analysis data as a pandas DataFrame.

        Returns:
            A new DataFrame with the derived metrics added.
        """
        # 1. Assemble the prompt
        prompt = self.prompt_assembler.assemble_prompt(self.framework_path, self.analysis_dir)

        # 2. Generate the code from the LLM
        # For now, assume a default model. This can be configured later.
        code_str, metadata = self.llm_gateway.generate_text(
            prompt=prompt,
            model="vertex_ai/gemini-2.5-flash"
        )
        if not metadata.get("success"):
            raise RuntimeError(f"LLM code generation failed: {metadata.get('error')}")

        # 3. Execute the code
        # The executor needs the raw DataFrame to be available in the execution context
        execution_result = self.code_executor.execute_code(
            code_str,
            input_data={'df': raw_df.to_json(orient='split')}
        )
        if not execution_result["success"]:
            raise RuntimeError(f"Code execution failed: {execution_result['stderr']}")
        
        # 4. Process the result
        # The executed code is expected to place the final DataFrame JSON in 'result_json'
        result_json = execution_result.get("result_json")
        if not result_json:
            raise ValueError("Execution did not produce 'result_json' in its output.")
            
        return pd.read_json(result_json, orient='split')
