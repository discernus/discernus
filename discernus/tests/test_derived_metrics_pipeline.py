import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from pathlib import Path

from discernus.orchestration.derived_metrics_pipeline import DerivedMetricsPipeline
from discernus.core.prompt_assemblers.derived_metrics_assembler import DerivedMetricsPromptAssembler
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.core.secure_code_executor import SecureCodeExecutor

class TestDerivedMetricsPipeline(unittest.TestCase):

    @patch('discernus.core.secure_code_executor.SecureCodeExecutor')
    @patch('discernus.gateway.llm_gateway.LLMGateway')
    @patch('discernus.core.prompt_assemblers.derived_metrics_assembler.DerivedMetricsPromptAssembler')
    def test_pipeline_executes_successfully(self, MockAssembler, MockGateway, MockExecutor):
        """
        Verify the full pipeline integrates and returns a DataFrame.
        """
        # 1. Setup Mocks
        mock_assembler = MockAssembler.return_value
        mock_gateway = MockGateway.return_value
        mock_executor = MockExecutor.return_value

        # Mock Assembler to return a dummy prompt
        mock_assembler.assemble_prompt.return_value = "This is a test prompt."

        # Mock LLM Gateway to return executable Python code
        mock_code = """
import pandas as pd
def calculate_derived_metrics(df):
    df['new_metric'] = df['col_a'] + df['col_b']
    return df
"""
        mock_gateway.generate_text.return_value = (mock_code, {"success": True})

        # Mock Secure Code Executor to return a successful execution result
        # The executor should return the result as a JSON string
        mock_result_df = pd.DataFrame({
            'col_a': [1, 3], 'col_b': [2, 4], 'new_metric': [3, 7]
        })
        mock_executor.execute_code.return_value = {
            "success": True,
            "result_json": mock_result_df.to_json(orient='split'),
            "stdout": "",
            "stderr": ""
        }

        # 2. Prepare Input Data
        # The pipeline will load this from files, but for the test we pass it directly.
        raw_df = pd.DataFrame({'col_a': [1, 3], 'col_b': [2, 4]})

        # 3. Instantiate and Run Pipeline
        pipeline = DerivedMetricsPipeline(
            framework_path=Path("/fake/framework.md"),
            analysis_dir=Path("/fake/analysis"),
            # Pass mock instances for dependency injection
            prompt_assembler=mock_assembler,
            llm_gateway=mock_gateway,
            code_executor=mock_executor
        )
        result_df = pipeline.run(raw_df)

        # 4. Assertions
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertIn('new_metric', result_df.columns)
        self.assertEqual(result_df['new_metric'].tolist(), [3, 7])
        
        mock_assembler.assemble_prompt.assert_called_once()
        mock_gateway.generate_text.assert_called_once_with(
            prompt="This is a test prompt.",
            model="vertex_ai/gemini-2.5-flash" # Assuming a default
        )
        mock_executor.execute_code.assert_called_once()

if __name__ == '__main__':
    unittest.main()
