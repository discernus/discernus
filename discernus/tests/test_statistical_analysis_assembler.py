
Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest
import tempfile
import json
import pandas as pd
from pathlib import Path
from unittest.mock import patch, mock_open
from discernus.core.prompt_assemblers.statistical_analysis_assembler import StatisticalAnalysisPromptAssembler

class TestStatisticalAnalysisPromptAssembler(unittest.TestCase):
    
    def setUp(self):
        self.assembler = StatisticalAnalysisPromptAssembler()
        
        # Mock framework content
        self.mock_framework_content = """
# Test Framework

## Part 2: The Machine-Readable Appendix

```yaml
name: "test_framework"
version: "1.0.0"
dimensions:
  - name: "dimension_a"
  - name: "dimension_b"
derived_metrics:
  - name: "composite_score"
    formula: "dimension_a + dimension_b"
```
"""
        
        # Mock experiment content
        self.mock_experiment_content = """
# Test Experiment

## Configuration Appendix

```yaml
metadata:
  name: "test_experiment"
  version: "1.0.0"
research_questions:
  - "How do dimensions correlate?"
  - "What is the reliability of the framework?"
components:
  framework: "test_framework.md"
  corpus: "test_corpus.md"
```
"""
        
        # Mock DataFrames
        self.raw_scores_df = pd.DataFrame([
            {'document_id': 'doc1', 'dimension_a': 0.8, 'dimension_b': 0.6},
            {'document_id': 'doc2', 'dimension_a': 0.7, 'dimension_b': 0.9}
        ])
        
        self.derived_metrics_df = pd.DataFrame([
            {'document_id': 'doc1', 'dimension_a': 0.8, 'dimension_b': 0.6, 'composite_score': 1.4},
            {'document_id': 'doc2', 'dimension_a': 0.7, 'dimension_b': 0.9, 'composite_score': 1.6}
        ])

    @patch('pathlib.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_assemble_prompt_successfully(self, mock_file_open, mock_exists):
        """Test that the assembler creates a valid prompt with all required components."""
        # Setup mocks
        mock_exists.return_value = True
        
        def mock_read_side_effect(file_path, *args, **kwargs):
            if 'framework' in str(file_path):
                return mock_open(read_data=self.mock_framework_content).return_value
            elif 'experiment' in str(file_path):
                return mock_open(read_data=self.mock_experiment_content).return_value
            return mock_open().return_value
        
        mock_file_open.side_effect = mock_read_side_effect
        
        # Test the assembler
        framework_path = Path('/fake/framework.md')
        experiment_path = Path('/fake/experiment.md')
        
        prompt = self.assembler.assemble_prompt(
            framework_path=framework_path,
            experiment_path=experiment_path,
            raw_scores_df=self.raw_scores_df,
            derived_metrics_df=self.derived_metrics_df
        )
        
        # Validate prompt content
        self.assertIn("perform_statistical_analysis", prompt)
        self.assertIn("test_framework", prompt)
        self.assertIn("How do dimensions correlate?", prompt)
        self.assertIn("dimension_a", prompt)
        self.assertIn("composite_score", prompt)
        self.assertIn("pandas, numpy, scipy", prompt)
        self.assertIn("pure Python code only", prompt)

if __name__ == '__main__':
    unittest.main()
